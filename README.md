# Movie Watchlist API

A RESTful API for managing movie watchlists built with FastAPI. Users can retrieve, add, and remove movies from their personal watchlists with full validation and error handling.

## Features

- Retrieve user's watchlist with full movie details
- Add movies to watchlist with duplicate prevention
- Remove movies from watchlist
- Input validation using Pydantic models
- Asynchronous operations with asyncio
- Comprehensive unit tests with pytest
- Docker support for easy deployment

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Python 3.11** - Asynchronous programming with asyncio
- **pytest** - Testing framework
- **Docker** - Containerization

## Project Structure

```
fastapi-movie-watchlist/
├── main.py                 # FastAPI application and endpoints
├── movies.json            # Movie data
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore         # Docker ignore rules
├── tests/
│   └── test_main.py     # Unit tests
└── README.md
```

## API Endpoints

### Get All Movies
```http
GET /movies
```
Returns a list of all available movies.

**Response:** `200 OK`
```json
[
  {
    "id": "tt0111161",
    "title": "The Shawshank Redemption",
    "year": 1994,
    "genres": ["drama"],
    "plot": "Two imprisoned men bond over a number of years..."
  }
]
```

### Get User's Watchlist
```http
GET /watchlist/{user_id}
```
Retrieves all movies in a user's watchlist.

**Response:** `200 OK`
```json
[
  {
    "id": "tt0111161",
    "title": "The Shawshank Redemption",
    "year": 1994,
    "genres": ["drama"],
    "plot": "Two imprisoned men bond over a number of years..."
  }
]
```

### Add Movie to Watchlist
```http
POST /watchlist/{user_id}
```

**Request Body:**
```json
{
  "movie_id": "tt0111161"
}
```

**Response:** `200 OK`
```json
{
  "message": "Movie added successfully",
  "watchlist": [...]
}
```

**Error Responses:**
- `404 Not Found` - Movie does not exist
- `400 Bad Request` - Movie already in watchlist

### Remove Movie from Watchlist
```http
DELETE /watchlist/{user_id}/{movie_id}
```

**Response:** `200 OK`
```json
{
  "message": "Movie removed successfully",
  "watchlist": [...]
}
```

**Error Responses:**
- `404 Not Found` - User has no watchlist or movie not in watchlist

## Getting Started

### Prerequisites

- Python 3.11+
- pip

### Installation & Running Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/rodrick-mpofu/fastapi-movie-watchlist.git
   cd fastapi-movie-watchlist
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate (Windows Git Bash)
   source venv/Scripts/activate

   # Activate (Mac/Linux)
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## Running with Docker

### Prerequisites
- Docker
- Docker Compose

### Steps

1. **Build and run the container**
   ```bash
   docker compose up --build
   ```

2. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs

3. **Stop the container**
   ```bash
   # Press Ctrl+C, then:
   docker compose down
   ```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py -v
```

## API Usage Examples

### Using curl

```bash
# Get all movies
curl http://localhost:8000/movies

# Get user's watchlist
curl http://localhost:8000/watchlist/user_123

# Add movie to watchlist
curl -X POST "http://localhost:8000/watchlist/user_123" \
  -H "Content-Type: application/json" \
  -d '{"movie_id": "tt0111161"}'

# Remove movie from watchlist
curl -X DELETE "http://localhost:8000/watchlist/user_123/tt0111161"
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Get all movies
response = requests.get(f"{BASE_URL}/movies")
movies = response.json()

# Add movie to watchlist
response = requests.post(
    f"{BASE_URL}/watchlist/user_123",
    json={"movie_id": "tt0111161"}
)
result = response.json()
```

## Development

### Code Quality
- Clean, modular code structure
- Comprehensive error handling
- Type hints throughout
- Async/await patterns for I/O operations

### Testing
- Unit tests for all endpoints
- Edge case coverage
- Database reset between tests

## Future Enhancements

- [ ] Persistent database (PostgreSQL/MongoDB)
- [ ] User authentication and authorization
- [ ] Movie rating and review system
- [ ] Search and filter movies
- [ ] Pagination for large watchlists

## License

This project is part of a take-home coding challenge.

## Author

Rodrick Mpofu