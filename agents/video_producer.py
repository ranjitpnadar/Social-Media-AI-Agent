import os
import edge_tts
import json
from models.state import AgentState
from langchain_core.prompts import ChatPromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI
from services.llm_client import chat_completion,video_generation
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

def generate_video(videoInstruction: str) -> dict:
    system_prompt = """Given Video Instruction convert into video {videoInstruction}"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Video: {videoInstruction}"},
    ]
    raw = video_generation(system_prompt)
    print("video generation response", raw)
    return raw[0] if raw else None
async def video_producer_node(state: AgentState) -> dict:
    try:
        print("--- 🎬 VIDEO PRODUCER WORKING ---", state["image_details"])
        video_output = []
        for scene_detail in state["image_details"]:
            video_instruction = scene_detail['video_prompt']

            temp = generate_video(video_instruction)
            # video_output.append({
            #         "scene_number": scene["scene_number"]
            # })
            print(f"✅ Video Agent successfully generated video for Scene {scene_detail['scene_number']}!", temp)
        return {"video_output": video_output}
    except Exception as e:
        error_msg = f"Video Generation Failed: {str(e)}"
        print(f"❌ {error_msg}")
        return {"error": error_msg}