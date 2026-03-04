import asyncio
from dotenv import load_dotenv
from graph.social_graph import build_graph

# Load environment variables (API Keys)
load_dotenv()

async def main():
    print("🚀 Waking up Autonomous Social Media Agent...\n")
    
    # Initialize the compiled LangGraph workflow
    app = build_graph()
    
    # We pass an empty state. The Topic Assistant will populate the 'topic'.
    initial_state = {}
    
    # Execute the asynchronous graph
    final_state = await app.ainvoke(initial_state)
    
    print("\n--- Pipeline Execution Complete ---")
    if final_state.get("error"):
        print(f"❌ Pipeline failed: {final_state['error']}")
    else:
        print(f"✅ Success! Audio saved to: {final_state.get('audio_file_path')}")

if __name__ == "__main__":
    asyncio.run(main())