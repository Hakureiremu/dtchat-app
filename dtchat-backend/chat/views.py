from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json 

OPENAI_API_KEY = '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'  # 在这里替换为你的 OpenAI API 密钥

@csrf_exempt
def ask_gpt(request):
    print(request.body)
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question', '')
        print("question: ", question)
        if question:
            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json',
            }
            json_data = {
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': question}],
            }

            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=json_data
            )

            if response.status_code == 200:
                answer = response.json()['choices'][0]['message']['content']
                print("answer: ", answer)
                return JsonResponse({'answer': answer})
            else:
                return JsonResponse({'error': 'Failed to get response from OpenAI'}, status=500)
        else:
            return JsonResponse({'error': 'No question provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
