# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv

# load_dotenv()


# def get_llm():
#     llm = ChatOpenAI(
#         model="gpt-4o-mini",
#         temperature=0.7
#     )
#     return llm


from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from app.configuration.model_config import llm_config

# -------------------------
# LLM Setup
# -------------------------

def get_llm(llm_provider):
    if llm_provider == 'GROQ':
        llm_model_config = llm_config.get("llm_models_groq").get("llm_model_1")
    elif llm_provider == 'AWS':
        llm_model_config = llm_config.get("llm_models_aws").get("llm_model_1")
    elif llm_provider == 'AZR':
        llm_model_config = llm_config.get("llm_models_openai").get("llm_model_1")
    
    llm = ChatGroq(
            model=llm_model_config.get("model"),
            temperature=llm_model_config.get("temperature"),
        )
    return llm  