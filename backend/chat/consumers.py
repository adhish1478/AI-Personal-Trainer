import json
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import UserProfile
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import ChatMessage

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
        #await self.send_question()

    async def receive(self, text_data):
        # Testing if the user is authenticated- temporary
        # ---------------------------------------------------
        user = self.scope['user']
        if not user.is_authenticated:
            await self.send(text_data=json.dumps({
                "message": "You must be logged in to use the chatbot.",
                "from_llm": False
            }))
            return
        # ---------------------------------------------------
        data = json.loads(text_data)
        message = data.get('message')

    
        # Store the answer
        if message:
            self.answers.append(message)

            # Save the chat message to the database
            await sync_to_async(ChatMessage.objects.create)(
                user= user,
                is_from_user= True,
                message= message,
            )


        if self.question_index < len(PREDEFINED_QUESTIONS):
            #await self.send_question()
            pass
        else:
            # If all questions are answered, process the answers

            # Get user details from the database
            # user_id = self.scope.get("user_id", None)

            try:
                profile= await sync_to_async(UserProfile.objects.get)(user_id=user.id)
                profile_data = f"""
                Age: {profile.age}
                Goal: {profile.goal}
                Maintenance Calories: {profile.maintanance_cals}
                Goal Calories: {profile.goal_cals}
                Carbs: {profile.carbs}
                Protein: {profile.protein}
                Fat: {profile.fats}
                Fibre: {profile.fibre}
                Cuisine Preferences: {profile.cuisine}
                Allergies: {profile.allergies}
                """
            except UserProfile.DoesNotExist:
                profile_data= 'Profile not found.'

            # If all questions are answered, process the answers
            chat_data = "\n".join(
            f"{q} {a}" for q, a in zip(PREDEFINED_QUESTIONS, self.answers)
            )

            # Generate the prompt for the LLM
            prompt= f"""Based on the following user profile and chat answers, generate a personalized meal plan which contains
            a meal plan which includes breakfast, lunch, dinner and snacks.:

            User Profile:
            {profile_data}

            Chat Data:
            {chat_data}
             

            """

            # LLm logic here
            from google import genai
            from django.conf import settings
            import re
            
            client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )
            response= client.models.generate_content(
                model="gemini-2.5-flash", contents= prompt,
            )

            text= (
                response.candidates[0].content.parts[0].text
                if response.candidates and response.candidates[0].content.parts
                else "No response from AI."
            )
        
            # Send the AI response back to the client
            await self.send(text_data=json.dumps({
            "message": text,
            "from_llm": True
             }))

            

    '''async def send_question(self):
        if self.question_index < len(PREDEFINED_QUESTIONS):
            question = PREDEFINED_QUESTIONS[self.question_index]
            await self.send(text_data=json.dumps({
                'message': question
            }))
            self.question_index += 1
'''

    async def disconnect(self, close_code):
        pass

