class PlaylistService:
    async def create_playlist(self, uid: str, name: str):
        # Implementation to create playlist in DB
        return {"id": "new_id", "name": name, "owner_uid": uid}

    async def add_song_to_playlist(self, playlist_id: str, song_id: str):
        # Implementation to add song
        return True

playlist_service = PlaylistService()
