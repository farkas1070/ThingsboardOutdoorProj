
import paho.mqtt.client as mqtt
import time
import random
from threading import Thread

def on_connect(client, userdata, flags, rc):
    print("Connected to the broker with result code: "+str(rc))
    # Subscribe to the topics where ThingsBoard will send updates
    client.subscribe("v1/devices/me/attributes/temperature_knob")

def on_message(client, userdata, msg):
    global temperature
    print(msg.topic + " " + str(msg.payload))
    
    # Update the temperature variable with the new value from the knob
    temperature = float(msg.payload)

    print("Temperature updated: {}".format(temperature))
 
def send_data(device_token):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(device_token, "")
    client.connect("127.0.0.1", 1883, 60)
    client.loop_start()

    while True:
        # Simulate data based on device token
        if device_token == device_tokens[0]:
            # Device 1: Temperature only
            temperature = 38
            payload = '{{"temperature": {0}}}'.format(temperature)
        elif device_token == device_tokens[1]:
            # Device 2: Humidity only
            humidity = 2
            payload = '{{"humidity": {0}}}'.format(humidity)
        elif device_token == device_tokens[2]:
            # Device 3: Rainfall only
            rainfall = 2
            payload = '{{"rainfall": {0}}}'.format(rainfall)
        elif device_token == device_tokens[3]:
            # Device 3: Rainfall only
            speed = 40
            payload = '{{"speed": {0}}}'.format(speed)
        else:
            # Default case: Send temperature, humidity, and rainfall
            temperature = random.uniform(20, 30)
            humidity = random.uniform(40, 60)
            rainfall = random.uniform(0, 20)
            payload = '{{"temperature": {0}, "humidity": {1}, "rainfall": {2}, "speed": {3}}}'.format(temperature, humidity, rainfall,speed)

        # Publish data to ThingsBoard
        client.publish("v1/devices/me/telemetry", payload)

        print("Data sent for device {}: {}".format(device_token, payload))

        time.sleep(5)  # Adjust the sleep duration based on your requirements

# Replace these with your actual device access tokens
device_tokens = ["es5pFCpAKJTpmloy4dIv", "033RVbhTQeiYkhTYT7O6","1d117ygtryf9n6xw4d3q","s1D1PD5oCt3LG5tzbMFD"]

# Create a thread for each device
threads = []
for token in device_tokens:
    thread = Thread(target=send_data, args=(token,))
    threads.append(thread)

# Start all threads
for thread in threads:
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
