#!/usr/bin/env python3
from base64 import decode, encode
from encodings import utf_8
from pickle import TRUE
import threading
from urllib import response
from flask import jsonify
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


last_measures = [1,2,3]



def callback_temp(ch, method, properties, body):
    message = measure_pb2.Measure()
    message.ParseFromString(body)
    value = message.value
    print('value:{}'.format(value))
    last_measures[0] = value
    print('temp:{}'.format(last_measures[0]))
    '''
    airCondState = AirCondState()
    airCondState.state = AirCondState.STRONG
    stub_aircond.setState(airCondState)'''


    ''' airCondState = AirCondState()
    if value<25: airCondState.state = AirCondState.WEAK
    elif value<32: airCondState.state = AirCondState.MEDIUM
    else: airCondState.state = AirCondState.STRONG

    stub_aircond.setState(airCondState)'''


def callback_light(ch, method, properties, body):
    message = measure_pb2.Measure()
    message.ParseFromString(body)
    value = message.value
    last_measures[1] = value
    print('light:{}'.format(last_measures[1]))

    '''lampState = LampState()
    if value<15:
        lampState.state = LampState.ON
        stub_lamp.setState(lampState)
    elif value>25:
        lampState.state = LampState.OFF
        stub_lamp.setState(lampState)'''
    

def callback_hum(ch, method, properties, body):
    message = measure_pb2.Measure()
    message.ParseFromString(body)
    value = message.value
    last_measures[2] = value
    print('hum:{}'.format(last_measures[2]))
    '''wateringCanState = WateringCanState()
    if value<55:
        wateringCanState.state = WateringCanState.ON
        stub_lamp.setState(wateringCanState)
    elif value>70:
        wateringCanState.state = WateringCanState.OFF
        stub_lamp.setState(wateringCanState)'''


def on_post(ch, method, props, body):
    aux=body.decode('utf_8')
    
    aux = aux.replace("['","").replace("'","").replace("'","").replace("'","").replace("]","").replace(" ","")
    aux = list(aux.split(","))
    print('Post')
    print(aux)
    
    if(aux[1] =='Air'):
        airCondState = AirCondState()
        airCondState.state = int(aux[0])
        stub_aircond.setState(airCondState)
        response = stub_aircond.getState(airCondState)
    elif (aux[1] =='Lamp'):
        lampState = LampState()
        lampState.state = int(aux[0])
        stub_lamp.setState(lampState)
        response = stub_lamp.getState(lampState)
    elif (aux[1] == 'Wat'):
        wateringcanState = WateringCanState()
        wateringcanState.state = int(aux[0])
        stub_water_can.setState(wateringcanState)
        response = stub_water_can.getState(wateringcanState)
    else: response = 'Valor invalido'
    
    ch.basic_publish(exchange='',
                     routing_key='rpc',
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)






def on_request(ch, method, props, body):
    
    print(body)
    aux = body.decode('utf8')
    print(aux)
    if(aux == 'temp'):
        response = last_measures[0]
    elif(aux=='hum'):
        response = last_measures[1]
    elif(aux=='light'):
        response = last_measures[2]
    elif(aux=='Air'):
        airCondState = AirCondState()
        response = stub_aircond.getState(airCondState)
    elif(aux=='Lamp'):
        lampState = LampState()
        response = stub_lamp.getState(lampState)
    elif(aux=='Wat'):
        wateringcanState = WateringCanState()
        response = stub_water_can.getState(wateringcanState)
    else: response = 'Valor invalido'
    ch.basic_publish(exchange='',
                     routing_key='rpc',
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    


def main():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='measures', exchange_type='direct')

    #fila da API
    channel.queue_declare(auto_delete=True,queue='rpc_queue', exclusive=True)
    channel.queue_bind(exchange='measures', queue='rpc_queue', routing_key='rpc')
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

    #fila da API
    channel.queue_declare(auto_delete=True,queue='rpc_queue_post', exclusive=True)
    channel.queue_bind(exchange='measures', queue='rpc_queue_post', routing_key='rpc-p')
    channel.basic_consume(queue='rpc_queue_post', on_message_callback=on_post)

    

    channel.queue_declare(queue='temp_queue', exclusive=False)
    channel.queue_bind(exchange='measures', queue='temp_queue', routing_key='temp')
    channel.basic_consume(queue='temp_queue', on_message_callback=callback_temp)

    channel.queue_declare(queue='light_queue', exclusive=False)
    channel.queue_bind(exchange='measures', queue='light_queue', routing_key='light')
    channel.basic_consume(queue='light_queue', on_message_callback=callback_light)

    channel.queue_declare(queue='hum_queue', exclusive=False)
    channel.queue_bind(exchange='measures', queue='hum_queue', routing_key='hum')
    channel.basic_consume(queue='hum_queue', on_message_callback=callback_hum)
    
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