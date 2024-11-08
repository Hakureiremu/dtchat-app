from .strategy import *  
import asyncio
from openai import OpenAI
from ..tools import * 
import logging
import json
from inspect import isclass, getmembers

GPT_MODEL = 'gpt-4o-2024-08-06'
logger = logging.getLogger(__name__)
client = OpenAI() 

# initialize strategies
strategies = {}

def initialize_strategies():
    for name, cls in getmembers(__import__('chat.strategy.strategy', fromlist=['']), isclass):
        if issubclass(cls, QueryStrategy) and cls is not QueryStrategy:
            instance = cls()
            strategies[instance.get_strategy()] = instance
            
initialize_strategies()

def function_call(question, response):
    try:
        tool_calls = response.choices[0].message.tool_calls
        connector_name = tool_calls[0].function.name
        print(strategies)
        strategy = strategies.get(connector_name)
        messages = messages = [{"role": "user", "content": question}]
        tools = strategy.get_tools()

        if not strategy:
            return {"error": f"Unknown function name: {connector_name}"}
        
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            tools=tools,
            tool_choice = "auto"
        )

        method_name = response.choices[0].message.tool_calls[0].function.name
        arguments = json.loads(response.choices[0].message.tool_calls[0].function.arguments)

        # execute specific method  
        data = asyncio.run(strategy.execute(method_name, arguments))
        data["method"] = method_name
        return data

    except Exception as e:
        return {"error": str(e)}
