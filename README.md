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

- Docker
- An Alpha Vantage API key (sign up at [Alpha Vantage](https://www.alphavantage.co/support/#api-key))

## Build and Run with Docker

1. **Build the Docker image**:

   ```
   docker build -t liquid-labs .
   ```

2. **Run the container**:

   Set your Alpha Vantage API key as an environment variable:

   ```
   docker run -p 8000:8000 -e ALPHAVANTAGE_API_KEY=YOUR_API_KEY_HERE -e DB=stocks.db liquid-labs
   ```

   Replace `YOUR_API_KEY_HERE` with your actual Alpha Vantage API key.

The API will be available at `http://localhost:8000`.

You can find the Swagger documentation at `http://localhost:8000/docs`.

## Development Setup

If you prefer to run the application locally for development:

### Prerequisites

- Python 3.11 or higher
- Poetry for dependency management
- An Alpha Vantage API key (sign up at [Alpha Vantage](https://www.alphavantage.co/support/#api-key))

### Setup

1. **Install Poetry** (if not already installed):

   ```
   pip install poetry
   ```

.

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Install dependencies**:

   ```
   poetry install
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory with the following variables:

   ```
   alphavantage_api_key=YOUR_API_KEY_HERE
   db=stocks.db
   ```

   Replace `YOUR_API_KEY_HERE` with your actual Alpha Vantage API key.

### Running the Application

To run the API in development mode with auto-reload:

```
poetry run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

If you need to run with VSCode debugger, select the Python interpreter from the Poetry virtual environment:

1. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`).
2. Select `Python: Select Interpreter`.
3. Choose the interpreter from the Poetry environment .

## API Endpoints

- `GET /`: Root endpoint returning a hello message.
- `GET /symbols/{symbol}/annual/{year}`: Get the annual stock summary for a given symbol and year.

Example request:

```
GET http://localhost:8000/symbols/AAPL/annual/2023
```

## Project Structure

- `main.py`: Entry point for the FastAPI application.
- `settings.py`: Configuration settings using Pydantic.
- `routes/stock_summary.py`: API routes for stock summary endpoints.
- `auxiliary/stock_summary.py`: Business logic for fetching and calculating stock summaries.
- `clients/api.py`: HTTP client for API requests.
- `database/db.py`: Database connection and operations.
- `models/alpha_response.py`: Pydantic models for API responses.