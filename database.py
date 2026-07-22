from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import MONGODB_URI

class DBHelper:

    def __init__(self, db_name='TR2026'):
        
        self.client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        print('[DBHelper] Connection Created')



    def select_collection(self, collection_name='users'):
        self.collection = self.db[collection_name]
        print('[DBHelper] Collection Selected:"', collection_name)



    def save(self, document):
       inserted_id = self.collection.insert_one(document)
       print('[DBHelper] Document Saved. Id is:', inserted_id)



    def retrieve(self,condition=None):
        result=self.collection.find(condition)
        print('[DBHelper] Document Retrieved. \nId is:', result)

        for document in result:
            print(document)

        return result

    


    def update(self, condition=None, document_to_update=None):
        result = self.collection.update_one(
            condition,
            {
                '$set': document_to_update
            }
        )
        print('[DBHelper] Document Updated\n', result)