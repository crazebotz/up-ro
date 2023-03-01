# funcs
import pymongo,os
from datetime import date

# ------------Database----------
DB_URL = os.environ.get("DB_URL", "mongodb+srv://admin:rahul@mydatabase.zu1yt8m.mongodb.net/?retryWrites=true&w=majority")

mongo = pymongo.MongoClient(DB_URL)
db = mongo["uploader"]
dbcol = db["users"]




# check user data update
def is_today(chat_id):
    date_str = find_any(chat_id,"DATE")
    if date_str:
        year, month, day = map(int, date_str.split("-"))
        date_tuple = (year, month, day)
        specific_date = date(*date_tuple)
        today = date.today()
        
        if today == specific_date:
           return True
        else:
           return False
    else:
        return False


# check remain usage
def check_usage(chat_id,file_size):
    u_remain = find_any(chat_id, "U_USAGE")
    if u_remain < file_size:
        return u_remain,False
    else:
        
        return u_remain, True



# get total users from db
def total_user() -> str:
    user = dbcol.count_documents({})
    return str(user)


# insert user data
def insert(chat_id,NAME):
    user_id = int(chat_id)
    user_det = {"_id": user_id,"name": NAME,"DATE": None, "U_USAGE": None, "CAPTION": None, "PHOTO_THUMB": None}
    try:
        dbcol.insert_one(user_det)
    except:
        return True

#find any data from just query
def find_any(id,query):
    id = {"_id": id}
    x = dbcol.find(id)
    for i in x:
        try:
            result = i[f"{query}"]
            
        except:
            result = None
    
        return result

    # return dbcol.find_one({"_id": id})

   
#add DATA Dynamic
def addDATA(chat_id,KEY, VALUE):
    dbcol.update_one({"_id": chat_id}, {"$set": {f"{KEY}": VALUE}})


#Delete DATA Dynamic
def delDATA(chat_id,KEY):
    dbcol.update_one({"_id": chat_id}, {"$set": {f"{KEY}": None}})

def getid():
    values = []
    for key in dbcol.find():
        id = key["_id"]
        values.append((id))
    return values


def delete(id):
    dbcol.delete_one(id)


# X = find_any(5294965763,"U_USAGE")
# Y = find_any(5294965763,"DATE")

# print(X,Y)
