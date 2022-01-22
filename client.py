#!/usr/bin/env python3
from base64 import decode
from turtle import Turtle
from typing import Dict
import pika, random, sys, os, traceback, time
import uuid

import measure_pb2

class ApiRpcClientPost:
    def __init__(self, name,estado) -> None:
        self.name = name
        self.state = estado
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(auto_delete=True, queue='rpc', exclusive=False)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            #message.ParseFromString(body)
            self.response = body.decode('utf8')
            

    def call(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        message = []
        message.append(self.name)
        message.append(self.state)
        self.channel.basic_publish(
            exchange='measures',
            routing_key='rpc-p',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(message) )
        while self.response is None:
            self.connection.process_data_events()
        self.channel.queue_delete(queue='rpc')
        self.channel.queue_delete(queue='rpc-queue')
        return str(self.response)


        