from django.shortcuts import render
from django.views import View
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class ChatView(View):
    def get(self, request, *args, **kwargs):
        conversations = request.session.get('conversations',[])
        return render(request, 'chat.html', {'conversations': conversations})
    
    def post(self, request, *args, **kwargs):
        prompt = request.POST.get('prompt')
        if prompt:
            session_conversations = request.session.get('conversations', [])
            previous_conversations = "\n".join([f"User: {c['prompt']}\nAI: {c['response']}" for c in session_conversations])
            prompt_with_previous = f"{previous_conversations}\nUser: {prompt}\nAI:"
            model_engine = "text-davinci-003"
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt_with_previous,
                max_tokens=1024,
                n=5,
                stop=None,
                temperature=0.5,
            )
            response = completions.choices[0].text.strip()
            conversation = {'prompt' : prompt, 'response' : response}

            session_conversations.append(conversation)
            request.session['conversations'] = session_conversations

        return self.get(request, *args, **kwargs)

