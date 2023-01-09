from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import permissions


from .models import Note
from accounts.authentication import JWTAuthentication


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def notes(request):
    if request.method == 'POST':
        return create_note(request)
    if request.method == 'GET':
        return get_notes(request)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def notes_pk(request, pk):
    if request.method == 'GET':
        return get_note(request, pk)
    if request.method == 'PUT':
        return update_note(request, pk)
    if request.method == 'DELETE':
        return delete_note(request, pk)


def get_notes(request):
    notes = Note.objects.all()
    return Response([note.to_dict() for note in notes])


def get_note(request, pk):
    note = Note.objects.get(id=pk)
    return Response(note.to_dict())


def create_note(request):
    note = Note.objects.create(
        body=request.data['body']
    )
    return Response(note.to_dict())


def update_note(request, pk):
    note = Note.objects.get(id=pk)
    note.body = request.data['body']
    note.save()
    return Response(note.to_dict())


def delete_note(request, pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return Response(note.to_dict())