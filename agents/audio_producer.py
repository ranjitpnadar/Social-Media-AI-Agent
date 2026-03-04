# from pathlib import Path
# import sys
# from models.state import AgentState
# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client
# import os

# PROJECT_ROOT = Path(__file__).parent.parent

# async def audio_producer_node(state: AgentState) -> dict:
#     print("\n--- 🎙️ AUDIO PRODUCER (MCP CLIENT) WORKING ---")
    
#     # Safely extract variables from the LangGraph state
#     story_text = state.get("story_text")
#     voice = state.get("voice_name", "Rachel") # Fallback to Rachel if missing
    
#     if not story_text:
#         print("❌ Error: No story text found in state.")
#         return {"error": "No story text provided to audio producer."}

#     # 1. Target the MCP server script
#     server_path = PROJECT_ROOT / "mcp_servers" / "tts_server.py"
    
#     # 3. Convert the Path object to a string for the StdioServerParameters
#     server_path_str = str(server_path.resolve())
    
#     if not server_path.exists():
#         error_msg = f"MCP Server script not found at exactly: {server_path_str}"
#         print(f"❌ {error_msg}")
#         return {"error": error_msg}

#     server_params = StdioServerParameters(
#         command=sys.executable,
#         args=[server_path_str],
#         env=os.environ.copy()
#     )

#     try:
#         print(f"Connecting to MCP Server via stdio...")
#         # 4. Connect and initialize the session
#         async with stdio_client(server_params) as (read, write):
#             async with ClientSession(read, write) as session:
#                 await session.initialize()
                
#                 print(f"Calling 'generate_audio' tool (Voice: {voice})...")
                
#                 # 5. Execute the tool with the exact arguments the server expects
#                 result = await session.call_tool(
#                     name="generate_audio", 
#                     arguments={
#                         "text": story_text,
#                         "voice_name": voice
#                     }
#                 )
                
#                 # 6. Parse the response from the server
#                 tool_output = result.content[0].text
#                 print(f"Server Response: {tool_output}")
                
#                 # Check if the server explicitly returned an Error string
#                 if "Error" in tool_output:
#                     return {"error": tool_output}
                    
#                 return {"audio_file_path": tool_output}
                
#     except Exception as e:
#         error_msg = f"MCP Communication Failed: {str(e)}"
#         print(f"❌ {error_msg}")
#         return {"error": error_msg}

# import os
# from models.state import AgentState
# from elevenlabs import ElevenLabs

# def audio_producer_node(state: AgentState) -> dict:
#     print("\n--- 🎙️ AUDIO PRODUCER WORKING ---")
    
#     # 1. Safely extract variables from the LangGraph state
#     story_text = state.get("story_text")
#     voice_name = state.get("voice_name", "Rachel") # Fallback to Rachel if missing
    
#     if not story_text:
#         error_msg = "No story text provided to audio producer."
#         print(f"❌ {error_msg}")
#         return {"error": error_msg}

#     try:
#         # 2. Initialize the ElevenLabs Client
#         # It automatically looks for ELEVENLABS_API_KEY in your environment variables
#         client = ElevenLabs()
        
#         # 3. Map the human-readable names to actual ElevenLabs Voice IDs
#         voice_ids = {
#             "Adam": "pNInz6obpgDQGcFmaJgB",
#             "Rachel": "21m00Tcm4TlvDq8ikWAM",
#             "Bella": "EXAVITQu4vr4xnSDxMaL",
#             "Antoni": "ErXwobaYiN019PkySvjV"
#         }
        
#         # Get the ID, defaulting to Rachel's ID if the LLM hallucinated a name
#         selected_id = voice_ids.get(voice_name, "21m00Tcm4TlvDq8ikWAM")
        
#         print(f"Generating audio for voice: {voice_name} (ID: {selected_id})...")
        
#         # 4. Request the audio stream using the v1.0+ SDK syntax
#         audio_stream = client.text_to_speech.convert(
#             text=story_text,
#             voice_id=selected_id,
#             model_id="eleven_multilingual_v2",
#             output_format="mp3_44100_128"
#         )
        
#         # 5. Ensure the output directory exists
#         output_dir = "output"
#         os.makedirs(output_dir, exist_ok=True)
        
#         # 6. Save the byte stream to an MP3 file
#         file_path = os.path.join(output_dir, "daily_story.mp3")
#         with open(file_path, "wb") as f:
#             for chunk in audio_stream:
#                 if chunk:
#                     f.write(chunk)
                    
#         print(f"✅ Audio successfully saved to: {file_path}")
#         return {"audio_file_path": file_path}

#     except Exception as e:
#         error_msg = f"ElevenLabs API Generation Failed: {str(e)}"
#         print(f"❌ {error_msg}")
#         return {"error": error_msg}


import os
import edge_tts
from models.state import AgentState

async def audio_producer_node(state: AgentState) -> dict:
    print("\n--- 🎙️ AUDIO PRODUCER WORKING (Edge TTS) ---")
    
    # 1. Safely extract variables from the LangGraph state
    story_text = state.get("story_text")
    voice_name = state.get("voice_name", "Rachel") 
    
    if not story_text:
        error_msg = "No story text provided to audio producer."
        print(f"❌ {error_msg}")
        return {"error": error_msg}

    try:
        # 2. Map your LLM voice names to high-quality Microsoft Azure Neural voices
        voice_ids = {
            "Adam": "en-US-ChristopherNeural",   # Deep, mature male (Great for horror)
            "Rachel": "en-US-AriaNeural",        # Calm, professional female
            "Bella": "en-US-AnaNeural",          # Bright, friendly female child/teen
            "Antoni": "en-GB-RyanNeural"         # Crisp British male
        }
        
        # Default to Aria if the LLM hallucinates
        edge_voice = voice_ids.get(voice_name, "en-US-AriaNeural")
        
        print(f"Generating audio for voice: {voice_name} (Edge ID: {edge_voice})...")
        
        # 3. Ensure the output directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, "daily_story.mp3")
        
        # 4. Generate and save the audio asynchronously
        communicate = edge_tts.Communicate(story_text, edge_voice)
        await communicate.save(file_path)
                    
        print(f"✅ Audio successfully saved to: {file_path}")
        return {"audio_file_path": file_path}

    except Exception as e:
        error_msg = f"Edge TTS Generation Failed: {str(e)}"
        print(f"❌ {error_msg}")
        return {"error": error_msg}