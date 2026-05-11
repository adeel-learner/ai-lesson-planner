# AI Lesson Planner

An AI-powered educational platform that generates comprehensive lesson plans integrating science, critical thinking, ethical reflection, and Islamic values. It creates structured learning content for specific topics and grade levels while maintaining scientific accuracy and promoting contemplative learning.

## Features

- **Multi-Provider LLM Support**: Flexible integration with GROQ (Llama 3.1), AWS (Claude 3.7/3.5 Sonnet), and Azure (GPT-4o)
- **Islamic-Science Integration**: Connects scientific concepts with Islamic themes of contemplation, gratitude, and ethical responsibility
- **Streaming Responses**: Real-time output for lesson generation
- **Critical Thinking Focus**: Emphasizes evidence-based learning and avoids conflating science with religion

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run sample test:
```bash
python -m app.test.simple_test
```
or 
maybe once you are confident then you can build a FASTAPI server later!

Run the FastAPI server:
```bash
uvicorn main:app --reload
```

Send a POST request to `http://localhost:8000/generate-lesson` with lesson parameters (topic, grade level, curriculum, dimensions) to generate structured lesson content.

## Project Structure

- `main.py`: FastAPI server with lesson generation endpoint
- `app/ai_curriculum_planner.py`: Core lesson planning logic
- `app/configuration/`: LLM service configuration and model settings
- `app/prompts/`: Educational prompts and guidelines
- `utils/`: Helper utilities like token counting

## Requirements

- Python 3.8+
- FastAPI
- LangChain
- Supported LLM providers (GROQ, AWS Bedrock, Azure OpenAI)