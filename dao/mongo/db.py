from pymongo import MongoClient


# todo add connection pooling
class MongoDB:
    """Performs CRUD Operations for MongoDB"""

    def __init__(self, database):
        """Initialize the MongoDB Client and select a database to modify"""
        self.client = MongoClient()
        self.mongo_database = self.client[str(database)]

    def create(self, collection, doc, single_doc=False):
        """Creates a new document and inserts it into the specified collection"""
        if single_doc:
            return self.mongo_database[collection].insert_one(doc).inserted_id
        else:
            return self.mongo_database[collection].insert(doc)

    def read(self, collection, query=None, single_doc=False, sort_args=None):
        """Returns the document(s) that match the query"""
        if single_doc:
            return self.mongo_database[collection].find_one(query)
        else:
            if sort_args:
                return self.mongo_database[collection].find(query).sort(sort_args)
            else:
                return self.mongo_database[collection].find(query)

    def update(self, collection, query, update_args, upsert=False, single_doc=False):
        """Modifies the document(s) that match the query"""
        if single_doc:
            return self.mongo_database[collection].update_one(query, update_args, upsert)
        else:
            return self.mongo_database[collection].update_many(query, update_args, upsert)

    def delete(self, collection, query, single_doc=False):
        """Deletes all documents that match the query"""
        if single_doc:
            return self.mongo_database[collection].delete_one(query)
        else:
            return self.mongo_database[collection].delete_many(query)
