from models.state import AgentState
from services.facebook_service import post_to_facebook_page

import os

def facebook_publisher_node(state: AgentState) -> dict:
    print("\n--- 📘 FACEBOOK PUBLISHER WORKING ---")
    
    story_text = state.get("story_text")
    topic = state.get("topic", "Daily Short Story")
    
    if not story_text:
        error_msg = "No story text provided to the Facebook Publisher."
        print(f"❌ {error_msg}")
        return {"error": error_msg}

    # Format the content specifically for the Facebook Page
    fb_post_content = f"📖 {topic}\n\n{story_text}\n\n#StoryTime #AutonomousAgent"
    
    print(f"Publishing to Facebook Page 'aaa' (ID: {os.getenv('FB_AAA_PAGE_ID')})...")
    
    # Execute the service
    result = post_to_facebook_page(fb_post_content)
    
    # Meta's API returns an 'id' upon successful creation
    if "id" in result:
        post_id = result["id"]
        print(f"✅ Successfully published to Facebook! Post ID: {post_id}")
        return {"facebook_post_id": post_id}
    else:
        # If it fails, Meta usually returns an 'error' dictionary
        error_details = result.get("error", result)
        print(f"❌ Facebook API Error: {error_details}")
        return {"error": f"Facebook Post Failed: {error_details}"}