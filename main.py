import asyncio
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Data Models
class Movie(BaseModel):
    id: str
    title: str
    year: int
    genres: list[str]
    plot: str


class WatchlistAddRequest(BaseModel):
    movie_id: str


# Database (In-Memory)
with open("movies.json") as f:
    MOVIES_DATA: list[Movie] = [Movie.model_validate(m) for m in json.load(f)]

# A simple in-memory "database" to store user watchlists.
# The key is a user_id (string), and the value is a list of movie IDs (strings).
WATCHLISTS: dict[str, list[str]] = {}

# API Endpoints
# TODO: Implement the following endpoints.
app = FastAPI()

@app.get("/movies")
async def get_all_movies() -> list[Movie]:
    """
    Returns a list of all available movies.
    """

    # Simulate network latency
    await asyncio.sleep(1)

    return MOVIES_DATA

@app.get("/watchlist/{user_id}")
async def get_watchlist(user_id: str):
    """
    Retrieves the watchlist for a given user.
    """
    
    movie_ids = WATCHLISTS.get(user_id, [])
    
    # get the movies for the given movie ids
    watchlist_movies = [
        movie for movie in MOVIES_DATA 
        if movie.id in movie_ids
    ]
    
    return watchlist_movies

@app.post("/watchlist/{user_id}")
async def add_to_watchlist(user_id: str, add_request: WatchlistAddRequest):
    """
    Adds a movie to a user's watchlist.
    """

    # 1. Validate: Does this movie exist?
    movie_exists = any(movie.id == add_request.movie_id for movie in MOVIES_DATA)
    if not movie_exists:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # 2. Initialize user's watchlist if it doesn't exist
    if user_id not in WATCHLISTS:
        WATCHLISTS[user_id] = []
    
    # 3. Check for duplicates
    if add_request.movie_id in WATCHLISTS[user_id]:
        raise HTTPException(status_code=400, detail="Movie already in watchlist")
    
    # 4. Add the movie
    WATCHLISTS[user_id].append(add_request.movie_id)
    
    # 5. Convert IDs to full Movie objects
    watchlist_movies = [
        movie for movie in MOVIES_DATA 
        if movie.id in WATCHLISTS[user_id]
    ]
    
    # 6. Return success with updated watchlist
    return {"message": "Movie added successfully", "watchlist": watchlist_movies}
    

@app.delete("/watchlist/{user_id}/{movie_id}")
async def remove_from_watchlist(user_id: str, movie_id: str):
    """
    Removes a movie from a user's watchlist.
    """
    raise NotImplementedError
