llm_config=	{ 
    "llm_models_openai": {
        "llm_model_1": {
            "model": "gpt-4o",
            "verbose": True,
            "streaming": True,
            "temperature": 0.0,
            "max_tokens": 16000,
            "deployment_name": "gpt-4o",
            "llm_provider": "AZR",
        },
    },
    "llm_models_aws": {
        "llm_model_1": {
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "verbose": True,
            "streaming": True,
            "temperature": 0,
            "max_tokens": 128000,
            "deployment_name": "",
            "llm_provider": "AWS",
        },
        "llm_model_2": {
            "model": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            "verbose": True,
            "streaming": True,
            "temperature": 0,
            "max_tokens": 8000,
            "deployment_name": "",
            "llm_provider": "AWS",
        }
    },
    "llm_models_groq": {
        "llm_model_1": {
            "model": "llama-3.1-8b-instant",
            "verbose": True,
            "streaming": True,
            "temperature": 0,
            "max_tokens": 16000,
            "deployment_name": "",
            "llm_provider": "GROQ",
        },
    }
}