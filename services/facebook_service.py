import os
import requests

def post_to_facebook_page(message: str) -> dict:
    """Publishes a text post to a specific Facebook Page."""
    
    page_id = os.getenv("FB_AAA_PAGE_ID")
    access_token = os.getenv("META_ACCESS_TOKEN")
    
    if not page_id or not access_token:
        return {"error": "Missing FB_AAA_PAGE_ID or META_ACCESS_TOKEN in environment variables."}

    # The /feed endpoint is used for standard text/link posts on a Page
    url = f"https://graph.facebook.com/{page_id}/feed"
    
    payload = {
        "message": message,
        "access_token": access_token
    }

    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}