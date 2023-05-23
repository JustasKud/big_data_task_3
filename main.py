from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient("mongodb://127.0.0.1:27117,127.0.0.1:27118")
    db = client.MainDatabase
    collection = db.MainCollection
    
    data = [
		{"name": "John", "age": 30},
		{"name": "Jane", "age": 25},
		{"name": "Bob", "age": 40}
	]
    
    collection.insert_many(data)
    
    for document in collection.find():
        print(document)