#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


@click.command()
@click.option('--pg_user', help='PostgreSQL username', required=True)
@click.option('--pg_password', help='PostgreSQL password', required=True)
@click.option('--pg_host', help='PostgreSQL host', required=True)
@click.option('--pg_db', help='PostgreSQL database name', required=True)
@click.option('--year', help='Year of the data to ingest', type=int, required=True)
@click.option('--month', help='Month of the data to ingest', type=int, required=True)
@click.option('--chunksize', help='Number of rows to process at a time', type=int, default=100000)
@click.option('--target_table', help='Name of the target table in PostgreSQL', required=True)
def run(pg_user, pg_password, pg_host, pg_db, year, month, chunksize , target_table):
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:5432/{pg_db}')

    df_iter = pd.read_csv(
        url, 
        dtype = dtype,
        parse_dates= parse_dates,
        iterator=True,
        chunksize = chunksize,
    )
    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(n=0).to_sql(
                name=target_table, 
                con=engine, 
                if_exists='replace'
            )
            first = False  
        df_chunk.to_sql(
            name=target_table, 
            con=engine, 
            if_exists='append'
        )


if __name__ == '__main__':
    run()


