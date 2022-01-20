#!/usr/bin/env python3
import pika, random, sys, os, traceback, time

import measure_pb2

class Measurer:
    def __init__(self, type, min_value, max_value, time_delay) -> None:
        self.type = type
        self.min_value = min_value
        self.max_value = max_value
        self.time_delay = time_delay

    def start(self) -> None:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='measures', exchange_type='direct')

        try:
            while True:
                measure = measure_pb2.Measure()

                measure.value = random.randint(self.min_value, self.max_value)
                message = measure.SerializeToString()
                
                channel.basic_publish(exchange='measures', routing_key=self.type, body=message)
                print(" [x] Sent %r" % message)

                time.sleep(self.time_delay)
        except KeyboardInterrupt:
            connection.close()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        except Exception:
            connection.close()
            traceback.print_exc()
