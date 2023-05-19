docker-compose up -d

docker exec -it mongo1 mongosh --eval 'rs.initiate({_id: "my-replica-set", members: [{_id: 0, host: "mongo1:27017", priority: 1}, {_id: 1, host: "mongo2:27017", priority: 0}, {_id: 2, host: "mongo3:27017", priority: 0}]});'

docker exec -it mongo1 mongosh --eval "rs.status()"

docker exec -it mongo1 mongosh

use myDatabase
db.createCollection("myCollection")
db.myCollection.insert({name: "John Doe", age: 30})

python main.py
