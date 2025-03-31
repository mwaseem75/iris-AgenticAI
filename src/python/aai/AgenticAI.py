import os
from dotenv import load_dotenv
from typing import cast, List
from pydantic import BaseModel, Field
from agents.mcp.server import MCPServerSse
from agents.model_settings import ModelSettings
import chainlit as cl
from agents import Agent, Runner, WebSearchTool, AsyncOpenAI,OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.tool import function_tool
import IrisUtil

# Load the environment variables from the .env file
load_dotenv()



#Get OPENAI Key, if not fond in .env then get the GEIMINI API KEY
#IF Both defined then take OPENAI Key 
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
   raise ValueError("OPENAI_API_KEY is not set. Please ensure to defined in .env file.")
    
@cl.set_starters  # type: ignore
async def set_starts() -> List[cl.Starter]:
    return [
        cl.Starter(
            label="Greetings",
            message="Hello! What can you help me with today?",           
        )
    ]


@cl.on_chat_start
async def start():
    # With GEMINI API KEY
    # #Reference: https://ai.google.dev/gemini-api/docs/openai
    # external_client = AsyncOpenAI(
    #      api_key=gemini_api_key,
    #      base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    # )
    # model = OpenAIChatCompletionsModel(
    #      model="gemini-2.0-flash",
    #      openai_client=external_client
    # )

    model = "o3-mini" 

    config = RunConfig(
        model=model,
        #model_provider=external_client,
        tracing_disabled=True
    )

    
    @function_tool
    def check_order_status(order_id: str):
        """Check the status of an order with the given order ID."""
        order_statuses = {
            "12345": "Your order 12345 is being prepared and will be delivered in 20 minutes.",
            "67890": "Your order 67890 has been dispatched and will arrive in 10 minutes.",
            "11121": "Your order 11121 is still being processed. Please wait a little longer."
        }
        return order_statuses.get(order_id, "Order ID not found. Please check and try again.")

    order_agent = Agent(
        name="OrderAgent",
        instructions="Help customers with their order status. If they provide an order ID, fetch the status.",
        tools=[check_order_status]
    )

     # #Start Production Agent Tool
    # @function_tool
    # def start_production(prod: str = "last") -> str:
    #         """Help to Start production"""
            
    #         #Get last running production name
    #         if str == "last":
    #             lastProd = iris.gref("^Ens.Configuration")['csp', "LastProduction"]
    #             if lastProd is not None and str(lastProd).strip():
    #                 prod = lastProd
    #             else:
    #                 return "Not able to get Production details"          

    #         sts = iris.cls('Ens.Director').StartProduction(prod)
    #         if sts == 1:
    #             return "Prodcution Started Successfully"
    #         else:
    #             return "Error while Sstarting Production"     
    
    # start_production_agent = Agent(
    #        name="StartProduction",
    #        instructions="Agent to Start the Production. if prod is not specified then take last production",
    #        tools=[start_production]
    # )

    # #Stop Production Agent Tool
    # @function_tool
    # def stop_production() -> str:
    #         """Agent to Stop currently running Production."""
            
    #         sts = iris.cls('Ens.Director').StopProduction(3,1)
    #         if sts == 1:
    #             return "Prodcution Stoped Successfully"
    #         else:
    #             return "Error while Sstarting Production"     

    
    # stop_production_agent = Agent(
    #        name="StopProduction",
    #        instructions="Help to Stop Currently running production",
    #        tools=[stop_production]
    # )


    # #MCP setting. 
    # async with MCPServerSse(
    #      name="time_mcp_server",
    #      params={"url": "https://router.mcp.so/sse/4dsvypm8vlhk9p"},         
    #      cache_tools_list=True,
    # ) as time_mscp_server:

    #     mcp_agent = Agent(
    #             name="mcp_agent",
    #             model=model,
    #             instructions="You are a helpful assistant with access to remote tools via MCP to answer real time questions",
    #             mcp_server=[time_mscp_server],
    #             model_settings=ModelSettings(tool_choice="required"),
    #     )
       
    #Production Agent Tool
    @function_tool
    def check_production_status():
            """Provide Production Status, production details"""
            production_status =  IrisUtil.get_production_status()
            if production_status == '{}':
                return "Production status not found. Please check and try again."
           
            return production_status

    production_agent = Agent(
            name="ProductionAgent",
            instructions="Assist to provide production details, production status.\
            Call the tool and return the production_status",            
            tools=[check_production_status]
    )

    #Production Agent Tool
    @function_tool
    def dashboard_info():
            """Provide Management Portal Dashboard information"""
            content = IrisUtil.get_dashboard_stats()            
            return content

    dashboard_agent = Agent(
            name="DashboardAgent",
            instructions="Assist to provide managment portal dashboard details.\
            ApplicationErrors,CSPSessions,CacheEfficiency,DatabaseSpace,DiskReads,DiskWrites,\
		    ECPAppServer,ECPAppSrvRate,ECPDataServer,ECPDataSrvRate,GloRefs,GloRefsPerSec,GloSets,\
		    JournalEntries,JournalSpace,JournalStatus,last_backup,LicenseCurrent,LicenseCurrentPct,\
		    LicenseHigh,LicenseHighPct,LicenseLimit,LicenseType,LockTable,.LogicalReads,Processes,\
		    RouRefs,SeriousAlerts,ShadowServer,ShadowSource,SystemUpTime,WriteDaemon"  ,      
            tools=[dashboard_info]
    )

        #Production Agent Tool
    @function_tool
    def process_info():
            """Provide Management Portal Dashboard information"""
            content = IrisUtil.get_processes()            
            return content

    processes_agent = Agent(
            name="ProcessesAgent",
            instructions="Assist to provide IRIS running processes details.\
            Process ID, NameSpace, Routine, LinesExecuted, GlobalReferences, \
            state, PidExternal, UserName, ClientIPAddress"  ,      
            tools=[process_info]
    )


    web_search_agent = Agent(
        name="WebSearchAgent",
        instructions="Perform web searches to find relevant information.",
        tools=[WebSearchTool()]
    )

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

  
    
    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)      
    cl.user_session.set("agent", triage_agent)
    
     
    WelcomeMsg = "Welcome to the IRIS AI Assistant! I can assist you to provide:\n" \
                "- IRIS Management Portal dashboard information\n" \
                "- Information about currently running processes\n" \
                "- Production status.\n" \
                "- Websearch functionality." 
            
    await cl.Message(content=WelcomeMsg).send()
   
    

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []
    
    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})
    

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        #result = Runner.run_sync(agent, history, run_config=config)
        result = Runner.run_sync(agent, history, run_config=config)

        response_content = result.final_output
        
        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()

        # Append the assistant's response to the history.
        history.append({"role": "developer", "content": response_content})
        # NOTE: Here we are appending the response to the history as a developer message.
        # This is a BUG in the agents library.
        # The expected behavior is to append the response to the history as an assistant message.
    
        # Update the session with the new history.
        cl.user_session.set("chat_history", history)
        
        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")