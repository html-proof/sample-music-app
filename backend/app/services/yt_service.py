import yt_dlp
import logging
from typing import List, Optional, Dict, Any
import time
from app.utils.cache import cache

logger = logging.getLogger(__name__)

class YTService:
    def __init__(self):
        self.ydl_opts_search = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist', # Don't extract full info for speed in search
            'skip_download': True,
            'ignoreerrors': True,
        }
        
        self.ydl_opts_stream = {
            'format': 'bestaudio/best', # High quality audio
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }

    def _score_video(self, title: str, duration: int, channel: str) -> int:
        """
        Scores a video to determine if it's a high-quality music track.
        Higher score = better match.
        """
        title_lower = title.lower()
        score = 0
        
        # Block words (Severe penalty)
        BLOCK_WORDS = [
            "trailer", "teaser", "reaction", "interview", "dialogue", "scene", 
            "bgm", "remix", "cover", "shorts", "status", "video song", # sometimes video song is okay, but we prefer audio
            "full movie", "movie review", "podcast", "episode", "discussion",
            "8d", "16d", "3d", "slowed", "reverb", "bass boosted", "nightcore",
            "mashup", "karaoke", "instrumental" 
        ]
        
        for w in BLOCK_WORDS:
            if w in title_lower:
                score -= 50 # Heavy penalty

        # Boost words (Reward)
        BOOST_WORDS = [
            "official audio", "lyrical", "full song", "soundtrack", "audio", 
            "original", "topic" # Artist - Topic
        ]
        
        for w in BOOST_WORDS:
            if w in title_lower:
                score += 10
        
        # Duration scoring
        if duration:
            if 120 <= duration <= 420: # 2 to 7 mins
                score += 10
            elif duration < 60: # Shorts/Snippets
                score -= 20
            elif duration > 720: # > 12 mins (likely jukebox/full movie)
                score -= 10
        
        # Channel Trust (Heuristic)
        if "topic" in channel.lower() or "vevo" in channel.lower() or "records" in channel.lower():
            score += 5
            
        return score

    async def search_videos(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Searches YouTube, filters, scores, and returns top N clean results.
        """
        try:
            # Fetch more results to allow for filtering
            fetch_limit = 50 
            search_query = f"ytsearch{fetch_limit}:{query}" 
            
            with yt_dlp.YoutubeDL(self.ydl_opts_search) as ydl:
                info = ydl.extract_info(search_query, download=False)
                
            candidates = []
            if 'entries' in info:
                for entry in info['entries']:
                    title = entry.get('title', '')
                    duration = entry.get('duration', 0)
                    channel = entry.get('uploader', '')
                    video_id = entry.get('id')
                    
                    if not title or not video_id:
                        continue

                    score = self._score_video(title, duration, channel)
                    
                    # Threshold for accepting a video as "music"
                    # We can adjust this. 
                    # If score is too low, we skip.
                    if score > -10: 
                        candidates.append({
                            "id": video_id,
                            "title": title,
                            "artist": channel, # Use uploader as artist roughly
                            "duration": duration,
                            "thumbnail": entry.get('thumbnail', ''),
                            "yt_video_id": video_id,
                            "score": score
                        })
            
            # Sort by score descending
            candidates.sort(key=lambda x: x['score'], reverse=True)
            
            # Return top N
            return candidates[:limit]

        except Exception as e:
            logger.error(f"YT Search Error: {e}")
            return []

    async def get_stream_url(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Gets the direct stream URL for a video ID with Redis caching.
        Cache TTL: 10 minutes for premium performance.
        """
        start_time = time.time()
        cache_key = f"yt_audio:{video_id}"
        
        # Try cache first
        cached_data = await cache.get(cache_key)
        if cached_data:
            fetch_time = int((time.time() - start_time) * 1000)
            logger.info(f"⚡ Cache HIT for {video_id} ({fetch_time}ms)")
            cached_data['cached'] = True
            cached_data['fetch_time_ms'] = fetch_time
            return cached_data
        
        # Cache miss - fetch from YouTube
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            with yt_dlp.YoutubeDL(self.ydl_opts_stream) as ydl:
                info = ydl.extract_info(url, download=False)
                
                stream_data = {
                    "video_id": video_id,
                    "stream_url": info.get('url'),
                    "duration": info.get('duration'),
                    "title": info.get('title'),
                    "artist": info.get('uploader'),
                    "thumbnail": info.get('thumbnail'),
                    "cached": False,
                    "fetch_time_ms": int((time.time() - start_time) * 1000)
                }
                
                # Cache for 10 minutes (600 seconds)
                await cache.set(cache_key, stream_data, ttl=600)
                
                logger.info(f"🔄 Cache MISS for {video_id} ({stream_data['fetch_time_ms']}ms) - Cached for 10min")
                return stream_data
                
        except Exception as e:
            logger.error(f"YT Stream Error for {video_id}: {e}")
            return None

yt_service = YTService()
