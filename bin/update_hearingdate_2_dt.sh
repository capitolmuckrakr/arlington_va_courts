#!/bin/bash
export SQL_DIR="${HOME}/scripts/arlington_va_courts/bin/sql/"
psql --host=${ENDPOINT} --port=5432 --username=alex --dbname=arlingtoncourts -f ${SQL_DIR}update_hearingdate_2_dt.sql