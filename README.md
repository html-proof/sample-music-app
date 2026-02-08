# 🎵 Sample Music App

Spotify-Premium-style music streaming application with instant playback, Redis caching, and Firebase backend.

## 🚀 Features

- ⚡ **Instant Streaming** - Direct audio URLs from YouTube (no downloads)
- 💾 **Redis Caching** - 10-minute TTL, < 50ms response times
- 🎯 **Smart Filtering** - AI-powered music quality scoring
- 🔐 **Firebase Auth** - Secure user authentication
- 📊 **Real-time Updates** - WebSocket support for live playback state
- 🚂 **Railway Ready** - One-click deployment

## 📁 Project Structure

```
sample-music/
├── backend/          # FastAPI backend
│   ├── app/         # Application code
│   ├── tests/       # Test suite
│   ├── Dockerfile   # Production container
│   └── README.md    # Backend documentation
├── models/          # Shared data models
└── dataconnect/     # Firebase Data Connect
```

## 🛠️ Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

See [backend/README.md](backend/README.md) for detailed setup instructions.

## 🚂 Deploy to Railway

1. Push to GitHub
2. Connect Railway to this repo
3. Add Redis plugin
4. Deploy automatically

## 📝 License

MIT
