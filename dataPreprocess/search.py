import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import json 

# Fetch the service account key JSON file contents
cred = credentials.Certificate('certain-reducer-381500-firebase-adminsdk-yvaaz-7a3bed5b0c.json')
# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred)
firestore_client = firestore.client()

# A reference to the laptops collection.
coll_ref = firestore_client.collection("movies")

# Create a query against the collection reference.
query_ref = coll_ref.where("Series_Title_Index", "array_contains", "Book")

# Print the documents returned from the query:
for doc in query_ref.stream():
    print(f"{doc.id} => {doc.to_dict()}")