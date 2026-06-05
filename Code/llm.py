from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel
import os
from dotenv import load_dotenv
load_dotenv()

def get_llm(model_name:str, temperature:float = 0.0) -> BaseChatModel:

    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model=model_name,
        temperature=temperature
    )
