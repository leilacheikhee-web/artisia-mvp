<!-- # ARTISIA MVP - AI Artisan Listing Generator

ARTISIA is an AI-powered system designed to help artisans transform their unique stories and products into globally competitive marketplace listings.

## Architecture

The system follows a multi-agent orchestrated pipeline:

1. **Artisan Interview**: Structured collection of artisan, product, story, and market data.
2. **ProductMemory**: A shared state object that persists data across the pipeline.
3. **Multi-Agent Pipeline**:
    - **Brand Agent**: Crafts the brand narrative.
    - **Market Agent**: Determines pricing and positioning.
    - **Listing Agent**: Generates marketplace-ready descriptions.
    - **Translator Agent**: Provides multilingual support (English & French).
    - **Scoring Agent**: Evaluates global readiness.

## File Structure

```
artisia/
├── app.py                  # Streamlit UI
├── requirements.txt         # Dependencies
├── .env                    # Environment variables (Ollama config)
├── agents/                 # Agent logic
│   ├── brand_agent.py
│   ├── market_agent.py
│   ├── listing_agent.py
│   ├── translator_agent.py
│   ├── scoring_agent.py
│   └── pipeline.py
├── utils/                  # Shared utilities
│   ├── memory.py           # Shared data structure
│   ├── interview.py        # Interview questions
│   ├── prompts.py          # LLM Prompts
│   └── ollama_client.py    # Ollama API client
├── data/
│   └── outputs/            # JSON records of generated listings
└── logs/
    └── runs.log            # Execution logs
```

## Setup Instructions

### 1. Prerequisites
- Ensure you have **Python 3.10+** installed.
- Ensure **Ollama** is installed and running on your system.
- Download the required models:
  ```bash
  ollama pull glm-4.6:cloud
  ```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Running the Application
```bash
streamlit run app.py
```

## Usage
1. Open the Streamlit URL provided in the terminal.
2. Fill out the four sections of the interview.
3. Click "Generate Listing".
4. View the results across the tabs.
5. The full memory state is visible in the sidebar. -->