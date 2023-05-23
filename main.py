from pymongo import MongoClient
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def insert_data(chunk):
    client = MongoClient("mongodb://127.0.0.1:27117,127.0.0.1:27118")
    db = client.MainDatabase
    collection = db.MainCollection
    collection.insert_many(chunk.to_dict('records'))
    client.close()


if __name__ == "__main__":
    PATH = "./data/aisdk-2023-05-01.csv"
    CHUNK_SIZE = 1000
    MAX_ROWS = 300_000
    
    data = list(pd.read_csv(PATH, chunksize=CHUNK_SIZE, nrows=MAX_ROWS))
    
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = {executor.submit(insert_data, chunk): chunk for chunk in data}
        for future in tqdm(as_completed(futures), total=len(data)):
            pass