from typing import TypedDict, Optional, Any

class AgentState(TypedDict):
    topic: Optional[str]
    voice_name: Optional[str]
    creative_prompt: Optional[str]
    story_text: Optional[str]
    audio_file_path: Optional[str]
    image_details: Any
    video_details: Any
    facebook_post_id: Optional[str] 
    error: Optional[str]