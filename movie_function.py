import random
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import os
import json

# Fetch the service account key JSON file contents
json_object = json.loads(os.environ["DB_KEY"])
cred = credentials.Certificate(json_object)
# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred)
firestore_client = firestore.client()

# A reference to the movies collection.
def getReference(collection):
    coll_ref = firestore_client.collection(collection)
    return coll_ref


def randomMovie():
    movie_list = []
    coll_ref = getReference("movies")
    for doc in coll_ref.stream():
        movie_list.append(doc.to_dict())

    return random.choice(movie_list)


def search(keyword):
    # Create a query against the collection reference.
    coll_ref = getReference("movies")
    query_ref = coll_ref.where("Series_Title_Index", "array_contains", keyword)
    movie_list = []
    # Print the documents returned from the query:
    for doc in query_ref.stream():
        movie_list.append(doc.to_dict())

    return movie_list


def read(movie_name):
    # Create a query against the collection reference.
    coll_ref = getReference("movie_reviews")
    collections = coll_ref.document(movie_name).collections()
    reviews_list = []
    for collection in collections:
        for doc in collection.stream():
            reviews_list.append(doc.to_dict())

    return reviews_list

