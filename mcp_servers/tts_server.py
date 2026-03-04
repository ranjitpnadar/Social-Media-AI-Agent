import os
from mcp.server.fastmcp import FastMCP
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

from models.schemas import TTSInput
load_dotenv()  # Load environment variables from .env file

# 1. Initialize the MCP Server
mcp = FastMCP("SocialMediaAgentServer")

# 2. Expose the TTS Tool to any connecting MCP Client
@mcp.tool()
def generate_audio(text: str, voice_name: str) -> str:
    """Converts written text into spoken audio."""
    try:
        # The client automatically picks up ELEVENLABS_API_KEY from your loaded .env
        client = ElevenLabs() 
        
        # 1. Map the human-readable names to actual ElevenLabs Voice IDs
        voice_ids = {
            "Adam": "pNInz6obpgDQGcFmaJgB",
            "Rachel": "21m00Tcm4TlvDq8ikWAM",
            "Bella": "EXAVITQu4vr4xnSDxMaL",
            "Antoni": "ErXwobaYiN019PkySvjV"
        }
        
        # Safely get the ID, defaulting to Rachel if the LLM hallucinates a name
        selected_id = voice_ids.get(voice_name, "21m00Tcm4TlvDq8ikWAM")
        
        # 2. Use the updated v1.0 syntax: text_to_speech.convert
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id=selected_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, "daily_story.mp3")
        
        # 3. Save the byte stream to a file
        with open(file_path, "wb") as f:
            for chunk in audio_stream:
                if chunk:
                    f.write(chunk)
                    
        return f"Success: Audio saved to {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"