#!/bin/bash

set -m

uv run python /irisdev/app/src/python/aai/runMCPServer.py
chainlit run /irisdev/app/src/python/aai/AgenticAI.py -h --port 8002 --host 0.0.0.0
chainlit run /irisdev/app/src/python/aai/MCPapp.py -h --port 8001 --host 0.0.0.0

fg %1