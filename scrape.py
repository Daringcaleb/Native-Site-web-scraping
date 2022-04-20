import requests

# from bs4 import BeautifulSoup
import itertools
import pymongo


BASE_URL = 'https://researchers.wlv.ac.uk/api/users/'

# link to Mongodb   
client = pymongo.MongoClient(
    "mongodb+srv://dase:1cxbOldnM5WmGI9j@cluster0.tboaf.mongodb.net/user?retryWrites=true&w=majority")
db = client.super


def params(startFrom):
    return {
        "params": {
            "by": "text",
            "type": "user",
            "text": ""
        },
        "pagination": {
            "startFrom": startFrom,
            "perPage": 310
        },
        "sort": "relevance",
        "filters": [
            {
                "name": "department",
                "matchDocsWithMissingValues": True,
                "useValuesToFilter": False
            }
        ]
    }
# QUERYING THE STAFF'S DATA


def getData():
    iterateCount = [0, 100, 200, 300]
    for count in iterateCount:
        req = requests.post(
            BASE_URL+'?by=text&text&type=user', json=params(count))
        data = req.json()
        # print(data.get("resource"))
        yield [{"discoveryUrlId": url.get('discoveryUrlId')} for url in data.get("resource")]


dataToInsert = list(itertools.chain(*getData()))
# INSERT THE FIRST DATA
db.data.insert_many(dataToInsert)

users = [item['discoveryUrlId'] for item in db.data.find()]

# GENERATE INDIVIDUAL PROFILE OF THE LECTURERS


def generateProfile(users):
    s = requests.Session()
    for user in users:
        json_url = BASE_URL+user
        res = s.get(json_url)
        res.raise_for_status()
        data = res.json()
        yield data


if __name__ == '__main__':
    #  insert in you mongo atlas
    db.lecturers.insert_many([*generateProfile(users)])
