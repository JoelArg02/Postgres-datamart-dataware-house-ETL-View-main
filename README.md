# Postgres-datamart-dataware-house-ETL-View-main

## ¿El por qué del proyecto? 

Se creo este proyecto y repositorio como parte de la evaluacion conjunta del primer parcial de base de datos avanzada

## Necesario para iniciar

Necesitaras docker para poder comenzar con este proyecto

docker network create nodes-master

# Nodo Maestro 1
docker run --name master-1 -e POSTGRES_PASSWORD=password -d postgres

### Conectar a red

docker network connect nodes-master master-1

# Nodo Maestro 2
docker run --name master-2 -e POSTGRES_PASSWORD=password -d postgres

### Conectar a red
docker network connect nodes-master master-2

## Configuracion nodo master 1

ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_wal_senders = 3;
ALTER SYSTEM SET max_replication_slots = 3;
ALTER SYSTEM SET listen_addresses = '

### Reinicia el nodo 

docker restart master-1

## Configuracion NODO master 2

ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_wal_senders = 3;
ALTER SYSTEM SET max_replication_slots = 3;
ALTER SYSTEM SET listen_addresses = '*';

### Reinicia el nodo 

docker restart master-2

# Configuracion Maestro a Maestro


´´´
SELECT pg_create_physical_replication_slot('replication_slot1');
SELECT pg_create_physical_replication_slot('replication_slot2');

SELECT pg_start_backup('base_backup');
rsync -a /var/lib/postgresql/data/ postgres-master2:/var/lib/postgresql/data/
SELECT pg_stop_backup();

´´´

## Configurar el Archivo recovery.conf en el Nodo Maestro 2:

docker exec -it postgres-master2 bash

# Crear el archivo recovery.conf
echo "standby_mode = 'on'" >> /var/lib/postgresql/data/recovery.conf
echo "primary_conninfo = 'host=postgres-master1 port=5432 user=postgres password=password'" >> /var/lib/postgresql/data/recovery.conf

### Reinicia el nodo 

docker restart master-2
