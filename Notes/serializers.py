from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30)
    date = serializers.DateField(required=False)
    body = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance
