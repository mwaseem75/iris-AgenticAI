#!/bin/bash

set -m

chainlit run /irisdev/app/src/python/aai/AgenticAI.py -h --port 8002 --host 0.0.0.0

fg %1