from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth, search, stream, user, library, playlist, recommendations, player, admin, ws, test
from app.firebase import initialize_firebase

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# CORS Middleware
origins = [
    "http://localhost:3000",
    "http://localhost:5173", # Vite default
    # Add production domains
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(search.router)
app.include_router(stream.router)
app.include_router(user.router)
app.include_router(library.router)
app.include_router(playlist.router)
app.include_router(recommendations.router)
app.include_router(player.router)
app.include_router(admin.router)
app.include_router(ws.router)
app.include_router(test.router)  # Test endpoints (remove in production)

@app.on_event("startup")
async def startup_event():
    initialize_firebase()

@app.get("/")
async def root():
    return {"status": "ok", "service": settings.APP_NAME}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
