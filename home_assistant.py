#!/usr/bin/env python3
import pika, sys, os, traceback
from generated import measure_pb2

last_measures = {}

def callback_temp(ch, method, properties, body):
    message = measure_pb2.Measure()
    message.ParseFromString(body)
    last_measures['temp'] = message.value
    print('temp:{}'.format(last_measures['temp']))

def callback_light(ch, method, properties, body):
    message = measure_pb2.Measure()
    message.ParseFromString(body)
    last_measures['light'] = message.value
    print('light:{}'.format(last_measures['light']))

def callback_hum(ch, method, properties, body):
    message = measure_pb2.Measure()
    message.ParseFromString(body)
    last_measures['hum'] = message.value
    print('hum:{}'.format(last_measures['hum']))

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