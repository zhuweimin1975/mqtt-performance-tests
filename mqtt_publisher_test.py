import paho.mqtt.client as mqtt
import time
import argparse
from time import sleep

sended_flag = False
sended_cnt = 0

def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))

def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def on_publish(client, userdata, mid):
    print("publish: {0}".format(mid))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PROG', conflict_handler='resolve')
    parser.add_argument('-s', '--server', nargs='?', metavar='mqtt broker', help='eule mqtt connector host',required=1)
    parser.add_argument('-t', '--topic', nargs='?', metavar='topic name', help='topic name of mqtt broker',required=1)   
    parser.add_argument('-q', '--qos', nargs='?', type=int, metavar='qos level', help='qos level of mqtt', default=0)
    parser.add_argument('-m','--cnt', nargs='?', type=int, metavar='count of messages', help='count of messages', default=1)
    param = parser.parse_args()
    print('argument : %s' % vars(param))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.connect(param.server, 1883, 60)
    client.loop_start()
    while not client.is_connected():
        sleep(1)
    for i in xrange(param.cnt):
        client.publish(param.topic, time.time(), param.qos)
    sleep(3)
