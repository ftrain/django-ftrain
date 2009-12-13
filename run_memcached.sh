#!/bin/bash

#run a 256meg instance of memcached on localhost, on port 11211
memcached -d -m 256 -l 127.0.0.1 -p 11211