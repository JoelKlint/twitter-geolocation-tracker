#!/bin/bash

# This script prints the disc usage of the database that this project uses

psql -d twitter-geo -f $(dirname $0)/database_disc_size_query.sql