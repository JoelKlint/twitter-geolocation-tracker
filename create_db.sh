#!/bin/bash

# This script setups the database in which all twitter data will be saved

createdb twitter-geo
psql -d twitter-geo -f set_up_database.sql