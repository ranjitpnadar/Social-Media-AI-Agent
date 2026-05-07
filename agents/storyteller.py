import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.state import AgentState
from services.llm_client import chat_completion  
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash", 
#     temperature=0.7,
#     max_retries=2
# )

def storyteller_node(state: AgentState) -> dict:
    try:
        print("--- ✍️ STORYTELLER WORKING ---", state)
        system_prompt = "You are a Master Storyteller. Write a captivating short story (max 100 words) for spoken-word narration. Output ONLY the story text."
        
        # prompt_template = ChatPromptTemplate.from_messages([
        #     ("system", system_prompt),
        #     ("human", "Writing Prompt: {creative_prompt}")
        # ])
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Writing Prompt: {state['creative_prompt']}"},
        ]
        
        
        # chain = prompt_template | llm
        # response = chain.invoke({"creative_prompt": state["creative_prompt"]})
        raw = chat_completion(messages, temperature=0.7)
        # response = json.loads(raw.strip('` \n'))
        response = raw
        print("--- ✍️ STORYTELLER Result ---", response)
        return {"story_text": response}
    except Exception as e:
        print(f"❌ Error in Storyteller Node: {str(e)}")