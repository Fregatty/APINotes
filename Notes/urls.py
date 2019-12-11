from django.urls import path
from .views import NoteView, login
from django.views.decorators.csrf import csrf_exempt

app_name = "notes"

urlpatterns = [
    path('notes/', NoteView.as_view()),
    path('notes/<int:pk>', csrf_exempt(NoteView.as_view())),
    path('login/', login)
]