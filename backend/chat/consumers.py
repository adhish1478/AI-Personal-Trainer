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
            # If all questions are answered, process the answers
            user_details = "\n".join(
            f"{q} {a}" for q, a in zip(PREDEFINED_QUESTIONS, self.answers)
            )

            prompt= f"""Based on the following user information, recommend a personalized fitness plan:

            {user_details}
             

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
            #print("RAW AI RESPONSE:", text)
            '''try:
                # Remove triple backticks and optional json tag using regex
                #cleaned_text= re.sub(r'^```json\s*|\s*```', '', text.strip(), flags= re.MULTILINE).strip()

                parsed= json.loads(text)
            except Exception:
                explanation= 'Invalid response from AI.' '''

            # Send the AI response back to the client
            await self.send(text_data=json.dumps({
            "message": text,
            "from_llm": True
             }))

            

    async def send_question(self):
        if self.question_index < len(PREDEFINED_QUESTIONS):
            question = PREDEFINED_QUESTIONS[self.question_index]
            await self.send(text_data=json.dumps({
                'message': question
            }))
            self.question_index += 1


    async def disconnect(self, close_code):
        pass

