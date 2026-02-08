from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    uid: str
    email: str
    display_name: Optional[str] = None
    photo_url: Optional[str] = None

class Song(BaseModel):
    id: str
    title: str
    artist: str
    album: Optional[str] = None
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    yt_video_id: str
    # Add other fields as per blueprint

class Playlist(BaseModel):
    id: str
    name: str
    owner_uid: str
    songs: List[str] = [] # List of song IDs

class PlaybackState(BaseModel):
    song_id: str
    position: int
    is_playing: bool
    device_id: str
