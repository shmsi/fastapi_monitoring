
from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import redis

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Initialize the rate limiter
FastAPILimiter.init(storage_uri=redis_client)


# Create a rate limiter dependency
limiter = RateLimiter(limit="10/minute")

# Prometheus metrics
requests_counter = Counter("fastapi_requests_total", "Total number of requests to the FastAPI application")

# Dummy database to store user information
db = []

# Data model for user info
class UserInfo:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

# Endpoint to create a new user
@app.post("/create_user")
async def create_user(username: str, email: str, limited: bool = Depends(limiter)):
    requests_counter.inc()
    new_user = UserInfo(username=username, email=email)
    db.append(new_user)
    return {"message": "User created successfully"}

# Endpoint to get user info by username
@app.get("/get_user/{username}")
async def get_user(username: str, limited: bool = Depends(limiter)):
    requests_counter.inc()
    user = next((user for user in db if user.username == username), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username, "email": user.email}

# Endpoint to expose Prometheus metrics
@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
