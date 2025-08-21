from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .services.chatbot import ChatbotService
from .serializers import ConversationSerializer

class ChatbotChatView(views.APIView):

    def post(self, request, *args, **kwargs):
        chatbot_service = ChatbotService()
        model = request.data.get('model')
        prompt = request.data.get('prompt')
        message = request.data.get('message')

        if not model:
            return Response({"error": "model field is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not message:
            return Response({"error": "message field is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            message = chatbot_service.chat(
                model=model,
                prompt=prompt,
                message=message
            )
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChatbotConversationView(views.APIView):

    def get(self, request, course_id, attempt_id, prompt_index, *args, **kwargs):
        chatbot_service = ChatbotService()
        conversations = chatbot_service.get_attempt_conversations(attempt_id=attempt_id, course_id=course_id, prompt_index=prompt_index)
        serializer = ConversationSerializer(conversations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, course_id, attempt_id, prompt_index, *args, **kwargs):
        chatbot_service = ChatbotService()
        model = request.data.get('model')

        if not model:
            return Response({"error": "model field is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            conversation = chatbot_service.initialize_conversation(
                attempt_id=attempt_id,
                course_id=course_id,
                prompt_index=prompt_index,
                model=model
            )
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": "Prompt not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f'Error initializing conversation: {e}')
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ChatbotMessageView(views.APIView):
    
    def post(self, request, conversation_id, *args, **kwargs):
        chatbot_service = ChatbotService()
        message = request.data.get('message')

        if not message:
            return Response({"error": "message field is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            response = chatbot_service.send_message(
                message=message, 
                conversation_id=conversation_id,
            )
            return Response(response, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": "Conversation not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f'Error sending message: {e}')
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ChatbotFeedbackView(views.APIView):
    
    def post(self, request, conversation_id, *args, **kwargs):
        chatbot_service = ChatbotService()
        prepend = request.data.get('prepend', False)
        model = request.data.get('model')

        if not model:
            return Response({"error": "model field is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            feedback = chatbot_service.get_feedback(conversation_id, model, prepend)
            return Response({"feedback": feedback}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": "Conversation not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f'Error fetching feedback: {e}')
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)