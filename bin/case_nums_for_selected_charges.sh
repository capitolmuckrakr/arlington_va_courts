#!/bin/bash
export SQL_DIR="${HOME}/scripts/arlington_va_courts/bin/sql/"
psql --host=${ENDPOINT} --port=5432 --username=alex --dbname=arlingtoncourts -f ${SQL_DIR}case_nums_for_selected_charges.sql