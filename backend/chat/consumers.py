import json
from channels.generic.websocket import AsyncWebsocketConsumer

PREDEFINED_QUESTIONS = [
    "What's your fitness goal?",
    "Do you have any dietary restrictions?",
    "What is your current activity level?",
]

class ChatBot(AsyncWebsocketConsumer):
    async def connect(self):
        self.question_index = 0
        self.answers= []

        await self.accept()
        # Send a welcome message when the socket connects
        await self.send(text_data=json.dumps({
        "message": "Welcome! Ask me anything."
        }))
        await self.send_question()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')

        # Store the answer
        if message:
            self.answers.append(message)
        if self.question_index < len(PREDEFINED_QUESTIONS):
            await self.send_question()
        else:
            await self.send(text_data= json.dumps({
                'message': 'Thank you, generating a personalized plan...',
                'answers': self.answers
            }))
        # LLM logic here

    async def send_question(self):
        if self.question_index < len(PREDEFINED_QUESTIONS):
            question = PREDEFINED_QUESTIONS[self.question_index]
            await self.send(text_data=json.dumps({
                'message': question
            }))
            self.question_index += 1


    async def disconnect(self, close_code):
        pass

