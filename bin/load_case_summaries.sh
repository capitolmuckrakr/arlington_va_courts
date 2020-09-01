#!/bin/bash
CSV_PATH=$1
cat $CSV_PATH | psql --host=${ENDPOINT} --port=5432 --username=alex --dbname=arlingtoncourts -c "\copy cases_summary (courtname,case_num,defendant,complainant,hearingdate,amended_charge,charge,result) FROM '$CSV_PATH' WITH DELIMITER E'\t' NULL '' CSV HEADER "
