# AI Agent Boilerplate

A minimal, ready-to-use boilerplate for building **AI Agents** using Streamlit, Langchain, and OpenAI.

This boilerplate includes an agent capable of calling tools to perform tasks it wouldn't normally be able to do, such as evaluating mathematical expressions safely or searching the web (using Tavily). It also supports persistent conversation memory throughout the session.

---

## Features

- **Tool Calling Agent**: Uses Langchain's tool calling agent capabilities.
- **Custom Tools**: Includes a safe `calculator` tool using `numexpr` to evaluate math expressions securely.
- **Web Search Tool**: Optionally integrates with Tavily for real-time web search.
- **Interactive Chat**: A Streamlit chat interface for interacting with the agent, complete with conversation history.
- **Configurable Settings**: A central `config.py` file to easily modify models, prompts, and agent parameters.

---

## Prerequisites

- Python 3.8+
- An OpenAI API Key
- (Optional) A Tavily API Key for web search capabilities

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-name>/agent
   ```

2. **Create a Virtual Environment**

   **Windows**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Copy the `.env_example` file to `.env`:
   ```bash
   cp .env_example .env
   ```
   Add your OpenAI API key and optionally your Tavily API key in `.env` or input them directly through the UI. Modify `config.py` to change standard settings.

---

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

1. Enter your API Keys in the sidebar.
2. **Interact with the agent**: Ask it to calculate something complex or search the web for recent events. The agent maintains conversational context throughout the session.
