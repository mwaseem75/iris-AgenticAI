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