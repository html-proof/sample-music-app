from firebase_admin import db
import time
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    async def log_play(self, uid: str, song_data: dict, duration_played: int):
        """
        Logs a play event.
        """
        try:
            event = {
                "type": "play",
                "song_id": song_data.get('id'),
                "artist": song_data.get('artist'),
                "title": song_data.get('title'),
                "duration_played": duration_played,
                "timestamp": int(time.time())
            }
            # Log to RTDB for immediate analysis/dashboard
            db.reference(f'analytics/{uid}/events').push(event)
            
            # Update user's specific history node (calls user_service internally or separately)
            # user_service.add_to_history(uid, song_data)
        except Exception as e:
            logger.error(f"Error logging play: {e}")

    async def log_feedback(self, uid: str, song_id: str, feedback_type: str):
        """
        Logs explicit user feedback (like, dislike, not_relevant).
        feedback_type: 'like', 'dislike', 'not_relevant'
        """
        try:
            event = {
                "type": "feedback",
                "song_id": song_id,
                "feedback": feedback_type,
                "timestamp": int(time.time())
            }
            db.reference(f'analytics/{uid}/feedback').push(event)
            
            # If 'not_relevant', potentially add to a blacklist for this user
            if feedback_type == 'not_relevant':
                db.reference(f'users/{uid}/blacklist').push(song_id)
                
        except Exception as e:
            logger.error(f"Error logging feedback: {e}")

analytics_service = AnalyticsService()
