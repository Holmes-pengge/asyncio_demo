from pymongo import MongoClient

mongo_config_ebay = {
    'username': 'ebay',
    'password': '464d7146f5f642d3bad957ad249a679d',
    'host': '45.34.33.156',
    'authSource': 'admin',
    'authMechanism': 'SCRAM-SHA-256',
}

local_mongo_config_ebay = {
    'host': 'localhost',
    "port": 27018,
}

client = MongoClient(**mongo_config_ebay)
db = client['ebay']

local_client = MongoClient(**local_mongo_config_ebay)
local_db = local_client['ebay']

for d in db.item.find({}).limit(100):
    # # update Viewed 为 true 并保存
    # d['Viewed'] = True
    # db.seller.save(d)
    print(d)
    # 存到 local_db current seller
    local_db.item.insert_one(d)
