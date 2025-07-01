from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from chat.rag_pipeline import RAGChatbot

chatbot = RAGChatbot()

def chat_page(request):
    return render(request, "chat.html")

class ChatAPIView(APIView):
    def post(self, request):
        message = request.data.get("message")
        if not message:
            return Response({"error": "Missing 'message'"}, status=status.HTTP_400_BAD_REQUEST)
        answer = chatbot.answer(message)
        return Response({"response": answer})
