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

Ask about IRIS licence information
![image](https://github.com/user-attachments/assets/8db9904b-ffb3-458e-b952-6c386e8d4c69)

![image](https://github.com/user-attachments/assets/a1f95ac7-7274-4ba0-a28f-bfe69b5abe65)

Websearch Tool
![image](https://github.com/user-attachments/assets/241f5270-6f7e-4556-89b2-1f51e2553353)



## MCP Server application
To run the Application, Navigate to [**http://localhost:8002**](http://localhost:8001) 
![image](https://github.com/user-attachments/assets/03d96d43-d42c-4ff2-a5b2-da3fc0b8f721)





