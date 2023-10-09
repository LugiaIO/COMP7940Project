# Movie Chatbot

Movie Chatbot is a Python-based Telegram bot that provides movie information, reviews, and note-taking capabilities. It utilizes various APIs and services to fetch movie data, process text-to-speech conversions, and store information in a cloud-based database.

## Table of Contents

- [Movie Chatbot](#movie-chatbot)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Features](#features)
  - [Dependencies](#dependencies)
  - [Contributing](#contributing)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Niltopia/COMP7940Project.git
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Set the environment variables:

- `TOKEN`: Your Telegram Bot Token
- `DB_KEY`: JSON representation of your Google Cloud Text-to-Speech API credentials

4. Run the application:

```bash
python app.py
```

## Usage

- Start the MovieBot by running the Flask server.
- Interact with the bot by sending commands in a Telegram chat.

## Features

- Search for Movies: Use the `/search` command followed by one or more keywords to search for movies. The bot will retrieve matching movies and display their details and posters.
- Read Movie Reviews: Use the `/read_reviews` command followed by the name of a movie to read reviews for that movie. The bot will retrieve reviews from the Firestore database and display them along with the username of the reviewer.
- Get Random Movie: Use the `/random_movie` command to get a random movie recommendation. The bot will retrieve a random movie from the Firestore database and display its details and poster.
- List Saved Notes: Use the `/list_note` command to list the saved notes in the Firestore database. The bot will retrieve all notes and display their details, including the movie name, genre, note, and username.
- Add Movie Note: Use the `/start_note` command to add a note for a movie. The bot will guide you through a conversation to enter the movie name, genre, and note. Once submitted, the note will be saved in the Firestore database.
- Write Movie Review: Use the `/write_review` command to write a review for a movie. The bot will guide you through a conversation to enter the movie name and your review. Once submitted, the review will be saved in the Firestore database under the respective movie's collection.

## Dependencies

The system relies on the following Python libraries:

- Flask: A lightweight web framework used for creating the bot's HTTP server.
- python-telegram-bot: A Python wrapper for the Telegram Bot API, providing convenient methods for interacting with Telegram bots.
- Werkzeug: A WSGI utility library used by Flask for handling HTTP requests and responses.
- firebase_admin: A Python SDK for integrating with Firebase services, used in this project for accessing Firestore.
- google-cloud-texttospeech: A client library for the Google Cloud Text-to-Speech API, enabling text-to-speech conversions.
- google-auth: A library for handling authentication with Google APIs, used in this project for the Text-to-Speech API credentials.
- google-auth-oauthlib: A library for handling OAuth-based authentication with Google APIs.
- google-auth-httplib2: A library providing authentication for HTTP requests made with the httplib2 library.

## Contributing

Developer: Vesper - [@Niltopia](https://github.com/Niltopia) - pccw@duck.com
Developer: Henry Zheng - [@FEI120483](https://github.com/FEI120483) - 1204831218@qq.com
