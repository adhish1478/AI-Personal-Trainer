import json
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import UserProfile
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import ChatMessage
# Gemini libraries
from google import genai
from django.conf import settings
import re

PREDEFINED_QUESTIONS = [
    "What's your fitness goal?",
    "Do you have any dietary restrictions?",
    "What is your current activity level?",
]

class ChatBot(AsyncWebsocketConsumer):
    async def connect(self):
        self.question_index = 0
        self.answers= []
        self.last_llm_response = None

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

        # checking wheather last message is confirmation or not
        if message.lower() == 'confirm':
            if self.last_llm_response:
                await self.generate_structured_plan(self.last_llm_response)
            else:
                self.send_error("No previous response to confirm.")
            return

        # checking if the user wants to regenerate the plan
        if message.lower() == 'regenerate':
            if self.last_llm_response:
                await self.regenrate_new_plan(self.last_llm_response)
            else:
                self.send_error("No previous response to regenerate.")
            return
        
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
            self.last_llm_response = text
            # Send the AI response back to the client
            await self.send(text_data=json.dumps({
            "message": text,
            "from_llm": True
             }))

    async def generate_structured_plan(self, raw_plain_text):
        # Process the raw plan text to generate a structured response
        structured_prompt = f"""
        Convert the following fitness plan into structured JSON:
        Return only JSON. No markdown or commentary.

        Plan:
        {raw_plain_text}
        """

        client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=structured_prompt,
        )

        text = response.candidates[0].content.parts[0].text if response.candidates and response.candidates[0].content.parts else "No response from AI."

        # Converting Markdown to JSON
        try:
            cleaned = re.sub(r'^```json\s*|\s*```$', '', text.strip(), flags=re.MULTILINE)
            structured_data= json.loads(cleaned)
        except Exception as e:
            await self.send_error(f"AI did not return valid JSON. Error: {e}")
            return
        
        # Saving the diet plan to the database
        await sync_to_async(DietPlan.objects.create) (
            user= self.scope['user'],
            breakfast=structured_data.get("breakfast"),
            lunch=structured_data.get("lunch"),
            dinner=structured_data.get("dinner"),
            snacks=structured_data.get("snacks"),
            notes=structured_data.get("notes", ""),
        )

        await self.send(text_data= json.dumps({
            "message": "✅ Diet plan saved successfully!",
            "from_llm": False
        }))
    
    async def regenrate_new_plan(self, previous_text):
        # Regenerate a new plan based on the previous response
        prompt = f"""
        Using the following previous plan, create a different meal plan
        with similar calorie/macronutrient structure but **no repetition** in dishes.

        Previous Plan:
        {previous_text}
        """

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )

        text= (
            response.candidates[0].content.parts[0].text
            if response.candidates and response.candidates[0].content.parts
            else "No response from AI."
        )
        self.last_llm_response= text

        # Send the new plan back to the client
        await self.send(text_data= json.dumps({
            'message': text,
            'from_llm': True
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

