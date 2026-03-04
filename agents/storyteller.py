from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.state import AgentState
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.7,
    max_retries=2
)

def storyteller_node(state: AgentState) -> dict:
    print("--- ✍️ STORYTELLER WORKING ---")
    system_prompt = "You are a Master Storyteller. Write a captivating short story (max 100 words) for spoken-word narration. Output ONLY the story text."
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Writing Prompt: {creative_prompt}")
    ])
    
    chain = prompt_template | llm
    response = chain.invoke({"creative_prompt": state["creative_prompt"]})
    print("--- ✍️ STORYTELLER Result ---", response.content)
    return {"story_text": response.content}