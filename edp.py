import urllib.request, json 
from datetime import datetime, timedelta
import os
import pymongo
from dotenv import load_dotenv

#Load env variables
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path)



MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION_CONSUMPTION = os.getenv("MONGO_COLLECTION_CONSUMPTION")
MONGO_COLLECTION_PRODUCTION = os.getenv("MONGO_COLLECTION_PRODUCTION")



baseURL = "https://www.edp-distribuicao.com/dados-energia/endpoint"

def getJSON( jsonURL ):
    with urllib.request.urlopen( baseURL + jsonURL ) as url:
        return json.loads(url.read().decode())




#Get yestardays date in YYYYMMDD format
yesterday = datetime.now() - timedelta(1)
yesterdayDate = datetime.strftime(yesterday, '%Y%m%d')


#Initailiaze Database
myclient = pymongo.MongoClient("mongodb://"+str(MONGO_HOST)+":"+MONGO_PORT+"/")
mydb = myclient[MONGO_DB]


consumptionFullURL = "?action=data&group=consumption&graph=statistics&date=" + yesterdayDate
consumptionJSON = getJSON( consumptionFullURL )

#Set mongo collection
mycol = mydb[MONGO_COLLECTION_CONSUMPTION]

consumptionRecord = {
    "date" : yesterdayDate,
    "mat" : consumptionJSON["rows"][0][2],
    "at" : consumptionJSON["rows"][1][2],
    "mt" : consumptionJSON["rows"][2][2],
    "bt" : consumptionJSON["rows"][3][2]
}

x = mycol.insert_one(consumptionRecord)


productionFullURL = "?action=data&group=production-national&graph=statistics&date=" + yesterdayDate
productionJSON = getJSON( productionFullURL )

#Set mongo collection
mycol = mydb[MONGO_COLLECTION_PRODUCTION]

productionRecord = {
    "date" : yesterdayDate,
    "pre" : productionJSON["rows"][0][2],
    "dgm" : productionJSON["rows"][1][2]
}

x = mycol.insert_one(productionRecord)
