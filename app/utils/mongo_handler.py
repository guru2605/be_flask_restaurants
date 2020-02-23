from datetime import datetime
# noinspection PyPackageRequirements
from bson import ObjectId
from pymongo import MongoClient


class MongoHandler:
    """
    Class consist
    """

    def __init__(self, host: str = 'localhost', port: int = 27017,):
        self.client = MongoClient(host=host, port=port)

    def get_client(self):
        """
        Get the Mongodb client.
        :return: 
        """
        return self.client

    def close_client(self):
        """
        Releases any valuable MongoDb Resources
        :return: 
        """
        self.client.close()

    def get_db(self, db_name: str):
        """
        Gets the Mongodb database specified by db_name
        :param db_name: 
        :return: 
        """
        return self.client[db_name]

    def drop_db(self, db_name: str):
        """
        Drops the Mongodb database specified by db_name
        :param db_name: 
        :return: 
        """
        return self.client.drop_database(self.client[db_name])

    def create_collection(self, db_name: str, collection_name: str):
        """
        Creates the collection specified by collection_name inside db_name Database
        :param db_name: 
        :param collection_name: 
        :return: 
        """
        db = self.get_db(db_name)
        return db.createCollection[collection_name]

    def get_collection(self, db_name: str, collection_name: str):
        """
        Gets the collection specified by collection_name in db_name Database
        :param db_name: 
        :param collection_name: 
        :return: 
        """
        db = self.get_db(db_name)
        return db[collection_name]

    def delete_collection(self, db_name: str, collection_name: str):
        """
        Deletes the collection specified by collection_name in db_name Database
        :param db_name: 
        :param collection_name: 
        :return: 
        """
        db = self.get_db(db_name)
        return db.drop_collection(collection_name)

    def insert_doc(self, obj_json_to_insert: dict, db_name: str, collection_name: str, session=None):
        """
        Inserts the document
        :param obj_json_to_insert: 
        :param db_name: 
        :param collection_name: 
        :param session: 
        :return: 
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        obj_json_to_insert['last_modified_time'] = datetime.utcnow()
        return collection.insert_one(obj_json_to_insert, session=session)

    def insert_doc_many(self, obj_dict_list: list, db_name: str, collection_name: str, session=None):
        """
        Inserts list to documents
        :param obj_dict_list: 
        :param db_name: 
        :param collection_name: 
        :param session: 
        :return: 
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        return collection.insert_many(obj_dict_list, session=session)

    def update_doc(self, obj_json_to_query: dict, obj_json_to_update: dict, db_name: str, collection_name: str,
                   session=None):
        """
        Updates multiple documents
        :param obj_json_to_query: 
        :param obj_json_to_update: 
        :param db_name: 
        :param collection_name: 
        :param session: 
        :return: 
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        obj_json_to_update['last_modified_time'] = datetime.utcnow()
        return collection.update_many(obj_json_to_query, {'$set': obj_json_to_update}, session=session)

    def update_one_doc(self, obj_json_to_query: dict, obj_json_to_update: dict, db_name: str, collection_name: str,
                       unset_json: dict = None, upsert=False, session=None):
        """
        Updates the document
        :param obj_json_to_query: 
        :param obj_json_to_update: 
        :param db_name: 
        :param collection_name: 
        :param unset_json: 
        :param session:
        :param upsert:
        :return: 
        """
        if unset_json is None:
            unset_json = {}
        db = self.get_db(db_name)
        collection = db[collection_name]
        obj_json_to_update['last_modified_time'] = datetime.utcnow()
        if unset_json:
            return collection.update_one(obj_json_to_query, {'$set': obj_json_to_update, '$unset': unset_json},
                                         upsert=upsert,
                                         session=session)

        return collection.update_one(obj_json_to_query, {'$set': obj_json_to_update}, upsert=upsert, session=session)

    def update_one_doc_increment(self, obj_json_to_query: dict, obj_json_to_update: dict, db_name: str,
                                 collection_name: str, unset_json: dict = None, session=None):
        """
        Updates the document
        :param obj_json_to_query: 
        :param obj_json_to_update: 
        :param db_name: 
        :param collection_name: 
        :param unset_json: 
        :param session: 
        :return: 
        """
        if unset_json is None:
            unset_json = {}
        db = self.get_db(db_name)
        collection = db[collection_name]
        # obj_json_to_update['last_modified_time'] = datetime.utcnow()
        if unset_json:
            return collection.update_one(obj_json_to_query, {'$inc': obj_json_to_update, '$unset': unset_json},
                                         session=session)

        return collection.update_one(obj_json_to_query, {'$inc': obj_json_to_update}, session=session)

    def update_value_of_object_in_doc(self, obj_json_to_query: dict, obj_json_to_update: dict, db_name: str,
                                      collection_name: str, session=None):
        """
        Updates the document
        :param obj_json_to_query:
        :param obj_json_to_update:
        :param db_name:
        :param collection_name:
        :param session:
        :return:
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        return collection.update_many(obj_json_to_query, obj_json_to_update, session=session)

    def add_elements_to_array_in_doc(self, obj_json_to_query: dict, field_name: str, array_to_add: list, db_name: str,
                                     collection_name: str):
        """
        Adds array of values
        :param obj_json_to_query:
        :param field_name:
        :param array_to_add:
        :param db_name:
        :param collection_name:
        :return:
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        return collection.update(obj_json_to_query, {'$push': {field_name: {'$each': array_to_add}}})

    def remove_elements_from_array_in_doc(self, obj_json_to_query: dict, field_name: str, array_to_remove: list,
                                          db_name: str, collection_name: str):
        """
        Removes array of values
        :param obj_json_to_query:
        :param field_name:
        :param array_to_remove:
        :param db_name:
        :param collection_name:
        :return:
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        return collection.update(obj_json_to_query, {'$pull': {field_name: {'$in': array_to_remove}}})

    def get_document_by_id(self, db_name: str, collection_name: str, object_id: str, session=None):
        """
        Get Specified ObjectId document
        :param db_name:
        :param collection_name:
        :param object_id:
        :param session:
        :return:
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        return collection.find_one({'_id': ObjectId(object_id)}, session=session)

    def get_document_by_id_string(self, db_name: str, collection_name: str, filter_json: dict, projection: dict,
                                  session=None):
        """
        Get Specified Document
        :param db_name:
        :param collection_name:
        :param filter_json:
        :param projection:
        :param session:
        :return:
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        return collection.find_one(filter_json, projection, session=session)

    def filter_docs(self, db_name: str, collection_name: str, filter_json: dict, projection: dict = None,
                    sort_list: list = None, session=None):
        """
        Gets all documents from the specified collection by applying the filter passed in the filter_json
        :param db_name:
        :param collection_name:
        :param filter_json:
        :param projection:
        :param sort_list:
        :param session:
        :return:
        """
        if sort_list is None:
            sort_list = []
        db = self.get_db(db_name)
        collection = db[collection_name]
        if sort_list:
            return collection.find(filter_json, projection, session=session).sort(sort_list)

        return collection.find(filter_json, projection, session=session)

    def count_docs(self, db_name: str, collection_name: str, filter_json: dict, projection: dict = None,
                   sort_list: list = None, session=None):
        """
        Gets all documents from the specified collection by applying the filter passed in the filter_json
        :param db_name:
        :param collection_name:
        :param filter_json:
        :param projection:
        :param sort_list:
        :param session:
        :return:
        """
        if sort_list is None:
            sort_list = []
        db = self.get_db(db_name)
        collection = db[collection_name]
        if sort_list:
            return collection.find(filter_json, projection, session=session).sort(sort_list).count()

        return collection.find(filter_json, projection, session=session).count()

    def filter_one_doc(self, db_name: str, collection_name: str, filter_json: dict, projection: dict = None,
                       sort_json: list = None, session=None):
        """
        Gets only the matching document from the specified collection by applying the filter passed in the filter_json.
        :param db_name:
        :param collection_name:
        :param filter_json:
        :param projection:
        :param sort_json:
        :param session:
        :return:
        """
        if sort_json is None:
            sort_json = {}
        db = self.get_db(db_name)
        collection = db[collection_name]
        if sort_json:
            return collection.find_one(filter_json, projection, sort=sort_json, session=session)

        return collection.find_one(filter_json, projection, session=session)

    def delete_one_doc(self, db_name: str, collection_name: str, filter_json: dict, session=None):
        """
        Deletes only first matching document from the specified collection by applying the filter passed in the
        filter_json.
        :param db_name:
        :param collection_name:
        :param filter_json:
        :param session:
        :return:
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        result = collection.delete_one(filter_json, session=session)
        return result.deleted_count

    def find_distinct_fields(self, db_name: str, collection_name: str, distinct_key: str, filter_json: dict = None,
                             session=None):
        """
        Finds distinct entries of the key based on the filter passed.
        :param db_name:
        :param collection_name:
        :param distinct_key:
        :param filter_json:
        :param session:
        :return:
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        return collection.distinct(distinct_key, filter=filter_json, session=session)

    def aggregate_docs(self, db_name: str, collection_name: str, aggregate_filter: list, session=None):
        """
        Unwind Nested Array and Match condition passed and Project in specified collection.
        :param db_name:
        :param collection_name:
        :param aggregate_filter:
        :param session:
        :return:
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        return collection.aggregate(aggregate_filter, session=session)

    def create_index(self, db_name: str, collection_name: str, index_data: list, uniqueness: bool = False,
                     session=None):
        """
        Creates Index in specified collection with index_data.
        :param db_name:
        :param collection_name:
        :param index_data:
        :param uniqueness:
        :param session:
        :return:
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        return collection.create_index(index_data, unique=uniqueness, sparse=True, session=session)

    def delete_docs(self, db_name: str, collection_name: str, filter_json: dict, session=None):
        """
        Deletes matching documents from the specified collection by applying the filter passed in the filter_json.
        :param db_name:
        :param collection_name:
        :param filter_json:
        :param session:
        :return:
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        result = collection.delete_many(filter_json, session=session)
        return result.deleted_count

    def get_all_databases(self):
        """
        Get All Databases with the client.
        :return:
        """
        return self.client.list_database_names()

    def get_all_collections_of_database(self, db_name: str):
        """
        Get list of Collections in the database
        :param db_name:
        :return:
        """
        db = self.get_db(db_name)
        return db.list_collection_names()

    def update_fields(self, obj_json_to_query: dict, obj_json_to_update: dict, db_name: str, collection_name: str,
                      session=None):
        """
        Updates multiple documents
        :param obj_json_to_query: 
        :param obj_json_to_update: 
        :param db_name: 
        :param collection_name: 
        :param session: 
        :return: 
        """
        db = self.get_db(db_name)
        collection = db[collection_name]
        return collection.update_many(obj_json_to_query, {'$rename': obj_json_to_update}, session=session)

    def rename_collection(self, db_name: str, collection: str, new_name: str, session=None):
        """

        :param db_name:
        :param collection:
        :param new_name:
        :param session:
        :return:
        """
        db = self.get_db(db_name)
        return db[collection].rename(new_name, session=session)
