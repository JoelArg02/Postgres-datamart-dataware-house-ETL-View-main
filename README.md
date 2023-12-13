# Postgres-datamart-dataware-house-ETL-View-main

## ¿El por qué del proyecto? 

Se creo este proyecto y repositorio como parte de la evaluacion conjunta del primer parcial de base de datos avanzada

## Necesario para iniciar

Necesitaras docker para poder comenzar con este proyecto
# Descargar imagen postgres

```
docker pull postgres:latest
```

# Crear una red
```
docker network create nodes-master
```


# Nodo Maestro 1
```
docker run --name master-1 -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres
```
### Conectar a red
```
docker network connect nodos-master master-1
```
# Nodo Maestro 2
```
docker run --name master-2 -p 5433:5432 -e POSTGRES_PASSWORD=password -d postgres
```
### Conectar a red
```
docker network connect nodos-master master-2
```

## Configuracion nodo master 1

```sql
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_wal_senders = 3;
ALTER SYSTEM SET max_replication_slots = 3;
ALTER SYSTEM SET listen_addresses = '
```
### Reinicia el nodo 

```
docker restart master-1
```

## Configuracion NODO master 2

```sql
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_wal_senders = 3;
ALTER SYSTEM SET max_replication_slots = 3;
ALTER SYSTEM SET listen_addresses = '*';
```
### Reinicia el nodo 

```
docker restart master-2
```

# Configuracion Maestro a Maestro


```sql
SELECT pg_create_physical_replication_slot('replication_slot1');
SELECT pg_create_physical_replication_slot('replication_slot2');
```

## Reinicas el MASTER 1
```
SELECT pg_create_logical_replication_slot('replication_slot1', 'pgoutput');
```

## Reinicas el MASTER 2
```
SELECT pg_create_logical_replication_slot('replication_slot2', 'pgoutput');
```
docker restart maestro-1 maestro-2

