from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .strategy.service import *
from .apis import connectors
from .strategy import *  
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)
# OPENAI_API_KEY = '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'  
GPT_MODEL = 'gpt-4o-2024-08-06'

client = OpenAI() 

@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def ask_gpt(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question', '')
        messages = [{"role": "user", "content": question}]

        if question:                                                                                                                                     
            response = client.chat.completions.create(
                model=GPT_MODEL,
                messages=messages,
                tools=connectors,
                tool_choice = "auto"
            )

            print("gpt 1st response:", response)
            tool_calls = response.choices[0].message.tool_calls
            response_message = response.choices[0].message
            messages.append(response_message)

            if tool_calls:
                tool_call_id = tool_calls[0].id         
                
                api_response = function_call(question, response)
                print(f"api response: {api_response}")
                method = api_response.get("method")
                api_data = json.dumps(api_response, ensure_ascii=False)
                have_schema = api_response.get("have_schema")

                messages.append({
                    "role": "tool",
                    "name": method,
                    "tool_call_id": tool_call_id, 
                    "content": api_data
                })

                if have_schema:                     
                    messages.append({
                        "role": "user", 
                        "content": f"Here is the data from api call: {api_data}. Please provide a very very concise summary based on the data."
                    })
                
                second_response = client.chat.completions.create(
                    model=GPT_MODEL,
                    messages=messages,
                    tools=connectors,
                    tool_choice = "none",
                    temperature=0.7
                )

                final_answer = second_response.choices[0].message.content
                return JsonResponse({
                    'answer': final_answer,
                    'data': api_response.get('result', {}),
                    'function_name': method
                })

            else:
                print(response)
                return JsonResponse({'answer': response.choices[0].message.content})


        else:
            return JsonResponse({'error': 'No question provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)