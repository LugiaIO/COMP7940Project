The_Jungle_Book = {
    "Series_Title_Index": ["The", "Jungle", "Book"],
    "Star2": "Sebastian Cabot",
    "Certificate": "U",
    "Genre": "Animation, Adventure, Family",
    "Released_Year": "1967",
    "Meta_score": "65",
    "Star1": "Phil Harris",
    "Series_Title": "The Jungle Book",
    "Gross": "141,843,612",
    "Star3": "Louis Prima",
    "IMDB_Rating": "7.6",
    "Director": "Wolfgang Reitherman",
    "Runtime": "78 min",
    "Overview": "Bagheera the Panther and Baloo the Bear have a difficult time trying to convince a boy to leave the jungle for human civilization.",
    "No_of_Votes": "166409",
    "Star4": "Bruce Reitherman",
    "Poster_Link": "https://m.media-amazon.com/images/M/MV5BMjAwMTExODExNl5BMl5BanBnXkFtZTgwMjM2MDgyMTE@._V1_UX67_CR0,0,67,98_AL_.jpg",
}


def output(movie):
    detail="Series Title: " + movie["Series_Title"] + "\nDirector: " + movie["Director"] + "\nIMDB Rating: " + movie["IMDB_Rating"] + "\nGenre: " + movie["Genre"] + "\nRuntime: " + movie["Runtime"] + "\nReleased Year: " + movie["Released_Year"] + "\nOverview:" + movie["Overview"]
    image_link = movie["Poster_Link"]
    return detail, image_link
