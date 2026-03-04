import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.state import AgentState
from services.topic_service import fetch_daily_trends

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.7,
    max_retries=2
)

def topic_assistant_node(state: AgentState) -> dict:
    print("--- 🤖 TOPIC ASSISTANT WORKING ---")
    trends = fetch_daily_trends()
    
    # Provide the LLM with your available ElevenLabs voices
    system_prompt = """
    You are the Lead Content Strategist. Review the trending topics and formulate a short story topic.
    
    You must also select the best voice actor for the genre from this list:
    - "Adam" (Deep, authoritative - great for horror/dark sci-fi)
    - "Rachel" (Calm, professional - great for drama)
    - "Bella" (Soft, friendly - great for wholesome/light stories)
    - "Antoni" (Well-rounded - great for mystery)
    
    Output a raw JSON object exactly like this, with no markdown formatting:
    {{
        "topic": "The chosen story topic",
        "voice_name": "Adam"
    }}
    """
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Today's Trends: {trends}")
    ])
    
    response = (prompt_template | llm).invoke({"trends": trends})
    
    # Parse the JSON response
    try:
        result = json.loads(response.content.strip('` \n'))
        print(f"Assistant Selected Topic: {result['topic']}")
        print(f"Assistant Selected Voice: {result['voice_name']}")
        return {"topic": result["topic"], "voice_name": result["voice_name"]}
    except Exception as e:
        # Fallback in case the LLM messes up the JSON formatting
        return {"topic": "A dark mystery horror story.", "voice_name": "Adam"}