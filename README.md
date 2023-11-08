# Spotify Playing History
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white)

A simple Python application to continuosly retrieve and store your Spotify listening history, leveraging the official [Spotify Web API](https://developer.spotify.com/documentation/web-api).

The idea behind this project is to provide a workaround to the official API's lack of a "time played" feature when fetching your playing history, making it impossible to programmatically know which songs you have listened to the most. As of the publishing of this repo, the only way to officially retrieve the milliseconds played for each track in a user's history is to manually ask Spotify to send you this data, as it is illustrated [here](https://support.spotify.com/us/article/understanding-my-data/). This process can take a few days, so it isn't really a feasible option if you want to retrieve your up-to-date data at any given moment.

# How it works
The way this application works is pretty straightforward:
1. A Flask server is used to manage the initial [OAuth2 flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow), which is responsible for the Authorization of the app

2. Once the app is authorized, the main script gets triggered. This consists in an infinite loop where we constantly poll the Spotify API to retrieve the currently playing track (I know that this isn't the best approach, but unfortunately their WebSockets API isn't open to the public)

3. Everytime a song stops playing the script is going to store the track's relevant information (including playtime in ms) into a SQLite database

4. The Flask server mentioned in 1. is providing the stored data in JSON format through a specific endpoint

# Prerequisites
In order to deploy this simple script, you first need to login and [create an app on the official Spotify for Developers website](https://developer.spotify.com/documentation/web-api/concepts/apps), as this is required to go through all the *Authentication* & *Authorization* that the Python app needs in order to function.

Once that's done, you have two ways of deploying this:
- directly using [Python](https://www.python.org/) (*preferably* version >= 3.11)
- using Docker & Docker-compose (both included in [Docker Desktop](https://www.docker.com/products/docker-desktop/))

# How to run
To start using this tool you can either clone this repo, or download the latest release.

As a first step you need to create the **.env** file at the root directory, setting the required environment variables like this:

    CLIENT_ID=<your-app-client_id>
    CLIENT_SECRET=<your-app-client-secret>
    REDIRECT_URI=<your-app-redirect-uri>
    HOST=<your-host-machine-address>
    PORT=<the-port-to-expose>

where the first three rows' values are found in the Spotify for Developer app you just created. 

**Note**: the redirect URI must be the **exact same** on the developer app settings and on the .env file. For our application to work out-of-the-box please set the redirect URI as `<host_address>:<port>/redirect` (for example `http://127.0.0.1:8080/redirect`).

After that is completed, you can decide whether you want to deploy your application using Docker or just with plain Python:

## Python
As an initial step, you will need to install all the required modules and dependencies by executing the following command

    pip install -r requirements.txt

Once that's done you will just need to run the main app program (using the **src** folder as your working directory)
    
    cd src
    python app.py

**Note**: if you're using a MacOS system you might need to replace the above *pip* and *python* commands with *pip3* and *python3*.

## Docker
To deploy this application with Docker-compose you just need to run this command

    docker-compose up
or

    docker-compose up -d

if you want to launch it in detached mode, so that it will run in the background.

# Retrieving the Data
Finally, as the data is being stored in your database, you can easily fetch your listening history by sending a GET request to the `/get_history` endpoint of your Flask server.

You also have the option to select a date range for your request by specifying the *optional* parameters **start** & **end** in the GET request (both need to be a date in YYYY-MM-DD format).

Upon a successful request, you will recieve your playing history in JSON format, which you can then use for whatever use case/analysis you might have 😉.

### Example response:

    [
      {
          "id": "2uB9gUU1HLnHckvK2tylJM",
          "name": "Deeper",
          "artist": "Freddie Gibbs",
          "featured_artists": null,
          "duration_ms": 199053,
          "release_date": "2014-03-18",
          "popularity": 52,
          "started_at": "2023-11-07 22:41:38.725070",
          "ms_played": 29980
      },
      {
          "id": "3VjCEyc0bHfa4Ie34kbWyb",
          "name": "CANDY - Remix",
          "artist": "ROSALÍA",
          "featured_artists": "Chencho Corleone",
          "duration_ms": 204654,
          "release_date": "2022-09-09",
          "popularity": 68,
          "started_at": "2023-11-07 22:43:38.271046",
          "ms_played": 19034
      }
    ]

Enjoy your musical taste 😎
