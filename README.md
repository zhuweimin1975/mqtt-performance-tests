# mqtt-performance-tests

### ENVIORMENT 
```
$pip install paho-mqtt
```

### USAGE example
#### 1. execute time of connect
```
python mqtt_connect_runtime_test.py -s local -c 100

argument : {'connections': '100', 'server': 'localhost'}
Creating 100 consumers
Average Runtime(sec): 0.453670
Maximum Runtime(sec): 1.217335
Minimum Runtime(sec): 0.040922
```

