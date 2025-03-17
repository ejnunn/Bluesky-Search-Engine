import json
from atproto import Client
from pydantic import BaseModel, ValidationError, Field
from typing import List, Optional

# Pydantic models for validation
class Embed(BaseModel):
    type: str = Field(..., alias="$type")
    images: Optional[List[dict]] = None
    video: Optional[dict] = None
    external: Optional[dict] = None

class ActorFeedResponse(BaseModel):
    feed: List[Embed]

class BlueSkyClient:
    def __init__(self, email, password):
        self.client = Client()
        self.profile = self.login(email, password)
    
    def login(self, email, password):
        try:
            profile = self.client.login(email, password)
            print(f"Welcome, {profile.display_name}")
            return profile
        except Exception as e:
            raise ValueError(f"Failed to login: {e}")

    def get_actor_feed(self, actor: str, cursor: str = None, _filter: str = None, limit: int = None):
        try:
            response = self.client.get_author_feed(actor, cursor, _filter, limit)
            print(f"Completed response!")
            return response.feed
        except Exception as e:
            print(f"Response failed... Error: {e}")
            raise Exception(e)

    def filter_posts(self, posts):
        """
        Filters a list of Bluesky posts (from a feed) to only include the necessary attributes to store in the DB.
        This includes author_handle, the post's text, and the timestamp it was posted.
        """
        filtered_results = []
        for post_object in posts:
            post = post_object.post
            author_handle = post.author.handle
            record = post.record
            text = record.text
            created_at = record.created_at

            filtered_results.append((author_handle, text, created_at))

        return filtered_results