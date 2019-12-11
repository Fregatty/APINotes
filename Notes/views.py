from django.contrib.auth import authenticate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK)
from .serializers import NoteSerializer
from .models import Note


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Provide both username and password'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)


class NoteView(APIView):
    def get(self, request):
        notes = Note.objects.all().order_by('title')

        paginator = Paginator(notes, 10)
        page = request.GET.get('page')

        try:
            note_page = paginator.page(page)
        except PageNotAnInteger:
            note_page = paginator.page(1)
        except EmptyPage:
            note_page = paginator.page(paginator.num_pages)
        serializer = NoteSerializer(note_page, many=True)
        return Response({"notes": serializer.data})

    def post(self, request):
        note = request.data.get('note')
        serializer = NoteSerializer(data=note)
        if serializer.is_valid(raise_exception=True):
            note_saved = serializer.save()
        return Response({"success": "Note '{}' created".format(note_saved.title)})

    def put(self, request, pk):
        note = get_object_or_404(Note.objects.all(), pk=pk)
        data = request.data.get("note")
        serializer = NoteSerializer(instance=note, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            saved_note = serializer.save()

        return Response({
                "success": "Note '{}' updated successfully".format(saved_note.title)
            })

    def delete(self, request, pk):
        note = get_object_or_404(Note.objects.all(), pk=pk)
        note.delete()
        return Response({
            "message": "Note with id `{}` has been deleted.".format(pk)
        }, status=204)
