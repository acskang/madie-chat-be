import json
from django.http import JsonResponse, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic import View
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

chatbot = ChatBot("Madie")

conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome.",
    "안~~녕~~~!",
    "반가워 ^^",
    "^_________^ Hi!",

]

trainer = ListTrainer(chatbot)
trainer.train(conversation)

class MadieBotAppView(TemplateView):
    template_name = 'chatroom.html'

@method_decorator(csrf_exempt, name='dispatch')
class MadieBotApiView(View):
    def post(self, request, *args, **kwargs):
        input_data = json.loads(request.body.decode('utf-8'))
        if "text" not in input_data:
            return JsonResponse({
                'text': ['The attribute "text" is required.']
            }, status=400)
        response = chatbot.get_response(input_data)
        response_data = response.serialize()
        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({
            'name': self.chatterbot.name
        })