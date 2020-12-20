Python Code Test 2020
=====================

This package contains of a Flask application which serves _Game of Thrones_ episodes
information.

## How to run

Run below command to run the service:

```
docker-compose up
```

Tt runs two containers:

* got: Flask application
* got_db: mySQL database

First time the service is running, it creates database and tables automatically.
It takes time the database be ready and be accessible. please check the log messages.

if database is not ready it will show below message:

`Could not connect to database! trying again in 10 seconds!``

it tries automatically to connect database until can make  a successfull connection
after that it fetches data from _OMDB_ and after fetching data all of episodes it shows below
message:

``Server is ready now!``

it means server is ready now and can reach the endpoints on the localhost port 80.

## Tests

This package has below tests:

1. Unit tests : 100% coverage
2. Flake8
3. Black: Formatting 
4. typing

you can run all tests by below command:

``make test``

or below commands for a specific test:

```make unittests```

```make flake```

```make testformatting```

```make testtyping```

## Database

_mySQL_ is used for database and all of its data will be store on the host in
`./data/mysql`

## Endpoints

* GET `/v1/`

    Returns all episodes information

* GET `/v1/<episode_id>`

    Returns information of an episode

    example : `http://localhost/v1/2` 

*  GET `/v1/high_rate`

    Returns all episodes with IMDB rate greater than 8.8
    
* GET `/v1/high_rate/<season_number>`

    Returns all episodes of a season with IMDB rate greater than 8.8
    
* GET `/comment/<episode_id>`

    Returns all comments of an episode same as below:
    
    ```json
    {
    "comments": [
        {
            "author": "test <test@test.com>",
            "body": "this episode was very nice!",
            "episode_id": 1,
            "id": 2,
            "time_stamp": "Sun, 20 Dec 2020 11:40:42 GMT"
        }
      ]
    }
    ``
    
* POST `/comment/<episode_id>`

    Post a comment for an episode. It needs a JSON payload as below:
    
    ```json
    {
      "author": "<author of this comment>",
      "body": "<body of the comment>"    
    }
    ```
  
    Return codes:
    
        200: successful
        
        400: Invalid episode id or payload
         
* DELETE `/comment/<comment_id>`

    Deletes a comment by its ID.
    
    Return codes:
    
        200: successful
        
        400: Invalid comment ID.
        
* PUT `/comment/<comment_id>`

    Updates a comment.
    
    It needs a JSON payload as below:
    
    ```json
    {
      "author": "new author",
      "body": "new body",
      "episode_id": <new episode ID>
    }
    ```
    
    or only the parameters those need to be updated.
    
    example: 
    
    ```json
    {
      "author": "new author",
      "episode_id": 3
    }
    ```
    
    Return codes:
    
        200: successful
        
        400: Invalid comment ID or invalid payload.
    
