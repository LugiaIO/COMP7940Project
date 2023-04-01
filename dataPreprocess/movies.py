import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import random 

# Fetch the service account key JSON file contents
cred = credentials.Certificate('certain-reducer-381500-firebase-adminsdk-yvaaz-7a3bed5b0c.json')
# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred)
firestore_client = firestore.client()

# A reference to the laptops collection.
coll_ref = firestore_client.collection("movies")
movie_list = []


for doc in coll_ref.stream():
    movie_list.append(doc.to_dict())
    #print(type)
    #print(f"{doc.id} => {doc.to_dict()}")

print(random.choice(movie_list))