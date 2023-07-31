from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from dotenv import load_dotenv
import openai
import os
from .models import Conversation


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class ChatView(View):
    def get(self, request, *args, **kwargs):
        conversations = request.session.get('conversations', [])
        return render(request, 'chat.html', {'conversations': conversations})

    # def post(self, request):
    #     chat = request.data
    #     serializer = self.serializer_class(data=chat)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        prompt = request.POST.get('prompt')
        if prompt:
            # 이전 대화 기록 가져오기
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

            conversation = Conversation(prompt=prompt, response=response)
            conversation.save()

            # 대화 기록에 새로운 응답 추가
            session_conversations.append({'prompt': prompt, 'response': response})
            request.session['conversations'] = session_conversations
            request.session.modified = True

        return self.get(request, *args, **kwargs)


# def chatbot(request):
    # 이전 코드 내용을 그대로 유지하고, 마지막에 JsonResponse로 응답을 반환합니다.
    # 예시로 {"choices": [{"message": {"response": "답변 내용"}}]} 형식으로 응답한다고 가정합니다.
    # 실제로는 원하는 JSON 응답 형식으로 수정해야 합니다.
    # return JsonResponse({"choices": [{"message": {"response": "답변 내용"}}]})

