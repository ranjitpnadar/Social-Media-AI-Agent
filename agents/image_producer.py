import os
import edge_tts
import json
from models.state import AgentState
from langchain_core.prompts import ChatPromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI
from services.llm_client import chat_completion,image_generation
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash", 
#     temperature=0.7,
#     max_retries=2
# )
def generate_image(imageInstruction: str) -> dict:
    system_prompt = """Given Image Instruction convert into image {imageInstruction}"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Image: {imageInstruction}"},
    ]
    raw = image_generation(system_prompt)
    print("image generation response", raw)
    return raw[0] if raw else None
async def image_producer_node(state: AgentState) -> dict:
    story_text = state.get("story_text")
    system_prompt = """You are a cinematic storyteller and AI video director.
Your task is to convert the given story into structured scenes in VALID JSON format.

Output Requirements:
- Return ONLY valid JSON (no explanation, no markdown)
- The JSON must contain an array called 'scenes'
- Generate 4 to 6 scenes
- Each scene must be visually descriptive and suitable for image and video generation

Each scene object must follow this structure:
{
  "scene_number": 1,
  "title": "Short cinematic title",
  "image_prompt": "Optimized prompt for image generation",
  "video_prompt": "Optimized prompt for video generation with motion"
}

Guidelines:
- Maintain continuity between scenes
- Keep descriptions visual (show, do not tell)
- Avoid abstract language unless visualized
- Ensure prompts are detailed and tool-friendly (Midjourney, SDXL, Runway, Pika)
- Keep character consistency across scenes
"""
    
    try:
        safe_system_prompt = system_prompt
        # prompt_template = ChatPromptTemplate.from_messages([
        #     ("system", safe_system_prompt),
        #     ("human", "Story: {story_text}")
        # ])
        messages = [
            {"role": "system", "content": safe_system_prompt},
            {"role": "user", "content": f"Story: {story_text}"},
        ]
        # chain = prompt_template | llm
        # response = chain.invoke({"story_text": story_text})   
        raw = chat_completion(messages, temperature=0.7)
        # response = raw #json.loads(raw.strip('` \n'))/
        clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

        scenes = json.loads(clean)["scenes"]
        # with open('scenes_res.json', 'w') as f:
        #     json.dump(response, f)
        # print("--- 🧠 IMAGE Renerator Response ---", response.content)
        # scenes = json.loads(response)["scenes"]
        # print("Parsed Scenes for Image Generation:", scenes)
        res = []
        for scene in scenes:
            print("scene==>",scene)
            if "image_prompt" in scene:
                temp = generate_image(scene["image_prompt"])
                print("image generation response", temp)
                res.append({
                    "scene_number": scene["scene_number"],
                    "title": scene["title"],
                    "image_prompt": scene["image_prompt"],
                    "video_prompt": scene["video_prompt"],
                    "image_url": temp
                })
            else:
                res.append({
                    "scene_number": scene["scene_number"],
                    "title": scene["title"],
                    "image_prompt": None,
                    "video_prompt": scene["video_prompt"],
                    "generated_image_details": None
                })
        # print(f"System Prompt for Image Generation:\n{system_prompt}\n")
        print(f"✅ Image Agent successfully generated the image prompts for all scenes!", res)
        print(f"✅ Image Agent successfully generated the creative prompt for image generation!")
        # return {"audio_file_path": audio_file_path}
        return {"image_details": res}
    except Exception as e:
        error_msg = f"Image Generation Failed: {str(e)}"
        print(f"❌ {error_msg}")
        return {"error": error_msg}