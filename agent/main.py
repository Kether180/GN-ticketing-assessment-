import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent
from agent.tools import ALL_TOOLS
from agent.prompts import SYSTEM_PROMPT

load_dotenv()


def create_agent(): # REACT : Reasoning + acting patterns .
    """Initialize the LLM and create a ReAct agent with tools."""
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    )
    return create_react_agent(llm, ALL_TOOLS)


def run_cli():
    """Simple CLI loop for interacting with the agent."""
    agent = create_agent()
    print("Ticket Assistant ready. Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                break
            if not user_input:
                continue

            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                ("user", user_input),
            ]
            response = agent.invoke({"messages": messages})
            last_message = response["messages"][-1]
            print(f"Agent: {last_message.content}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    run_cli()
