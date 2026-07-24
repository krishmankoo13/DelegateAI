from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import MONGODB_URI,DB_NAME
import json

#Database references to perform direct operations
mongo_client=MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db = mongo_client[DB_NAME]
tasks_collection=db['tasks']
contacts_collection=db['contacts']



class DBHelper:

    def __init__(self, db_name='TR2026'):
        self.client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        print('[DBHelper] Connection Created')

    def select_collection(self, collection_name='users'):
        self.collection = self.db[collection_name]
        print('[DBHelper] Collection Selected:', collection_name)

    # save can be anyname of your choice
    def save(self, document):
       inserted_id = self.collection.insert_one(document)
       print('[DBHelper] Document Saved. Id is:', inserted_id)

    def save_many(self, documents):
       inserted_id = self.collection.insert_many(documents)
       print('[DBHelper] Documents Saved')
    
    # retrieve can be anyname of your choice eg: fetch, query
    def retrieve(self, condition=None):
        # result = self.collection.find()
        result = self.collection.find(condition)
        print('[DBHelper] Documents Retrieved. result is:', result)

        # for document in result:
        #     print(document)

        return result

    def update(self, condition=None, document_to_update=None):
        result = self.collection.update_one(
            condition,
            {
                '$set': document_to_update
            }
        )
        print('[DBHelper] Document Updated', result)


    def delete(self, condition):
        result = self.collection.delete_one(condition)
        print('[DBHelper] Document Deleted', result)

    

# this is outside of class
# kind of a extra function to save contacts
def save_contacts():
    file = open('contacts.json', 'r')
    contacts = file.read()
    contacts_dictionary = json.loads(contacts)
    print(contacts_dictionary, type(contacts_dictionary))
    # Capture List of Contacts from JSON
    contacts_to_save = contacts_dictionary['contacts']

    db = DBHelper()
    db.select_collection('contacts')
    db.save_many(contacts_to_save)
    print('Contacts Saved Successfully')