#!/bin/bash

GIT=/home/ford/local/bin/git
BACKUP_DIR=/home/ford/sites/backup
PYTHON_DIR=/home/ford/sites/ftrain
cd $PYTHON_DIR
#./manage.py dumpdata --indent=1 > $BACKUP_DIR/database.json
pg_dump ftrain > $BACKUP_DIR/postgres.sql
cd $BACKUP_DIR
#$GIT add database.json
$GIT add postgres.sql
$GIT commit -m"Automatic database backup"
$GIT push origin master
