#!/bin/bash

# This script setups the database in which all twitter data will be saved

createdb twitter-geo
psql -d twitter-geo -f $(dirname $0)/create_tables.sql