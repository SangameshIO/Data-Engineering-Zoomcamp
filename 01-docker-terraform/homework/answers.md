## question 1
Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.
What's the version of pip in the image?

commands to run 
docker run -it --rm --entrypoint=bash python:3.13-slim
then pip --version 
pip -V
pip 26.0.1 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
ans : 26.0.1

## question 2
Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data


## answer 
all services in docker compose be on same network so they can connect via container name or service name and pgadmin can connect to postgres database using name postgres and port 5432 
and also servcie name and port 
db:5432

and port : 5433:5432 
is for localhost to container and not container to container 
so localhost:5433 will establish connection between localhost and postgres
it is better to use ervice name in docker compose rather than container name 


## question 3 
For the trips in january 2021 (lpep_pickup_datetime between '2021-01-01' and '2021-02-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?
## answer
select * from yellow_taxi_trips_2021_1
where tpep_pickup_datetime >= '2021-01-01' and
tpep_pickup_datetime < '2021-02-01' and trip_distance < 1;

## question 4
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).
## answer
select cast(tpep_pickup_datetime as date) as day   from yellow_taxi_trips_2021_1
where trip_distance = (select max(trip_distance) from yellow_taxi_trips_2021_1
where  trip_distance < 100)

## question 7. Terraform Workflow
Which of the following sequences, respectively, describes the workflow for:

Downloading the provider plugins and setting up backend,
Generating proposed changes and auto-executing the plan
Remove all resources managed by terraform`


terraform init, terraform apply -auto-approve, terraform destroy
terraform init : get provider plugin 
terraform apply 
    will plan and execute the plan since we have use -auto -approve 
terraform  destroy : will destroy resources created using terraform apply internallly 
it check state file and plans on what steps to take for destroying resource 





