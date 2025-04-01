# Iris-AgenticAI
The rise of agentic AI marks a transformative leap in how artificial intelligence interacts with the world—moving beyond static responses to dynamic, goal-driven problem-solving. Powered by [OpenAI’s Agentic SDK](https://openai.github.io/openai-agents-python/)) , this application showcases the next generation of autonomous AI systems capable of reasoning, collaborating, and executing complex tasks with human-like adaptability.

[![one](https://img.shields.io/badge/Platform-InterSystems%20IRIS-blue)](https://www.intersystems.com/data-platform/) [![one](https://img.shields.io/badge/LLM-GPT-Purple)](https://openai.com/index/gpt-3-apps/) [![one](https://img.shields.io/badge/WebFramework-Chainlit-teal)](https://https://docs.chainlit.io/get-started/overview/) [![one](https://img.shields.io/badge/SDK-OpenAI%20Agentic%20SDK-Orange)](https://openai.github.io/openai-agents-python/) [![one](https://img.shields.io/badge/ORM-SQLAlchemy-teal)](https://www.sqlalchemy.org/)  [![one](https://img.shields.io/badge/OpenAI-ChatGPT-yellow)](https://openai.com/) [![OEX](https://img.shields.io/badge/Available%20on-Intersystems%20Open%20Exchange-00b2a9.svg)](https://github.com/mwaseem75/iris-RAG-Gen/blob/main/LICENSE) [![license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/mwaseem75/iris-RAG-Gen/blob/main/LICENSE)


# Application Structure
![image](https://github.com/user-attachments/assets/6525c638-4708-4eb8-9b83-6411d8592d6a)



# Application Interface
![image](https://github.com/user-attachments/assets/31b89b5c-5c81-4b7f-aa90-9997ae9092b8)

# Features
* IRIS Management Portal Dashboard Agent
* IRIS Running Process Monitoring Agent
* IRIS Production Information Agent
* WebSearch Agent
* Local Functional Agent
* Model context protocol (MCP) functionality

# Installation
1. Clone/git pull the repo into any local directory

```
git clone https://github.com/mwaseem75/iris-AgenticAI.git
```

## Requirement
Application requires OpenAI API Key, sign up for OpenAI API on [this page](https://platform.openai.com/account/api-keys). Once you have signed up and logged in, click on Personal, and select View API keys in drop-down menu. Create and copy the API Key
![image](https://github.com/mwaseem75/irisChatGPT/assets/18219467/7e7c7880-b9ac-4a60-9ec9-289dd2375a73)

Create a .env file in the root directory and add your OpenAI API key:
![image](https://github.com/user-attachments/assets/c610f65a-6a33-4fcb-a12f-7b4895728da3)

2. Open a Docker terminal in this directory and run:

```
docker-compose build
```

3. Run the IRIS container:

```
docker-compose up -d 
```


## Run Chainlit Web Application
To run the Application, Navigate to [**http://localhost:8002**](http://localhost:8002) 
![image](https://github.com/user-attachments/assets/71a7d091-b7d0-4650-b0a9-1439363bb47f)

## About OpenAI Agents SDK
The OpenAI Agents SDK enables you to build agentic AI apps in a lightweight, easy-to-use package with very few abstractions. It's a production-ready upgrade of our previous experimentation for agents, Swarm.

####  Main features of the SDK:
Agent loop: Built-in agent loop that handles calling tools, sending results to the LLM, and looping until the LLM is done.
Python-first: Use built-in language features to orchestrate and chain agents, rather than needing to learn new abstractions.
Handoffs: A powerful feature to coordinate and delegate between multiple agents.
Guardrails: Run input validations and checks in parallel to your agents, breaking early if the checks fail.
Function tools: Turn any Python function into a tool, with automatic schema generation and Pydantic-powered validation.
Tracing: Built-in tracing that lets you visualize, debug and monitor your workflows, as well as use the OpenAI suite of evaluation, fine-tuning and distillation tools.

#### Agent
Agents are the core building block in your apps. An agent is a large language model (LLM), configured with instructions and tools.
Basic configuration
The most common properties of an agent you'll configure are:

instructions: also known as a developer message or system prompt.
model: which LLM to use, and optional model_settings to configure model tuning parameters like temperature, top_p, etc.
tools: Tools that the agent can use to achieve its tasks.

```
from agents import Agent, ModelSettings, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model="o3-mini",
    tools=[get_weather],
)
```
our application contains 7 agents
![image](https://github.com/user-attachments/assets/7dae8064-0ba2-42be-bb09-561e9df755e7)

-
-
-
-
-
-
-

#### handoffs
Handoffs allow an agent to delegate tasks to another agent. This is particularly useful in scenarios where different agents specialize in distinct areas. For example, a customer support app might have agents that each specifically handle tasks like order status, refunds, FAQs, etc.

Triage agent is our main agent which delegate tasks to another agent based on user input
```
triage_agent = Agent(
        name="Triage agent",
        instructions=(
            "Handoff to appropriate agent based on user query."
            "If they ask about production, handoff to the production agent."
            "If they ask about dashboard, handoff to the dashboard agent."
            "If they ask about process, handoff to the processes agent." 
            "use the WebSearchAgent tool to find information related to the user's query."           
            "If they ask about order, handoff to the order_agent."            
        ),
        handoffs=[production_agent,dashboard_agent,processes_agent,web_search_agent,order_agent]
    )

```

Ask about IRIS licence information
![image](https://github.com/user-attachments/assets/8db9904b-ffb3-458e-b952-6c386e8d4c69)

![image](https://github.com/user-attachments/assets/a1f95ac7-7274-4ba0-a28f-bfe69b5abe65)

Websearch Tool
![image](https://github.com/user-attachments/assets/241f5270-6f7e-4556-89b2-1f51e2553353)

### Tracing
The Agents SDK includes built-in tracing, collecting a comprehensive record of events during an agent run: LLM generations, tool calls, handoffs, guardrails, and even custom events that occur. Using the Traces dashboard, you can debug, visualize, and monitor your workflows during development and in production.
https://platform.openai.com/logs
![image](https://github.com/user-attachments/assets/f5476f50-c748-4bfa-97e4-60c65a1d904e)


## MCP Server application
To run the Application, Navigate to [**http://localhost:8002**](http://localhost:8001) 
![image](https://github.com/user-attachments/assets/3a911108-bc52-473b-9b16-bfe8581f3c3f)


in case of below error, start application manually by using below command in the docker 
![image](https://github.com/user-attachments/assets/9f833b26-d0bf-4f83-abb3-7b629a7e0e65)

```
chainlit run /irisdev/app/src/python/aai/MCPapp.py -h --port 8001 --host 0.0.0.0
```
![image](https://github.com/user-attachments/assets/f2003c1f-5fbc-40ed-8ef7-160497a3aea2)

Below is the command to start MCP server in case if server is not started
```
uv run python /irisdev/app/src/python/aai/runMCPServer.py
```
MCP Server is running at https://localhost:8000/sse
![image](https://github.com/user-attachments/assets/359c623b-0aab-45e1-a78f-610d93b4131d)


MCP server is equiped with the below tools, based on user input it calls the related tool
![image](https://github.com/user-attachments/assets/7be957e3-0661-45b4-b351-562205f6c1b3)
Based on the user input, Server calls related tool.
4 Tools are defined with MCP server, 1,2,3,4.
Based on the user input MCP will call related tool.
![image](https://github.com/user-attachments/assets/03d96d43-d42c-4ff2-a5b2-da3fc0b8f721)

Thanks



