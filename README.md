# Task 3

## Installation

```bash
docker-compose up -d
```

```bash
docker-compose exec configsvr01 sh -c "mongosh < /scripts/init-configserver.js"
```

```bash
docker-compose exec shard01-a sh -c "mongosh < /scripts/init-shard01.js"
```

```bash
docker-compose exec shard02-a sh -c "mongosh < /scripts/init-shard02.js"
```

```bash
docker-compose exec shard03-a sh -c "mongosh < /scripts/init-shard03.js"
```

```bash
docker-compose exec router01 sh -c "mongosh < /scripts/init-router.js"
```

```bash
docker-compose exec router01 mongosh --port 27017
```

```bash
sh.enableSharding("MainDatabase")
```

```bash
db.adminCommand( { shardCollection: "MainDatabase.MainCollection", key: { oemNumber: "hashed", zipCode: 1, supplierId: 1 } } )
```

```bash
python main.py
```
