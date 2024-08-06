# Backend README

## Installation
```bash
pip install -r requirements.txt
```

## Running the server
```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000

```
Note: The server will be running on http://localhost:8000.
Be sure to run this command from the root directory of the project.

## Running tests
```bash
python3 -m pytest
```

## Generating coverage report
```bash
python3 -m pytest --cov=myproj tests/ 
```

## Postman Workspace
[![Run in Postman](https://run.pstmn.io/button.svg)](https://mp6-backend-api-endpoint-testing.postman.co/workspace/8272030c-3ed4-409e-bf53-b9ae07a682db)

When working with the API in Postman, make sure to choose the correct environment. For local development, use the `Development` environment. For testing the deployed API, use the `Production` environment.