#!/usr/bin/env python3
import pika, sys, os, traceback, grpc

from flask import Flask, jsonify
from flask import render_template
from flask import request
import socket

import json

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

#Rotas de comunicações

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/temperatura', methods=['GET'])
def Temperature():

    result = last_measures['temp']
    print(result)
    
    return jsonify(result)


@app.route('/humidade', methods=['GET'])
def Humidity():

    result = last_measures['hum']
    print(result)
    
    return jsonify(result)

@app.route('/luz', methods=['GET'])
def Luz():

    result = last_measures['light']
    
    return jsonify('A luz encontra-se desligada')

@app.route('/ligarlampada', methods=['POST'])
def LigarLampada():

    stub_lamp.setState(1)
    result  = stub_lamp.getState
    return jsonify('Lampada Ligada')

@app.route('/desligarlampada', methods=['POST'])
def DesligarLampada():

    stub_aircond.setState(0)
    result  = stub_lamp.getState
    return jsonify('Lampada Desligada')


@app.route('/ligarArcondicionado', methods=['POST'])
def LigarArcondicionado():

    stub_aircond.setState(1)
    result  = stub_aircond.getState
    return jsonify(result)

@app.route('/desligarArcondicionado', methods=['POST'])
def DesligarArcondicionado():

    stub_aircond.setState(0)
    result  = stub_aircond.getState
    return jsonify(result)

@app.route('/ligarRegador', methods=['POST'])
def LigarRegador():

    stub_water_can.setState(1)
    result  = stub_water_can.getState
    return jsonify(result)


@app.route('/desligarRegador', methods=['POST'])
def DesligarRegador():

    stub_water_can.setState(0)
    result  = stub_water_can.getState
    return jsonify(result)

#fim das rotas




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

    app.run(host = '0.0.0.0',port=8080, debug=True)

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