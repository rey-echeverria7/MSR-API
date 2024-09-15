from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Refaccion
from .serializer import RefaccionSerializer

# Create your views here.
class RefaccionViewSet(viewsets.ModelViewSet):
    queryset= Refaccion.objects.all()
    serializer_class = RefaccionSerializer
    

     # Custom action to get all products with a custom route
    @action(detail=False, methods=['get'], url_path='listaRefacciones')
    def lista_refacciones(self, request):
        queryset = Refaccion.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)