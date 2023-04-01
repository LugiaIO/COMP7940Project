import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import os

def conn():
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate(os.environ["DB_KEY"])
    # Initialize the app with a service account, granting admin privileges
    app = firebase_admin.initialize_app(cred)
    firestore_client = firestore.client()

    # A reference to the movies collection.
    coll_ref = firestore_client.collection("movies")
    return coll_ref