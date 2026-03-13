# Liquid Labs Stock Summary API

## Description

This is a FastAPI-based application that provides annual stock summary data for given stock symbols and years. The application fetches data from the Alpha Vantage API, calculates yearly summaries (high, low, volume), and caches the results in a local SQLite database for faster subsequent access.

The API exposes an endpoint to retrieve stock summaries, ensuring efficient data retrieval and storage.

## Features

- Fetch and cache stock data from Alpha Vantage API
- Calculate annual stock summaries (high, low, volume)
- SQLite database for data persistence
- FastAPI framework for building the REST API
- Asynchronous request handling

## Prerequisites

- Python 3.11 or higher
- Poetry for dependency management
- An Alpha Vantage API key (sign up at [Alpha Vantage](https://www.alphavantage.co/support/#api-key))

## Setup

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Install dependencies**:
   ```
   poetry install
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory of the project with the following variables:
   ```
   alphavantage_api_key=YOUR_API_KEY_HERE
   db=stock_data.db
   ```
   - Replace `YOUR_API_KEY_HERE` with your actual Alpha Vantage API key.
   - The `db` variable specifies the path to the SQLite database file. You can change it if needed.

## Running the Application

### Run the Database

The database is SQLite-based and will be automatically created when the application runs. No separate setup is required for the database.

### Run the API

To run the API in development mode with auto-reload:
```
poetry run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

To run the API in production mode:
```
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://127.0.0.1:8000` (or `http://localhost:8000` in production).

You can find swagger documentation http://127.0.0.1:8000/docs#/

### API Endpoints

- `GET /`: Root endpoint returning a hello message.
- `GET /symbols/{symbol}/annual/{year}`: Get the annual stock summary for a given symbol and year.

Example request:
```
GET http://127.0.0.1:8000/symbols/AAPL/annual/2023
```

## Building the Application

To build the application package:
```
poetry build
```

This will create a `dist/` directory with the built package.

## Deployment

For deployment, you can use any ASGI server like Uvicorn, Gunicorn with Uvicorn workers, or deploy to cloud platforms like Heroku, AWS, etc.

Example with Gunicorn:
```
poetry run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

Ensure the `.env` file is properly configured in your deployment environment.

## Project Structure

- `main.py`: Entry point for the FastAPI application.
- `settings.py`: Configuration settings using Pydantic.
- `routes/stock_summary.py`: API routes for stock summary endpoints.
- `auxiliary/stock_summary.py`: Business logic for fetching and calculating stock summaries.
- `clients/api.py`: HTTP client for API requests.
- `database/db.py`: Database connection and operations.
- `models/alpha_response.py`: Pydantic models for API responses.

