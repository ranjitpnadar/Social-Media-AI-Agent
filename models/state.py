from typing import TypedDict, Optional

class AgentState(TypedDict):
    topic: Optional[str]
    voice_name: Optional[str]
    creative_prompt: Optional[str]
    story_text: Optional[str]
    audio_file_path: Optional[str]
    error: Optional[str]