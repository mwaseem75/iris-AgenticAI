# Iris-AgenticAI 🤖⚡
The rise of agentic AI marks a transformative leap in how artificial intelligence interacts with the world—moving beyond static responses to dynamic, goal-driven problem-solving. Powered by [OpenAI’s Agentic SDK](https://openai.github.io/openai-agents-python/), The OpenAI Agents SDK enables you to build agentic AI apps in a lightweight, easy-to-use package with very few abstractions. It's a production-ready upgrade of our previous experimentation for agents, Swarm. 

This application showcases the next generation of autonomous AI systems capable of reasoning, collaborating, and executing complex tasks with human-like adaptability. 

[![one](https://img.shields.io/badge/Platform-InterSystems%20IRIS-blue)](https://www.intersystems.com/data-platform/) [![one](https://img.shields.io/badge/LLM-GPT-Purple)](https://openai.com/index/gpt-3-apps/) [![one](https://img.shields.io/badge/WebFramework-Chainlit-teal)](https://https://docs.chainlit.io/get-started/overview/) [![one](https://img.shields.io/badge/SDK-OpenAI%20Agentic%20SDK-Orange)](https://openai.github.io/openai-agents-python/) [![one](https://img.shields.io/badge/ORM-SQLAlchemy-teal)](https://www.sqlalchemy.org/)  [![one](https://img.shields.io/badge/OpenAI-ChatGPT-yellow)](https://openai.com/) [![OEX](https://img.shields.io/badge/Available%20on-Intersystems%20Open%20Exchange-00b2a9.svg)](https://github.com/mwaseem75/iris-RAG-Gen/blob/main/LICENSE) [![license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/mwaseem75/iris-RAG-Gen/blob/main/LICENSE)


# Application Structure
![image](https://github.com/user-attachments/assets/2dd912f7-c467-4da1-85ac-d6d330207674)


# Application Interface
![image](https://github.com/user-attachments/assets/fb6efbc1-46a1-421d-9822-7006fd80462a)


# Features
* **Agent Loop** 🔄
A built-in loop that autonomously manages tool execution, sends results back to the LLM, and iterates until task completion.

* **Python-First** 🐍
Leverage native Python syntax (decorators, generators, etc.) to orchestrate and chain agents without external DSLs.

* **Handoffs** 🤝
Seamlessly coordinate multi-agent workflows by delegating tasks between specialized agents.

* **Function Tools** ⚒️
Decorate any Python function with @tool to instantly integrate it into the agent’s toolkit.

* **Vector Search (RAG)** 🧠
Native integration of vector store (IRIS) for RAG retrieval.

* **Tracing** 🔍
Built-in tracing to visualize, debug, and monitor agent workflows in real time (think LangSmith alternatives).

* **MCP Servers** 🌐
Support for Model Context Protocol (MCP) via stdio and HTTP, enabling cross-process agent communication.

* **Chainlit UI** 🖥️
Integrated Chainlit framework for building interactive chat interfaces with minimal code.

* **Stateful Memory** 🧠
Preserve chat history, context, and agent state across sessions for continuity and long-running tasks.


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
![image](https://github.com/user-attachments/assets/bb93669c-2005-4378-9323-1c54236e4549)


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
The application contains 7 agents:
* **Triage Agent** 🤖 : Main agent receives user input and delegates to other agent by using handoffs
* **Vector Search Agent** 🤖: Provide IRIS 2025.1 Release notes details (RAG Functionality)
* **IRIS Dashboard Agent** 🤖: Assist in providing below management portal dashboard details:
( ApplicationErrors,CSPSessions,CacheEfficiency,DatabaseSpace,DiskReads,DiskWrites,    ECPAppServer,ECPAppSrvRate,ECPDataServer,ECPDataSrvRate,GloRefs,GloRefsPerSec,GloSets,
JournalEntries,JournalSpace,JournalStatus,last_backup,LicenseCurrent,LicenseCurrentPct,		    LicenseHigh,LicenseHighPct,LicenseLimit,LicenseType,LockTable,.LogicalReads,Processes,		    RouRefs,SeriousAlerts,ShadowServer,ShadowSource,SystemUpTime,WriteDaemon)  
* **IRIS Running Process Agent** 🤖: Assist to provide IRIS running processes details.(Process ID, NameSpace, Routine, state, PidExternal)
* **IRIS Production Agent** 🤖: Assist to provide Production information, start and stop the production.
* **WebSearch Agent** 🤖: Perform web searches to find relevant information.
* **Order Agent** 🤖: Check the status of an order with the given order ID. 

#### Handoffs
Handoffs allow an agent to delegate tasks to another agent. This is particularly useful in scenarios where different agents specialize in distinct areas. For example, a customer support app might have agents that each specifically handle tasks like order status, refunds, FAQs, etc.

Triage agent is our main agent which delegate tasks to another agent based on user input
```
    #TRIAGE AGENT, Main agent receives user input and delegates to other agent by using handoffs
    triage_agent = Agent(
        name="Triage agent",
        instructions=(
            "Handoff to appropriate agent based on user query."
            "if they ask about Release Notes, handoff to the vector_search_agent."
            "If they ask about production, handoff to the production agent."
            "If they ask about dashboard, handoff to the dashboard agent."
            "If they ask about process, handoff to the processes agent."     
            "use the WebSearchAgent tool to find information related to the user's query and do not use this agent is query is about Release Notes."               
            "If they ask about order, handoff to the order_agent."            
        ),
        handoffs=[vector_search_agent,production_agent,dashboard_agent,processes_agent,order_agent,web_search_agent]
    )
```
## Application Workflow Process
#### Vector Search Agent
Vector Search Agent automatically ingests [New in InterSystems IRIS 2025.1](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=GCRN_new20251) text information into IRIS Vector Store only once if the data doesn't already exist.

Use the query below to retrieve the data
```
select 
```
![image](https://github.com/user-attachments/assets/81812797-b293-456c-911a-746a545be33c)

The Triage Agent receives user input, routing the question to the Vector Search Agent.
![image](https://github.com/user-attachments/assets/66a5fac4-7a1d-4928-b615-29494b359c74)



The Triage Agent receives user input, routing the question to the IRIS Dashboard Agent.
![image](https://github.com/user-attachments/assets/868fe832-fcd9-4d2c-907e-896787f52c39)

The Triage Agent receives user input, routing the question to the IRIS Processes Agent.
![image](https://github.com/user-attachments/assets/cb941c66-e35b-4dd9-9d59-950d648a5eec)

Start and Stop the Production.
![image](https://github.com/user-attachments/assets/b44f3f79-e29c-49ea-9686-9a22289199ba)

Get Production Details.
![image](https://github.com/user-attachments/assets/b356a29a-fcf9-4dfc-9d4a-8ce41fcd8dc6)

The Triage Agent receives user input, routing the question to the Local Order Agent.
![image](https://github.com/user-attachments/assets/83dff43f-8214-4e69-8c59-fa2abfa42d42)

Here, the triage Agent receives two questions, routing both to the WebSearcg Agent.
![image](https://github.com/user-attachments/assets/241f5270-6f7e-4556-89b2-1f51e2553353)

### Tracing
The Agents SDK includes built-in tracing, collecting a comprehensive record of events during an agent run: LLM generations, tool calls, handoffs, guardrails, and even custom events that occur. Using the Traces dashboard, you can debug, visualize, and monitor your workflows during development and in production.
https://platform.openai.com/logs
![image](https://github.com/user-attachments/assets/f5476f50-c748-4bfa-97e4-60c65a1d904e)


## MCP Server
MCP Server is running at https://localhost:8000/sse
![image](https://github.com/user-attachments/assets/df7ff363-3b67-4991-8ba3-0bed644f5040)

**NOTE:** The MCP Server is configured to start automatically. If the server fails to launch, manually start it using the following command:
```
uv run python /irisdev/app/src/python/aai/runMCPServer.py
```

The MCP Server is equipped with the following tools:
* IRIS Info tool
* Check Weather tool
* Find secret word tool (Local function)
* Addition Tool (Local function)
```
import random,iris
import requests
from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("Echo Server")

#Local function
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"[debug-server] add({a}, {b})")
    return a + b

#Local Function
@mcp.tool()
def get_secret_word() -> str:
    print("[debug-server] get_secret_word()")
    return random.choice(["apple", "banana", "cherry"])

#Get IRIS Version details
@mcp.tool()
def get_iris_version() -> str:
    print("[debug-server] get_iris_version()")
    return iris.system.Version.GetVersion()

#Get Current weather
@mcp.tool()
def get_current_weather(city: str) -> str:
    print(f"[debug-server] get_current_weather({city})")

    endpoint = "https://wttr.in"
    response = requests.get(f"{endpoint}/{city}")
    return response.text

if __name__ == "__main__":
    mcp.run(transport="sse")
```

## MCP application
The application communicates with the MCP Server, which runs locally at localhost.
MCP application is running at http://localhost:8001
![image](https://github.com/user-attachments/assets/1fbacf2d-d60b-4683-aaab-817d0ce73695)

#### Starting the MCP application
**NOTE:** In case of "Page isn't working error", manually start the application by using the following Docker command:
```
chainlit run /irisdev/app/src/python/aai/MCPapp.py -h --port 8001 --host 0.0.0.0
```
![image](https://github.com/user-attachments/assets/f2003c1f-5fbc-40ed-8ef7-160497a3aea2)


The MCP Server dynamically delegates tasks to the appropriate tool based on user input.
![image](https://github.com/user-attachments/assets/41fd5443-6da3-495d-8264-0af4390c3ece)


Thanks



