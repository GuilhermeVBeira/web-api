[![Build Status](https://travis-ci.org/GuilhermeVBeira/web-api.svg?branch=main)](https://travis-ci.org/GuilhermeVBeira/web-api)
[![codecov](https://codecov.io/gh/GuilhermeVBeira/sample-fast-api/branch/master/graph/badge.svg)](https://codecov.io/gh/GuilhermeVBeira/web-api)

# web-api
A sample of api with external api dependency

Install dependencies.

We use [poetry](https://poetry.eustace.io/) to manage dependencies, so make sure you have it installed.
```
make install
```
Create .env
```
cp default.env .env
```
After create database test and set on [.env](https://github.com/GuilhermeVBeira/web-api/blob/main/default.env) file
Update the values of databases, PRODUCTS_API and SECRET_KEY

Sync migrations

```
make migrate
```
Create a user

```
make createuser
```

Run
```
make run
```
## How to use
to simplify, the examples bellow use [httpie](https://httpie.org/)


### Authentication

request
```
 http -f POST http://localhost:8000/auth/login username=outrouser password=senha
```
response
```
HTTP/1.1 200 OK
content-length: 178
content-type: application/json
date: Sun, 3 Oct 1991 02:13:05 GMT
server: uvicorn

{
    "access_token": "<TOKEN>",
    "token_type": "bearer"
}
```

### Create client

request
```
 http POST http://localhost:8000/clients/ "Authorization: Bearer <TOKEN>" username=Guilherme email=email@email.com favorite_products:='[{"id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"}]
```
response
```
HTTP/1.1 201 Created
content-length: 363
content-type: application/json
date: Sun, 3 Oct 1991 02:13:05 GMT
server: uvicorn

{
    "email": "email@email.com",
    "favorite_products": [
        {
            "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
            ... and other fields from your api
        }
    ],
    "id": "8a7fb195-81f6-433f-a084-2348977e6950",
    "username": "Guilherme"
}
```

### Update client

request
```
 http PUT http://localhost:8000/clients/7a7fb195-71f6-433f-a084-2348977e6950 "Authorization: Bearer <TOKEN>" username=Guilherme email=updated@email.com favorite_products:='[{"id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"}]'
```
response
```
HTTP/1.1 200 OK
content-length: 368
content-type: application/json
date: Sun, 3 Oct 1991 02:13:05 GMT
server: uvicorn

{
    "email": "updated@email.com",
    "favorite_products": [
        {
            "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
            ... and other fields from your api
        }
    ],
    "id": "7a7fb195-71f6-433f-a084-2348977e6950",
    "username": "Guilherme"
}
```

### List clients

request
```
 http GET http://localhost:8000/clients/ "Authorization: Bearer <TOKEN>"
```
response
```
HTTP/1.1 200 OK
content-length: 2887
content-type: application/json
date: Sun, 3 Oct 1991 02:22:38 GMT
server: uvicorn

[
    {
        "email": "email3@email.com",
        "favorite_products": [
            {...}
        ],
        "id": "2aea592a-45d8-4481-a887-403258bfcb32",
        "username": "client-username"
    },
    {...}
]

```

### Delete client

request
```
 http DELETE http://localhost:8000/clients/<CLIENT-ID> "Authorization: Bearer <TOKEN>"
```
response
```
HTTP/1.1 204 No Content
content-length: 4
content-type: application/json
date: Sun, 3 Oct 1991 02:28:18 GMT
server: uvicorn
```
