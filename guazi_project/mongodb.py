import pymongo


class Mongo():
    def __init__(self):
        # 连接数据库
        self.mymongo = pymongo.MongoClient("mongodb://admin:abc123456@localhost:27017")
        # 选择数据库
        mongo_db = self.mymongo['guazi_db']
        # 选择表
        self.my_collections = mongo_db['guazi_collections']

    def get_data(self):
        result = self.my_collections.find_one_and_delete({})
        return result

    def save(self,data):
        self.my_collections.insert_one(data)

    def save_many(self,data):
        mongo_db = self.mymongo['guazi_db']
        collections = mongo_db['crawl_finish']
        collections.update({'car_id':data['car_id']},data,True)