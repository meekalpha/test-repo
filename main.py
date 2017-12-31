#!/bin/python3

import requests
from datasource import EcusisSource
source = EcusisSource(requests.Session())

f = open('output/out.html', 'w')
f.write(source.GetHtml())
f.close()
