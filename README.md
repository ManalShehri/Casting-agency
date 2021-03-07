# Casting-agency

The Casting Agency is th Udacity capstone project which models company that is responsible for creating movies and managing and assigning actors to those movies. It has three access roles as showen in below table. 

Role  | Access permission
------------- | -------------
Casting Assistant  | view actors and movies 
Casting Director  | All permissions a Casting Assistant has + Add or delete an actor & Modify actors or movies
Executive Producer  | All permissions a Casting Director has + Add or delete a movie


## Getting Started 

### Pre-requisites and Local Development

Developers using this project should already have:

- Python3 
- Pip 

#### Backend 

initialize and activate a virtualenv
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

then run ``` pip install -r requirements.txt ``` All required packages are included in the requirements file.


To export the credentials as environment variable including DB variables, tokens and ENV
```
source setup.sh
```

To run the application run the following commands:

```
python app.py
```
The application is run on  ``` http://127.0.0.1:8080/``` 


#### Tests

To run the tests, run

```
python test_app.py
```


## API Reference

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

404: Resource Not Found
401: Not Authorized
500: Internal Server Error
405: Method Not Allowed

### Endpoints


**GET /actors**

General:
- Returns a list of actors, success value
- Authorized Roles: Casting Assistant,Casting Director,Executive Producer.

Sample: ```curl http://127.0.0.1:8080/actors```

```
{
    "actors": [
        {
            "age": 45,
            "bio": "Angelina Jolie is an American actress, filmmaker, and humanitarian. The recipient of numerous accolades, including an Academy Award and three Golden Globe Awards.",
            "created_at": "2021-03-03 16:58:24",
            "gender": "female",
            "id": 1,
            "image_link": "http:/image/Angelina_Jolie/1",
            "name": "Angelina Jolie",
            "updated_at": "None"
        },
        {
            "age": 57,
            "bio": "William Bradley Pitt is an American actor and film producer. He has received multiple awards, including two Golden Globe Awards and an Academy Award for his acting.",
            "created_at": "2021-03-03 17:08:15",
            "gender": "male",
            "id": 2,
            "image_link": "http:/image/Brad_Pitt/1",
            "name": "Brad Pitt",
            "updated_at": "None"
        },
        {
            "age": 52,
            "bio": "Jennifer Joanna Aniston is an American actress, producer, and businesswoman. The daughter of actors John Aniston and Nancy Dow.",
            "created_at": "2021-03-04 09:15:40",
            "gender": "female",
            "id": 3,
            "image_link": "http:/image/Jennifer_Aniston/1",
            "name": "Jennifer Aniston",
            "updated_at": "None"
        },

        {
            "age": 45,
            "bio": "ALeonardo Wilhelm DiCaprio is an American actor, film producer, and environmentalist. He has often played unconventional roles, particularly in biopics and period films.",
            "created_at": "2021-03-04 10:30:43",
            "gender": "male",
            "id": 4,
            "image_link": "http:/image/Leonardo_DiCaprio/1",
            "name": "Leonardo DiCaprio",
            "updated_at": "None"
        }
    ],
    "success": true
}
```


**GET /movies**

General:
- Returns a list of movies, success value
- Authorized Roles: Casting Assistant,Casting Director,Executive Producer.

Sample: ```curl http://127.0.0.1:8080/movies```

```
{
    "movies": [
        {
            "category": [
                "Drama"
            ],
            "created_at": "2021-03-03 17:10:11",
            "description": "Anna sets out on a journey with an iceman, Kristoff, and his reindeer, Sven, in order to find her sister, Elsa, who has the power to convert any object or person into ice.",
            "director": "Jennifer Lee,",
            "id": 1,
            "image_link": "http:/image/frozen/1",
            "release_date": "Tue, 19 Nov 2013 00:00:00 GMT",
            "title": "Frozen I",
            "updated_at": "None"
        },
        {
            "category": [
                "Drama"
            ],
            "created_at": "2021-03-03 17:10:11",
            "description": "Anna sets out on a journey with an iceman, Kristoff, and his reindeer, Sven, in order to find her sister, Elsa, who has the power to convert any object or person into ice.",
            "director": "Jennifer Lee,",
            "id": 1,
            "image_link": "http:/image/frozen/2",
            "release_date": "Tue, 19 Nov 2019 00:00:00 GMT",
            "title": "Frozen II",
            "updated_at": "None"
        }
    ],
    "success": true
}
```


**DELETE /actors/{id}**

General:
- Deletes the actor of the given ID if it exists. Returns success value and message.
- Authorized Roles: Casting Director,Executive Producer.

