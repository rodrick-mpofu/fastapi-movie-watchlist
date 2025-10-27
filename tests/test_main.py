import pytest
from fastapi.testclient import TestClient
from main import app, WATCHLISTS, MOVIES_DATA

# Create a test client
client = TestClient(app)

# Reset database before each test
@pytest.fixture(autouse=True)
def reset_database():
    """Reset the in-memory database before each test"""
    WATCHLISTS.clear()
    yield
    WATCHLISTS.clear()


class TestGetWatchlist:
    """Tests for GET /watchlist/{user_id}"""
    
    def test_get_empty_watchlist(self):
        """Test retrieving watchlist for new user returns empty list"""
        response = client.get("/watchlist/user_123")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_watchlist_with_movies(self):
        """Test retrieving watchlist with movies returns full movie objects"""
        # Setup: Add movies to watchlist directly
        WATCHLISTS["user_123"] = ["tt0111161", "tt0068646"]
        
        response = client.get("/watchlist/user_123")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] == "tt0111161"
        assert data[0]["title"] == "The Shawshank Redemption"


class TestAddToWatchlist:
    """Tests for POST /watchlist/{user_id}"""
    
    def test_add_movie_to_new_user(self):
        """Test adding a movie to a new user's watchlist"""
        response = client.post(
            "/watchlist/user_123",
            json={"movie_id": "tt0111161"}
        )
        assert response.status_code == 201

        data = response.json()
        assert data["message"] == "Movie added successfully"
        assert data["movie"]["id"] == "tt0111161"
        assert data["movie"]["title"] == "The Shawshank Redemption"
    
    def test_add_movie_to_existing_watchlist(self):
        """Test adding a movie to existing watchlist"""
        # Setup: User already has one movie
        WATCHLISTS["user_123"] = ["tt0111161"]

        response = client.post(
            "/watchlist/user_123",
            json={"movie_id": "tt0068646"}
        )
        assert response.status_code == 201
        assert response.json()["movie"]["id"] == "tt0068646"
    
    def test_add_invalid_movie(self):
        """Test adding non-existent movie returns 404"""
        response = client.post(
            "/watchlist/user_123",
            json={"movie_id": "tt9999999"}
        )
        assert response.status_code == 404
        assert "Movie not found" in response.json()["detail"]
    
    def test_add_duplicate_movie(self):
        """Test adding duplicate movie returns 409 Conflict"""
        # Setup: User already has this movie
        WATCHLISTS["user_123"] = ["tt0111161"]

        response = client.post(
            "/watchlist/user_123",
            json={"movie_id": "tt0111161"}
        )
        assert response.status_code == 409
        assert "already in watchlist" in response.json()["detail"]


class TestRemoveFromWatchlist:
    """Tests for DELETE /watchlist/{user_id}/{movie_id}"""
    
    def test_remove_movie_from_watchlist(self):
        """Test removing a movie from watchlist"""
        # Setup: User has movies in watchlist
        WATCHLISTS["user_123"] = ["tt0111161", "tt0068646"]

        response = client.delete("/watchlist/user_123/tt0111161")
        assert response.status_code == 204
        assert response.content == b""

        # Verify movie was actually removed
        assert "tt0111161" not in WATCHLISTS["user_123"]
        assert "tt0068646" in WATCHLISTS["user_123"]
    
    def test_remove_from_nonexistent_user(self):
        """Test removing from non-existent user returns 404"""
        response = client.delete("/watchlist/user_999/tt0111161")
        assert response.status_code == 404
        assert "no watchlist" in response.json()["detail"]
    
    def test_remove_movie_not_in_watchlist(self):
        """Test removing movie not in watchlist returns 404"""
        # Setup: User exists but doesn't have this movie
        WATCHLISTS["user_123"] = ["tt0068646"]
        
        response = client.delete("/watchlist/user_123/tt0111161")
        assert response.status_code == 404
        assert "not in watchlist" in response.json()["detail"]