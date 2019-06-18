#!/usr/bin/env python
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Copyright 2016 Confluent Inc.
# Licensed under the MIT License.
# Licensed under the Apache License, Version 2.0
#
# Original Confluent sample modified for use with Azure Event Hubs for Apache Kafka Ecosystems

import time
from confluent_kafka import Producer
import sys
import json
import random

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s <topic>\n' % sys.argv[0])
        sys.exit(1)
    topic = sys.argv[1]

    # Producer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    # See https://github.com/edenhill/librdkafka/wiki/Using-SSL-with-librdkafka#prerequisites for SSL issues
    conf = {
        'bootstrap.servers': '<name>.servicebus.windows.net:9093', #replace
        'security.protocol': 'SASL_SSL',
        'ssl.ca.location': '/usr/lib/ssl/certs/ca-certificates.crt',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': '$ConnectionString',
        'sasl.password': '<connection-string>',          #replace
        'client.id': 'python-example-producer'
    }

    # Create Producer instance
    p = Producer(**conf)


    def delivery_callback(err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message delivered to %s [%d] @\n' % (msg.value(), msg.partition()))

    i = 1
    # Write 1-100 to topic
    while 1:
        try:
            if i % 120 == 0:
                data = { 
                    'sensor': random.uniform(0.2,0.21),
                    'tag' : 'TagEDA'
                }
            else:
                data = { 
                        'sensor': random.uniform(0.9,1.1),
                        'tag' : 'TagEDA'
                    }

            p.produce(topic, json.dumps(data), callback=delivery_callback)
            time.sleep(1)
            i += 1
        except BufferError as e:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(p))
        p.poll(0)

    # Wait until all messages have been delivered
    sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
    p.flush()