Sample ```curl -X DELETE http://127.0.0.1:8080/actors/1 ```


```
{
    "Message": "Actor deleted successfully",
    "success": true
}
```

**DELETE /movies/{id}**

General:
- Deletes the movie of the given ID if it exists. Returns success value and message.
- Authorized Role: Executive Producer.

Sample ```curl -X DELETE http://127.0.0.1:8080/movies/1 ```


```
{
    "Message": "Movie deleted successfully",
    "success": true
}
```


**POST /actors/new**


General:
- Add a new actor 
- Returns the actor info, success value
- Authorized Roles: Casting Director,Executive Producer.

Sample: ```curl http://127.0.0.1:8080/actors/new -X POST -H "Content-Type: application/json" -d '{"name": "Angelina","age": 45,"gender": "female", "image_link": "http:/image/Angelina_Jolie/1", "bio": "Angelina Jolie is an American actress, filmmaker, and humanitarian. The recipient of numerous accolades, including an Academy Award and three Golden Globe Awards."}'```


```
{
    "new_actor": {
        "age": 45,
        "bio": "Angelina Jolie is an American actress, filmmaker, and humanitarian. The recipient of numerous accolades, including an Academy Award and three Golden Globe Awards.",
        "created_at": "2021-03-04 12:13:33",
        "gender": "female",
        "id": 1,
        "image_link": "http:/image/Angelina_Jolie/1",
        "name": "Angelina",
        "updated_at": "None"
    },
    "success": true
}
```

**POST /movies/new**


General:
- Add a new movie 
- Returns the movie info, success value
- Authorized Role: Executive Producer.

Sample: ```curl http://127.0.0.1:8080/movies/new -X POST -H "Content-Type: application/json" -d '{"title": "Frozen I","release_date": "2013-11-19 00:00:00","description": "Anna sets out on a journey with an iceman, Kristoff, and his reindeer, Sven, in order to find her sister, Elsa, who has the power to convert any object or person into ice.","director": "Jennifer Lee,", "category": ["Drama"],"image_link": "http:/image/frozen/1"}'```


```
{
    "new_moive": {
        "category": [
            "Drama"
        ],
        "created_at": "2021-03-04 12:20:54",
        "description": "Anna sets out on a journey with an iceman, Kristoff, and his reindeer, Sven, in order to find her sister, Elsa, who has the power to convert any object or person into ice.",
        "director": "Jennifer Lee,",
        "id": 1,
        "image_link": "http:/image/frozen/1",
        "release_date": "Tue, 19 Nov 2013 00:00:00 GMT",
        "title": "Frozen I",
        "updated_at": "None"
    },
    "success": true
}
```



**PATCH /actors/1**

General:
- edit actor info 
- Returns the actor info, success value and message
- Authorized Roles: Casting Director,Executive Producer.


Sample``` curl http://127.0.0.1:8080/actors/1 -X PATCH -H "Content-Type: application/json" -d '{"name": "Angelina Jolie"}'``` 


```
{
    "Message": "Actor updated successfully",
    "actor": {
        "age": 45,
        "bio": "Angelina Jolie is an American actress, filmmaker, and humanitarian. The recipient of numerous accolades, including an Academy Award and three Golden Globe Awards.",
        "created_at": "2021-03-04 12:13:33",
        "gender": "female",
        "id": 1,
        "image_link": "http:/image/Angelina_Jolie/1",
        "name": "Angelina Jolie",
        "updated_at": "2021-03-04 12:27:02.419482"
    },
    "success": true
}
```

**PATCH /movies/1**

General:
- edit movie info 
- Returns the movie info, success value and message
- Authorized Roles: Casting Director,Executive Producer.


Sample``` curl http://127.0.0.1:8080/movies/1 -X PATCH -H "Content-Type: application/json" -d '{"title": "Frozen II","release_date":"2019-11-19 00:00:00"}'``` 


```
{
    "Message": "Movie updated successfully",
    "movie": {
        "category": [
            "Drama"
        ],
        "created_at": "2021-03-04 12:20:54",
        "description": "Anna sets out on a journey with an iceman, Kristoff, and his reindeer, Sven, in order to find her sister, Elsa, who has the power to convert any object or person into ice.",
        "director": "Jennifer Lee,",
        "id": 1,
        "image_link": "http:/image/frozen/1",
        "release_date": "Tue, 19 Nov 2019 00:00:00 GMT",
        "title": "Frozen II",
        "updated_at": "2021-03-04 12:31:53.654965"
    },
    "success": true
}
```
### Demo

- [Link](https://casting-ag.herokuapp.com/)


