import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import implicit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.services.user_service import user_service
import os
import pickle
import logging

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self.model = None
        self.user_map = {}
        self.item_map = {}
        self.reverse_item_map = {}
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.model_path = "models/als_model.pkl"
        
        if not os.path.exists("models"):
            os.makedirs("models")
            
        # Try loading existing model on init
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                    # Use a flexible loading structure
                    if len(data) >= 4:
                        self.model = data[0]
                        self.user_map = data[1]
                        self.item_map = data[2]
                        self.reverse_item_map = data[3]
            except Exception as e:
                logger.error(f"Failed to load ML model: {e}")

    async def train_als_model(self):
        """
        Fetches interaction data from UserService (Firebase) and trains the ALS model.
        """
        interactions = await user_service.get_all_interactions()
        if not interactions:
            logger.warning("No interactions found for training.")
            return

        df = pd.DataFrame(interactions)
        
        # Simple implicit feedback weighing
        # plays=1, likes=5, skips=-1 ?
        # Ideally, 'weight' column should be pre-calculated or done here.
        if 'weight' not in df.columns:
            df['weight'] = 1 # Default weight

        # Create mappings
        df['user_cat'] = df['user_id'].astype('category')
        df['item_cat'] = df['video_id'].astype('category')
        
        user_ids = df['user_cat'].cat.codes
        item_ids = df['item_cat'].cat.codes
        
        self.user_map = dict(enumerate(df['user_cat'].cat.categories))
        self.item_map = {id: i for i, id in enumerate(df['item_cat'].cat.categories)}
        self.reverse_item_map = {i: id for id, i in self.item_map.items()}
        
        matrix = csr_matrix((df['weight'], (item_ids, user_ids)))
        
        # Train
        self.model = implicit.als.AlternatingLeastSquares(factors=50, iterations=20, regularization=0.1)
        self.model.fit(matrix)
        
        # Save
        with open(self.model_path, 'wb') as f:
            pickle.dump((self.model, self.user_map, self.item_map, self.reverse_item_map), f)
            
        logger.info("ALS Model trained and saved.")

    def get_recommendations(self, user_id: str, n=10) -> list:
        if self.model is None:
            return []

        # Reverse lookup for user index
        reverse_user_map = {v: k for k, v in self.user_map.items()}
        if user_id not in reverse_user_map:
            return []
            
        user_idx = reverse_user_map[user_id]
        
        try:
            # recommend returns (ids, scores)
            ids, scores = self.model.recommend(user_idx, csr_matrix((1, len(self.item_map))), N=n)
            return [self.reverse_item_map.get(idx) for idx in ids if idx in self.reverse_item_map]
        except Exception as e:
            logger.error(f"Recommendation error: {e}")
            return []

    def get_content_similarity(self, song_title: str, artist: str, n=5) -> list:
        """
        Fallback content-based similarity using TF-IDF on title+artist strings.
        Realistically needs a corpus of songs. For now, we mock or return empty 
        if we don't have a loaded song metadata db.
        """
        return []

ml_service = MLService()
