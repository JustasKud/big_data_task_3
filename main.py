from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.8.2")
    db = client.test
    collection = db.testCollection
    for document in collection.find():
        print(document)