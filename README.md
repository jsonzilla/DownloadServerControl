# Download Server

This project was generated via [manage-fastapi](https://ycd.github.io/manage-fastapi/)! :tada:

## License

This project is licensed under the terms of the Apache license.

# Install the requirements:
A mongo database is required to run the server.
Get one from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas), for free.
```bash
pip install -r requirements.txt
```

## Run
```bash
uvicorn app.main:app --reload
```

## Test
```bash
python -m pytest -W ignore::DeprecationWarning
pytest --cov=app --cov-report=html
python -m pytest_watch
```

## [Config .env](https://fastapi.tiangolo.com/advanced/settings/#reading-a-env-file)
Configure the location of your MongoDB database in a .env file:
```
MONGO_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"
BUCKET_NAME="configzero-jsonzilla"
```

Need to create a user at database to run the server:
```
mongo <db> --eval "db.users({username: '<username>', password: '<bcrypt_password>', email: '<email@email>'});"
```

## Swagger
To see the Swagger documentation, visit:
http://localhost:8000/docs


## Documentation of libraries
To see the documentation, visit:
* [FastAPI](https://fastapi.tiangolo.com/)
* [MongoDB](https://www.mongodb.com/)
* [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
* [Pydantic](https://pydantic-docs.helpmanual.io/)

## WIP
* Automated tests
* S3 is not yet implemented.
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html