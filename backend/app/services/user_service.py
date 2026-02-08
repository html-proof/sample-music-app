from firebase_admin import firestore, db
import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self._db = None
        self._collection = None

    @property
    def db(self):
        if self._db is None:
            self._db = firestore.client()
        return self._db

    @property
    def collection(self):
        if self._collection is None:
            self._collection = self.db.collection('users')
        return self._collection

    async def get_user_profile(self, uid: str):
        try:
            doc = self.collection.document(uid).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"Error fetching user profile for {uid}: {e}")
            return None

    async def create_user_profile(self, uid: str, email: str, display_name: str = None, photo_url: str = None):
        try:
            doc_ref = self.collection.document(uid)
            doc = doc_ref.get()
            
            if not doc.exists:
                user_data = {
                    "uid": uid,
                    "email": email,
                    "display_name": display_name,
                    "photo_url": photo_url,
                    "created_at": firestore.SERVER_TIMESTAMP,
                }
                doc_ref.set(user_data)
                
                try:
                    ref = db.reference(f'users/{uid}')
                    ref.set({
                        'profile': user_data,
                        'state': {'status': 'idle'},
                        'queue': []
                    })
                except Exception as rtdb_error:
                    logger.error(f"Error initializing RTDB for {uid}: {rtdb_error}")

                logger.info(f"Created new user profile for {uid}")
                return user_data
            else:
                return doc.to_dict()
        except Exception as e:
            logger.error(f"Error creating user profile for {uid}: {e}")
            raise e

    async def save_onboarding_data(self, uid: str, data: dict):
        try:
            required = ['country', 'language', 'artists', 'modes']
            if not all(k in data for k in required):
                raise ValueError("Missing onboarding fields")
            
            ref = self.collection.document(uid)
            ref.update({"onboarding": data})
            
            rtdb_ref = db.reference(f'users/{uid}/preferences')
            rtdb_ref.set(data)
            
            logger.info(f"Saved onboarding data for {uid}")
            return True
        except Exception as e:
            logger.error(f"Error saving onboarding for {uid}: {e}")
            raise e
            
    async def update_playback_state(self, uid: str, state: dict):
        try:
            ref = db.reference(f'users/{uid}/state')
            ref.update(state)
        except Exception as e:
            logger.error(f"Error updating playback state for {uid}: {e}")

    async def add_to_history(self, uid: str, song: dict):
        try:
            ref = db.reference(f'users/{uid}/history')
            new_ref = ref.push(song)
        except Exception as e:
            logger.error(f"Error adding to history for {uid}: {e}")

    async def get_all_interactions(self):
        """
        Fetch all interactions (plays) for ML training.
        """
        try:
            ref = db.reference('users')
            snapshot = ref.get()
            if not snapshot:
                return []
                
            interactions = []
            for user_id, user_data in snapshot.items():
                history = user_data.get('history', {})
                # History here is a dict of push_ids -> song_data
                for entry_id, song_data in history.items():
                    interactions.append({
                        'user_id': user_id,
                        'video_id': song_data.get('id'), # Assumes 'id' is stored
                        'weight': 1 # Play = 1
                    })
            return interactions
        except Exception as e:
            logger.error(f"Error fetching all interactions: {e}")
            return []

    async def get_recent_history(self, uid: str, limit: int = 20):
        try:
            ref = db.reference(f'users/{uid}/history')
            snapshot = ref.order_by_key().limit_to_last(limit).get()
            if not snapshot:
                return []
            return list(snapshot.values())
        except Exception as e:
            logger.error(f"Error fetching history for {uid}: {e}")
            return []

user_service = UserService()
