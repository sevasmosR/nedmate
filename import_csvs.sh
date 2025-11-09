#!/bin/bash

# PostgreSQL connection string
PG_CONN="host=nedmate-ai-db-001.postgres.database.azure.com dbname=postgres user=nedmateadmin password='SecretP@ssword1' sslmode=require"

# Folder containing CSV files
CSV_DIR="/home/respect/Downloads/Nedbank Hackathon Final"

# Loop through all CSV files in the folder and subfolders
find "$CSV_DIR" -type f -name "*.csv" | while read -r csv_file; do
    echo "Importing $csv_file ..."
    psql "$PG_CONN" -c "\copy transactions(date, account, description, debit_fc, credit_fc, balance_fc, debit_zar, credit_zar, balance_zar, category, reference, currency, fx_to_zar_at_txn, latitude, longitude, counterparty) FROM '$csv_file' DELIMITER ',' CSV HEADER"
done

echo "All CSV files imported!"
