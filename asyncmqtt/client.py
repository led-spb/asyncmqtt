from tornado.ioloop import IOLoop, PeriodicCallback
import paho.mqtt.client as mqtt
import logging
import base64
import os

connack_string = mqtt.connack_string

class TornadoMqttClient(object):
    def __init__(self, ioloop=None, clean_session=True, clientid=None, host='127.0.0.1', port=1883, keepalive=60, username=None, password=None):
        self.ioloop = ioloop or IOLoop.current()

        self._client =  mqtt.Client(client_id=clientid or self._genid(), clean_session=clean_session)
        if username!=None:
            self._client.username_pw_set(self._username, self._password)   

        self._client.on_connect = self.on_mqtt_connect
        self._client.on_disconnect = self.on_mqtt_disconnect
        self._client.on_message = self.on_mqtt_message

        self._client.on_socket_open = self._on_socket_open
        self._client.on_socket_close = self._on_socket_close
        self._client.on_socket_register_write = self._on_socket_register_write
        self._client.on_socket_unregister_write = self._on_socket_unregister_write        

        self.host = host
        self.port = port
        self.keepalive = keepalive

        self._misc_loop = PeriodicCallback(callback=self._handle_misc, callback_time=10000)
        self._reconnect_loop = PeriodicCallback(callback=self._client.reconnect, callback_time=10000)
        pass

    def _genid(self):
        return base64.urlsafe_b64encode(os.urandom(32)).replace('=', 'e')
    
    def start(self):
        logging.info("Connecting to mqtt broker")
        self._client.connect(self.host, self.port, self.keepalive)
        pass

    def on_mqtt_connect(self, client, userdata, flags, rc ):
        logging.info("MQTT broker: %s", mqtt.connack_string(rc))
        pass

    def on_mqtt_disconnect(self, client, userdata, rc):
        logging.info("MQTT broker disconnected, reason: %d", rc)
        if rc>0:
           logging.info("Try to reconnecting...")
           self._reconnect_loop.start()
        pass

    def on_mqtt_message(self, client, userdata, msg):
        pass

    def _on_socket_open(self, client, userdata, sock):
        logging.debug('MQTT Socket %d opened', sock.fileno())

        self._reconnect_loop.stop()
        self._misc_loop.start()

        self.ioloop.add_handler(sock, self._handle_read, IOLoop.READ)
        pass

    def _on_socket_close(self, client, userdata, sock):
        logging.debug('MQTT Socket %d closed', sock.fileno())
        self.ioloop.remove_handler(sock)
        self._misc_loop.stop()
        pass

    def _on_socket_register_write(self, client, userdata, sock):
        logging.debug('MQTT register socket %d write', sock.fileno())
        self.ioloop.update_handler(sock, IOLoop.READ|IOLoop.WRITE)
        pass

    def _on_socket_unregister_write(self, client, userdata, sock):
        logging.debug('MQTT unregister socket %d write', sock.fileno())
        self.ioloop.update_handler(sock, IOLoop.READ)
        pass

    def _start_ioloop(self):
        # not used now to remove
        self._sock = self._client.socket()
        self.ioloop.add_handler(self._sock.fileno(), self._handle_read, IOLoop.READ | IOLoop.WRITE | IOLoop.ERROR)
        self.ioloop.add_handler(self._client._sockpairR.fileno(), self._handle_write, IOLoop.READ | IOLoop.ERROR)
        
        self._misc_loop.start()
        pass

    def _handle_misc(self):
        self._client.loop_misc()

    def _handle_write(self, fd, events):
        # not used now to remove
        if events & IOLoop.READ:
            self._client._sockpairR.recv(1)
            rc = self._client.loop_write() 

    def _handle_read(self, fd, events):
        if events & IOLoop.READ:
            rc = self._client.loop_read()
        if events & IOLoop.WRITE:
            rc = self._client.loop_write()
