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

def prompt_engineer_node(state: AgentState) -> dict:
    try:
        print("State in Prompt Engineer Node:", state)
        print("--- 🧠 PROMPT ENGINEER WORKING ---")
        system_prompt = "You are a Creative Director. Generate a highly detailed, 2-paragraph writing prompt defining characters, setting, tone, and hook for the given topic."
        
        # prompt_template = ChatPromptTemplate.from_messages([
        #     ("system", system_prompt),
        #     ("human", "Topic: {topic}")
        # ])
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Topic: {state['topic']}"},
        ]
        
        # chain = prompt_template | llm
        # response = chain.invoke({"topic": state["topic"]})
        raw = chat_completion(messages, temperature=0.7)
        result = raw #json.loads(raw.strip('` \n'))

        return {"creative_prompt": result}
    except Exception as e:
        print(f"❌ Error in Prompt Engineer Node: {str(e)}")