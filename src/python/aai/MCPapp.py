import os
from dotenv import load_dotenv
from typing import cast, List
from pydantic import BaseModel, Field
from agents.mcp.server import MCPServerSse
from agents.model_settings import ModelSettings
import chainlit as cl
from agents.run import RunConfig
from agents import Agent, Runner, gen_trace_id, trace


# Load the environment variables from the .env file
load_dotenv()

#Get OPENAI Key, if not fond in .env then get the GEIMINI API KEY
#IF Both defined then take OPENAI Key 
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
   raise ValueError("OPENAI_API_KEY is not set. Please ensure to defined in .env file.")
    

@cl.on_chat_start
async def start():
      
    WelcomeMsg = "Welcome to the IRIS MCP Assistant! I can assist you to provide:\n" \
                "- Weather Information. e.g(What's the weather in Tokyo?)\n" \
                "- Find secret word. e.g(What is the secret word?)\n" \
                "- Perform Addition. e.g (Add these numbers: 9 and 21)."            
    
    await cl.Message(content=WelcomeMsg).send()
   
    

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()
    async with MCPServerSse(
        name="IRIS-AgenticAI MCP Server",
        params={
            "url": "http://localhost:8000/sse",
        },
    ) as server:          
        agent = Agent(
        name="Assistant",
        instructions="Use the tools to answer the questions.",
        mcp_servers=[server],
        model_settings=ModelSettings(tool_choice="required"),
        )
        try:
            config = RunConfig(tracing_disabled=True)
            result = await Runner.run(starting_agent=agent,input=message.content,run_config=config)        
                 
            response_content = result.final_output
            msg.content = response_content
            await msg.update()
           
              

        except Exception as e:
            content = f"Error: {str(e)}"
            await cl.Message(content=content).send()    