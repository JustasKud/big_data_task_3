docker-compose up -d

docker exec -it mongo1 mongosh --eval "rs.initiate({
\_id: \"myReplicaSet\",
members: [
{_id: 0, host: \"mongo1\"},
{_id: 1, host: \"mongo2\"},
{_id: 2, host: \"mongo3\"}
]
})"

docker exec -it mongo1 mongosh --eval "rs.status()"

docker exec -it mongo1 mongosh

use myDatabase
db.createCollection("myCollection")
db.myCollection.insert({name: "John Doe", age: 30})

docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongo1
