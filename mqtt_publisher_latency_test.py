import paho.mqtt.client as mqtt
import argparse
import time

execute_time = []

def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(param.topic, param.qos)

def on_disconnect(client, userdata, flag, rc):
    if  rc != 0:
        print("Unexpected disconnection.")

def on_message(client, userdata, msg):
    execute_time.append(time.time() - float(msg.payload))
    #print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))
    if len(execute_time) == param.cnt:
        print("Average latency(sec): %f" % (sum(execute_time) / len(execute_time)))
        print("Maximum latency(sec): %f" % max(execute_time))
        print("Minimum latency(sec): %f" % min(execute_time))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PROG', conflict_handler='resolve')
    parser.add_argument('-s', '--server', nargs='?', metavar='mqtt broker', help='eule mqtt connector host',required=1)
    parser.add_argument('-t', '--topic', nargs='?', metavar='topic name', help='topic name of mqtt broker',required=1)   
    parser.add_argument('-q', '--qos', nargs='?', type=int, metavar='qos level', help='qos level of mqtt', default=0)
    parser.add_argument('-c','--cnt', nargs='?', type=int, metavar='count of messages', help='count of messages', default=1)
    param = parser.parse_args()
    print('argument : %s' % vars(param))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(param.server, 1883, 60)
    client.loop_forever()
