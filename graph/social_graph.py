from langgraph.graph import StateGraph, END
from agents.facebook_publisher import facebook_publisher_node
from agents.topic_agent import topic_assistant_node
from models.state import AgentState

# Import individual agent nodes
from agents.prompt_engineer import prompt_engineer_node
from agents.storyteller import storyteller_node
from agents.audio_producer import audio_producer_node

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("topic_assistant", topic_assistant_node)
    workflow.add_node("prompt_engineer", prompt_engineer_node)
    workflow.add_node("storyteller", storyteller_node)
    workflow.add_node("audio_producer", audio_producer_node)
    workflow.add_node("facebook_publisher", facebook_publisher_node)

    workflow.set_entry_point("topic_assistant")
    workflow.add_edge("topic_assistant", "prompt_engineer")
    workflow.add_edge("prompt_engineer", "storyteller")
    workflow.add_edge("storyteller", "audio_producer")
    workflow.add_edge("audio_producer", "facebook_publisher")
    workflow.add_edge("facebook_publisher", END)

    return workflow.compile()