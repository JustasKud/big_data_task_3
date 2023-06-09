from pymongo import MongoClient
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing as mp
from tqdm import tqdm
import sys
from datetime import datetime
import matplotlib.pyplot as plt


def generate_histogram(mmsi):
	client = MongoClient("mongodb://127.0.0.1:27117,127.0.0.1:27118")
	db = client.shipDB
	collection = db.filtered_ships

	pipeline = [
		{"$match": {
			"MMSI": mmsi["_id"]
		}}
	]

	data = list(collection.aggregate(pipeline))
	client.close()
	
	sorted_data = sorted(data, key=lambda d: d["# Timestamp"])
	previous_timestamp = None
	delta_t_values = []

	for document in sorted_data:
		timestamp_str = document['# Timestamp']
		timestamp = datetime.strptime(timestamp_str, '%d/%m/%Y %H:%M:%S')
		if previous_timestamp is not None:
			delta_t = (timestamp - previous_timestamp).total_seconds() * 1000
			delta_t_values.append(delta_t)
			print(f"Vessel: {document['MMSI']}, Delta t: {delta_t} ms")

		previous_timestamp = timestamp
	
	plt.hist(delta_t_values, bins=10)
	plt.xlabel('Delta t (milliseconds)')
	plt.ylabel('Frequency')
	plt.title(f'Histogram of Delta t of vessel {mmsi["_id"]}')
	plt.savefig(f'./figs/delta_t_histogram_of_{mmsi["_id"]}.png')
	plt.close()

def insert_filtered_data(mmsi):
	client = MongoClient("mongodb://127.0.0.1:27117,127.0.0.1:27118")
	db = client.shipDB
	
	collection = db.ships
	new_collection = db.filtered_ships
	
	pipeline = [
		{"$match": {
			"MMSI": mmsi["_id"], 
			"Navigational status": {"$ne": float("nan")}, 
			"Latitude": {"$ne": float("nan")}, 
			"Longitude": {"$ne": float("nan")}, 
			"ROT": {"$ne": float("nan")}, 
			"SOG": {"$ne": float("nan")}, 
			"COG": {"$ne": float("nan")}, 
			"Heading": {"$ne": float("nan")},
		}}
	]
	filtered_data = list(collection.aggregate(pipeline))
	if len(filtered_data) >= 100:
		new_collection.insert_many(filtered_data)
	client.close()


def insert_data(chunk):
	client = MongoClient("mongodb://127.0.0.1:27117,127.0.0.1:27118")
	db = client.shipDB
	collection = db.ships
	collection.insert_many(chunk.to_dict('records'))
	client.close()


def task_2():
	PATH = "./data/aisdk-2023-05-01.csv"
	CHUNK_SIZE = 1000
	MAX_ROWS = 1_000_000
	MAX_WORKERS = 16
	
	data = list(pd.read_csv(PATH, chunksize=CHUNK_SIZE, nrows=MAX_ROWS))
	
	with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
		futures = {executor.submit(insert_data, chunk): chunk for chunk in data}
		for future in tqdm(as_completed(futures), total=len(data)):
			pass


def task_3():
	MAX_WORKERS = 16
	client = MongoClient("mongodb://127.0.0.1:27117,127.0.0.1:27118")
	db = client.shipDB
	collection = db.ships
	collection.create_index([("MMSI", 1)])
	
	count_pipeline = [
		{"$group": {"_id": "$MMSI", "count": {"$sum": 1}}},
		{"$match": {
			"count": {"$gt": 100},
		}}
	]
	
	over_100_data = list(collection.aggregate(count_pipeline))
	client.close()
	
	with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
		futures = {executor.submit(insert_filtered_data, chunk): chunk for chunk in over_100_data}
		for future in tqdm(as_completed(futures), total=len(over_100_data)):
			pass


def task_4():
	client = MongoClient("mongodb://127.0.0.1:27117,127.0.0.1:27118")
	db = client.shipDB
	collection = db.filtered_ships
	collection.create_index([("MMSI", 1)])
	
	pipeline = [
		{"$group": {"_id": "$MMSI", "count": {"$sum": 1}}},
	]
	
	data = list(collection.aggregate(pipeline))
	client.close()
	
	MAX_WORKERS = 14
	with mp.Pool(MAX_WORKERS) as pool:
		pool.map(generate_histogram, data)


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("You need to add an argument 'insert','filter', or 'calculate'.")
	elif sys.argv[1] == "insert":
		task_2()
	elif sys.argv[1] == "filter":
		task_3()
	elif sys.argv[1] == "calculate":
		task_4()
	else:
		print("Incorrect argument. You need to use 'insert','filter', or 'calculate'.")