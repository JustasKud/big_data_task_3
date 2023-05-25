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

Initialize a virtual environment if not initialized (Windows):

```bash
python -m virtualenv venv
source ./venv/Scripts/activate
```

Initialize a virtual environment if not initialized (Mac/Linux):

```bash
python -m virtualenv venv
source ./venv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

I assume the data is stored in a "data" folder in root. To insert data, run this command:

```bash
python main.py insert
```

To filter data, run this command:

```bash
python main.py filter
```

Make sure to have a directory to store created figures:

```bash
mkdir figs
```

To perform calculations=, run this command:

```bash
python main.py calculate
```
