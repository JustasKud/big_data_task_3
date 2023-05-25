# Task 3

## Installation

Requirements:

- Docker installed.

Start up docker:

```bash
docker-compose up -d
```

Initialize the config servers:

```bash
docker-compose exec configsvr01 sh -c "mongosh < /scripts/init-configserver.js"
```

Initialize the shards:

```bash
docker-compose exec shard01-a sh -c "mongosh < /scripts/init-shard01.js"
```

```bash
docker-compose exec shard02-a sh -c "mongosh < /scripts/init-shard02.js"
```

```bash
docker-compose exec shard03-a sh -c "mongosh < /scripts/init-shard03.js"
```

Initialize the routers:

```bash
docker-compose exec router01 sh -c "mongosh < /scripts/init-router.js"
```

Access the primary router:

```bash
docker-compose exec router01 mongosh --port 27017
```

Enable sharding on a specified database:

```bash
sh.enableSharding("shipDB")
```

Initialize ships and filtered_ships.

```bash
db.adminCommand( { shardCollection: "database.ships", key: { oemNumber: "hashed", zipCode: 1, supplierId: 1 } } )
```

```bash
db.adminCommand( { shardCollection: "database.filtered_ships", key: { oemNumber: "hashed", zipCode: 1, supplierId: 1 } } )
```

Exit the primary router:

```bash
exit
```

## Dev environment

Requirements:

- virtualenv package
- windows 10

Initialize a virtual environment if not initialized:

```bash
python -m virtualenv venv
source ./venv/Scripts/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

To insert data, run this command:

```bash
python main.py insert
```

To filter data, run this command:

```bash
python main.py filter
```

To perform calculations=, run this command:

```bash
python main.py calculate
```
