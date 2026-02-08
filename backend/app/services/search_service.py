from app.services.yt_service import yt_service

class SearchService:
    def _normalize_string(self, s: str) -> str:
        """Helper to normalize strings for comparison"""
        import re
        if not s: return ""
        # Remove brackets, non-alphanumeric, etc.
        s = re.sub(r"[\(\[].*?[\)\]]", "", s) # Remove content inside brackets
        s = re.sub(r"[^a-zA-Z0-9\s]", "", s) # Remove special chars
        return s.lower().strip()

    def _is_duplicate(self, item1: dict, item2: dict) -> bool:
        """Checks if two items are likely the same song"""
        # 1. Duration check (within 10s)
        dur1 = item1.get('duration', 0)
        dur2 = item2.get('duration', 0)
        if abs(dur1 - dur2) > 10:
            return False
            
        # 2. Title similarity (Exact match on normalized)
        t1 = self._normalize_string(item1.get('title'))
        t2 = self._normalize_string(item2.get('title'))
        
        return t1 == t2

    async def search(self, query: str, limit: int = 10):
        # Hybrid search logic (Firebase + YT)
        # Fetch raw candidates from YT Service (which already scores them)
        raw_results = await yt_service.search_videos(query, limit=50) # Fetch more to dedupe
        
        unique_results = []
        
        for item in raw_results:
            is_dup = False
            for existing in unique_results:
                if self._is_duplicate(item, existing):
                    is_dup = True
                    break
            
            if not is_dup:
                unique_results.append(item)
                
            if len(unique_results) >= limit:
                break
                
        return {"results": unique_results}

search_service = SearchService()
