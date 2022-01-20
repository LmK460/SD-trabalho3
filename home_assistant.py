#!/usr/bin/env python3
import pika, sys, os, traceback, grpc

import measure_pb2
from air_cond_pb2 import AirCondState
import air_cond_pb2_grpc
from lamp_pb2 import LampState
import lamp_pb2_grpc
from watering_can_pb2 import WateringCanState
import watering_can_pb2_grpc

channelAC = grpc.insecure_channel('localhost:50051')
stub_aircond = air_cond_pb2_grpc.AirCondStub(channelAC)
channelL = grpc.insecure_channel('localhost:50052')
stub_lamp = lamp_pb2_grpc.LampStub(channelL)
channelWC = grpc.insecure_channel('localhost:50053')
stub_water_can = watering_can_pb2_grpc.WateringCanStub(channelWC)

last_measures = {}

def callback_temp(ch, method, properties, body):
    message = measure_pb2.Measure()
    message.ParseFromString(body)
    value = message.value
    last_measures['temp'] = value
    print('temp:{}'.format(last_measures['temp']))

    airCondState = AirCondState()
    if value<25: airCondState.state = AirCondState.WEAK
    elif value<32: airCondState.state = AirCondState.MEDIUM
    else: airCondState.state = AirCondState.STRONG

    stub_aircond.setState(airCondState)


def callback_light(ch, method, properties, body):
    message = measure_pb2.Measure()
    message.ParseFromString(body)
    value = message.value
    last_measures['light'] = value
    print('light:{}'.format(last_measures['light']))

    lampState = LampState()
    if value<15:
        lampState.state = LampState.ON
        stub_lamp.setState(lampState)
    elif value>25:
        lampState.state = LampState.OFF
        stub_lamp.setState(lampState)
    

def callback_hum(ch, method, properties, body):
    message = measure_pb2.Measure()
    message.ParseFromString(body)
    value = message.value
    last_measures['hum'] = value
    print('hum:{}'.format(last_measures['hum']))

    wateringCanState = WateringCanState()
    if value<55:
        wateringCanState.state = WateringCanState.ON
        stub_lamp.setState(wateringCanState)
    elif value>70:
        wateringCanState.state = WateringCanState.OFF
        stub_lamp.setState(wateringCanState)

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='measures', exchange_type='direct')

    channel.queue_declare(queue='temp_queue', exclusive=True)
    channel.queue_bind(exchange='measures', queue='temp_queue', routing_key='temp')
    channel.basic_consume(queue='temp_queue', on_message_callback=callback_temp, auto_ack=True)

    channel.queue_declare(queue='light_queue', exclusive=True)
    channel.queue_bind(exchange='measures', queue='light_queue', routing_key='light')
    channel.basic_consume(queue='light_queue', on_message_callback=callback_light, auto_ack=True)

    channel.queue_declare(queue='hum_queue', exclusive=True)
    channel.queue_bind(exchange='measures', queue='hum_queue', routing_key='hum')
    channel.basic_consume(queue='hum_queue', on_message_callback=callback_hum, auto_ack=True)
    
    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel.start_consuming()

try:
    main()
except KeyboardInterrupt:
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
except Exception:
    traceback.print_exc()