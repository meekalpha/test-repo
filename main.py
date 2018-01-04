#!/bin/python3

import requests
from datasource import EcusisSource

source = EcusisSource(requests.Session())
time_slots = source.get_time_slots();

for t in time_slots:
    print(t)
