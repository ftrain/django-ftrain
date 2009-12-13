#!/bin/bash

#run solr 

pushd .

PWD=/home/ford/proj/sites/bin/solr/jetty/
cd $PWD
java -jar $PWD/start.jar &
popd 