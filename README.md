
# Coding interview flashcards

Backend part of the study tool for interview preparation


## Built in

- FastAPI
- SQLAlchemy

## Environment Variables

To run this project, you will need to add the following environment variables to your src/.env file

`POSTGRES_DB`

`POSTGRES_PASSWORD`

`POSTGRES_USER`

`POSTGRES_HOST`

`POSTGRES_PORT`

`SECRET_AUTH`

`ALLOWED_HOSTS` = localhost 127.0.0.1


## Run Locally

Clone the project

```bash
  git clone https://github.com/Persepha/Coding-interview-flashcards.git
```

Go to the project directory

```bash
  cd Coding-interview-flashcards
```

Create virtual environment

```bash
    python -m venv env
```

```bash
    env\Scripts\Activate
```

Build the images and run the containers:

```bash
  make pip-install-dev
```

```bash
  make pip-update
```

```bash
  make build-server
```


Test it out at http://localhost:8000. 
## Documentation


You can see docs at 

http://127.0.0.1:8000/docs


