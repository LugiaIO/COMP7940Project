def movieOutput(movie):
    """Format the movie details for output."""
    detail = (
        "Series Title: "
        + movie["Series_Title"]
        + "\nDirector: "
        + movie["Director"]
        + "\nIMDB Rating: "
        + movie["IMDB_Rating"]
        + "\nGenre: "
        + movie["Genre"]
        + "\nRuntime: "
        + movie["Runtime"]
        + "\nReleased Year: "
        + movie["Released_Year"]
        + "\nOverview: "
        + movie["Overview"]
    )
    image_link = movie["Poster_Link"]
    return detail, image_link


def reviewOutput(review):
    """Format the review details for output."""
    detail = '"' + review["movie_reviews"] + '" - @' + review["username"]
    return detail, review["username"]


def noteOutput(note):
    """Format the note details for output."""
    detail = (
        "Movie name: "
        + note["name"]
        + "\nGenre: "
        + note["genre"]
        + "\nNote: "
        + note["note"]
        + "\nUsername: "
        + note["username"]
    )
    return detail, note["username"]
