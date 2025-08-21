from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('chat', views.ChatbotChatView.as_view(), name="chatbot_chat"),
    path('courses/<int:course_id>/attempts/<int:attempt_id>/prompts/<prompt_index>/conversations', views.ChatbotConversationView.as_view(), name="chatbot_conversation"),
    path('conversations/<int:conversation_id>/chat/', views.ChatbotMessageView.as_view(), name="chatbot_message"),
    path('conversations/<int:conversation_id>/feedback/', views.ChatbotFeedbackView.as_view(), name="chatbot_feedback"),
]