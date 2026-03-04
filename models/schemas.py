from pydantic import BaseModel, Field

class TTSInput(BaseModel):
    """MCP-style schema enforcing strict input for the TTS service."""
    text: str = Field(..., description="The finalized story text to be synthesized into audio.")
    voice_name: str = Field("Rachel", description="The name of the voice to use for synthesis. Defaults to 'Rachel'.")
