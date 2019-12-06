import paho.mqtt.client as mqtt
import multiprocessing
import time
import argparse
from time import sleep

class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                self.task_queue.task_done()
                break
            answer = next_task(self.name)
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return

def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))

class ConnectToMqttBrokerTask(object):
    def __init__(self, host):
        self.host = host

    def __call__(self, proc_name):
        client = mqtt.Client()
        client.on_connect = on_connect
        start = time.time()
        client.connect(self.host, 1883, 60)
        while not client.is_connected():
            sleep(0.1)
        end = time.time()
        client.disconnect()
        return end - start

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PROG', conflict_handler='resolve')
    parser.add_argument('-s', '--server', nargs='?', metavar='mqtt broker', help='eule mqtt connector host',required=1)
    parser.add_argument('-c', '--connections', nargs='?', metavar='connection numbers', help='connection numbers', default=1)

    param = parser.parse_args()
    print('argument : %s' % vars(param))

    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    num_consumers = int(param.connections)
    print("Creating %d consumers" % num_consumers)
    consumers = [ Consumer(tasks, results)
                 for i in xrange(num_consumers) ]
    for w in consumers:
        w.start()
        tasks.put(ConnectToMqttBrokerTask(param.server))
    for i in xrange(num_consumers):
        tasks.put(None)

    tasks.join()

    execute_time = []
    for i in xrange(num_consumers):
        execute_time.append(results.get())

    print("Average Runtime(sec): %f" % (sum(execute_time) / len(execute_time)))
    print("Maximum Runtime(sec): %f" % max(execute_time))
    print("Minimum Runtime(sec): %f" % min(execute_time))
