import os
import time
import json
import paho.mqtt.client as mqtt
from sensor import SENSOR_TYPES

BROKER_HOST = os.environ.get("MQTT_BROKER", "mosquitto")
BROKER_PORT = int(os.environ.get("MQTT_PORT", "1883"))
SENSOR_TYPE = os.environ.get("SENSOR_TYPE", "temperature")
SENSOR_NAME = os.environ.get("SENSOR_NAME", "sensor1")
INTERVAL = float(os.environ.get("INTERVAL", "5"))
FORMULA_TYPE = os.environ.get("FORMULA_TYPE", "random")
TOPIC_FORMAT = os.environ.get("TOPIC_FORMAT", "value")

sensor_class = SENSOR_TYPES.get(SENSOR_TYPE, SENSOR_TYPES["temperature"])
sensor = sensor_class(name=SENSOR_NAME, formula=FORMULA_TYPE)

client = mqtt.Client()

def on_connect(c, userdata, flags, rc):
    print(f"Connected to {BROKER_HOST}:{BROKER_PORT} (rc={rc})")

client.on_connect = on_connect

while True:
    try:
        client.connect(BROKER_HOST, BROKER_PORT, 60)
        break
    except Exception as e:
        print(f"Broker not ready: {e}, retry in 3s...")
        time.sleep(3)

client.loop_start()

topic_base = f"sensors/{SENSOR_TYPE}"

while True:
    value = sensor.read()
    if TOPIC_FORMAT == "json":
        topic = topic_base
        payload = json.dumps({"name": SENSOR_NAME, "value": value})
    else:
        topic = f"{topic_base}/{SENSOR_NAME}"
        payload = str(value)

    client.publish(topic, payload)
    print(f"[{SENSOR_NAME}] {topic} -> {payload}")
    time.sleep(INTERVAL)
