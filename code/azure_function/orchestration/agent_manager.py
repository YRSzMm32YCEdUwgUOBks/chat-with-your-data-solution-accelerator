# orchestration/agent_manager.py
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os


def create_assistant_agent():
    # Model client – use the env vars
    # Set up the model client
    model_client = AzureOpenAIChatCompletionClient(
        model=os.getenv("AZURE_OPENAI_MODEL"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0.2,
        max_tokens=3500,
    )
    return AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="You are a helpful, wry assistant.",
    )
