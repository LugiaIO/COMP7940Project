from database_config import conn
import random

def randomMovie():
    coll_ref = conn()
    movie_list = []
    for doc in coll_ref.stream():
        movie_list.append(doc.to_dict())
    
    return random.choice(movie_list)

def search(keyword):
    coll_ref = conn()
    # Create a query against the collection reference.
    query_ref = coll_ref.where("Series_Title_Index", "array_contains", keyword)
    movie_list = []
    # Print the documents returned from the query:
    for doc in query_ref.stream():
        movie_list.append(doc.to_dict())
    
    return movie_list