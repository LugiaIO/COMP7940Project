def movieOutput(movie):
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
    detail = '"' + review['movie_reviews'] + '" - @' + review['username']
    return detail, review['username']
