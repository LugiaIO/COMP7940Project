import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import json 

# Fetch the service account key JSON file contents
cred = credentials.Certificate('certain-reducer-381500-firebase-adminsdk-yvaaz-7a3bed5b0c.json')
# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred)
firestore_client = firestore.client()

with open('imdb_top_1000.json', 'r') as f:
  movies = json.load(f)
  for movie in movies:
    print(movie['Series_Title'])
    doc_ref = firestore_client.collection("movies").document(movie['Series_Title'])
    doc_ref.set(movie)