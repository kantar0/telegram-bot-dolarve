import pymongo # pymongo library
from pymongo.errors import OperationFailure 
import os # os library
import settings # settings.py
from log_func import log_info, log_error, log_debug, log_warning # log_func.py
# start_env()
settings.start_env()

def start_connection():
    client = pymongo.MongoClient(os.getenv('MONGODB_URL'))
    return client

def check_connection(client_mongodb):
    try:
        client_mongodb.admin.command('ismaster')
        log_info('MongoDB connection successful')
        return True
    except OperationFailure as err:
        log_error('MongoDB connection failed. Error : ' + str(err))
        return False
        
def insert_record(record, client_mongodb):
    db = client_mongodb["database"]
    collection = db["dolarve"]
    collection.insert_one(record)
    return True
