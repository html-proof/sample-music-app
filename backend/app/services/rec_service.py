from app.services.yt_service import yt_service
from app.services.user_service import user_service
from app.services.ml_service import ml_service
from app.services.classifier_service import classifier_service
import random

class RecService:
    async def get_home_recommendations(self, uid: str):
        """
        Generates the 'Home' view content.
        Uses ML model if available, otherwise fallback heuristics.
        """
        profile = await user_service.get_user_profile(uid)
        onboarding = profile.get('onboarding', {})
        
        # 1. Jump Back In
        jump_back_in = await user_service.get_recent_history(uid, limit=10)
        
        # 2. Made For You (ML + Favorites)
        made_for_you = []
        
        # Try ML first
        ml_recs = ml_service.get_recommendations(uid, n=10)
        if ml_recs:
            # ml_recs are IDs, need to fetch metadata (mocked here or via Search)
            for vid in ml_recs:
                 # Ideally we should have metadata service. For now, search by ID fallback
                 res = await yt_service.search_videos(vid, limit=1)
                 if res: made_for_you.append(res[0])
        
        # Fallback to artists if ML empty
        if not made_for_you:
            fav_artists = onboarding.get('artists', [])
            if fav_artists:
                seed_artist = random.choice(fav_artists)
                made_for_you = await yt_service.search_videos(f"{seed_artist} mix", limit=10)
            
        # 3. Trending (Global)
        trending = await yt_service.search_videos("Global Top 50 Music", limit=10)
        
        return {
            "jump_back_in": jump_back_in,
            "made_for_you": made_for_you,
            "trending": trending
        }

    async def generate_smart_queue(self, current_song: dict, history: list, limit: int = 20):
        """
        Generates a 'Next Up' queue based on the current song.
        Uses ML similarity or Heuristic fallbacks.
        """
        # Heuristic: Search for "Related" or "Mix"
        query = f"{current_song.get('artist')} {current_song.get('title')} official radio"
        candidates = await yt_service.search_videos(query, limit=50)
        
        queue = []
        artist_counts = {}
        played_ids = {h.get('id') for h in history if h.get('id')}
        
        for song in candidates:
            vid = song.get('id')
            artist = song.get('artist', 'Unknown')
            
            # Anti-repetition
            if vid in played_ids: continue
            if any(q.get('id') == vid for q in queue): continue
            
            # Classify Channel Trust (Optional check)
            # trust = await classifier_service.classify_channel(song.get('uploader_url', ''), [])
            # if trust['channel_type'] == 'spam': continue

            # Artist Variety
            if artist_counts.get(artist, 0) >= 3: continue
            
            queue.append(song)
            artist_counts[artist] = artist_counts.get(artist, 0) + 1
            
            if len(queue) >= limit: break
                
        return queue

rec_service = RecService()
