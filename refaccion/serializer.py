from rest_framework import serializers
from .models import Refaccion

class RefaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refaccion
        #fields=('id', 'nombre', 'descripcion', 'precio')
        fields = '__all__'