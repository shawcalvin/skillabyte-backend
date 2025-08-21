import openai

from django.conf import settings

from ..models import Prompt, Conversation, PromptIndex

class ChatbotService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ChatbotService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        openai.organization = settings.OPENAI_ORGANIZATION
        
    def get_prompt(self, course_id, prompt_index):
        try:
            return PromptIndex.objects.get(course_id=course_id, index=prompt_index).prompt
        except PromptIndex.DoesNotExist:
            raise ValueError("Prompt does not exist for the given course and index.")

    def get_conversation(self, id):
        try:
            return Conversation.objects.get(
                id=id
            )
        except Conversation.DoesNotExist:
            raise ValueError("Conversation does not exist.")
        
    def get_attempt_conversations(self, attempt_id, course_id, prompt_index):
        try:
            prompt = PromptIndex.objects.get(course_id=course_id, index=prompt_index).prompt
        except PromptIndex.DoesNotExist:
            return None

        return Conversation.objects.filter(
            attempt_id=attempt_id,
            prompt=prompt
        )

    def get_feedback(self, id, model, prepend=False):
        conversation = self.get_conversation(id)
        if not conversation.feedback:
            messages = conversation.messages[1:]
            if prepend == True:
                messages = [{"role": "system", "content": conversation.prompt.feedback_prompt}] + messages
            else:
                messages.append({"role": "system", "content": conversation.prompt.feedback_prompt})
            response = openai.chat.completions.create(
                model=model,
                messages=messages
            )
            response_content = response.choices[0].message.content
            conversation.feedback = response_content
            self.save_conversation(conversation)
        return conversation.feedback
    
    def initialize_conversation(self, attempt_id, course_id, prompt_index, model):
        prompt = self.get_prompt(course_id, prompt_index)
        messages = [{"role": "system", "content": prompt.prompt}]

        try:
            response = openai.chat.completions.create(
                model=model,
                messages=messages
            )

            response_content = response.choices[0].message.content
            conversation = Conversation.objects.create(
                attempt_id=attempt_id,
                prompt=prompt, 
                model=model,
                messages=messages
            )
            conversation.messages.append({"role": "assistant", "content": response_content})
            self.save_conversation(conversation)

            return conversation
        except Exception as e:
            raise e
    
    def send_message(self, message, conversation_id):
        conversation = self.get_conversation(conversation_id)
        conversation.messages.append(
            {"role": "user", "content": message}
        )

        response = openai.chat.completions.create(
            model=conversation.model,
            messages=conversation.messages
        )

        response_content = response.choices[0].message.content
        message = {"role": "assistant", "content": response_content}
        conversation.messages.append(message)
        self.save_conversation(conversation)

        return message
    
    def chat(self, model, prompt, message):
        messages = []
        if prompt:
            messages.append({"role": "assistant", "content": prompt})
        
        messages.append({"role": "user", "content": message})

        response = openai.chat.completions.create(
            model=model,
            messages=messages
        )

        response_content = response.choices[0].message.content
        message = {"role": "assistant", "content": response_content}

        return message
    
    def request_feedback(self):
        pass

    def save_conversation(self, conversation):
        try:
            conversation.save()
        except Exception as e:
            raise ValueError(f"An error occurred while saving the conversation: {str(e)}")