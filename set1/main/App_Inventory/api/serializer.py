from rest_framework import serializers
from django.utils import timezone
from App_Inventory.models import CarInventory

class CarInventorySerializer(serializers.ModelSerializer):

    qr_code = serializers.SerializerMethodField()

    class Meta:
        model = CarInventory
        exclude = ['QR_CODE','created','updated']
    
    def get_qr_code(self,object):
        return object.QR_CODE.url
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.model = validated_data.get('model',instance.model)
        instance.company_name = validated_data.get('company_name',instance.company_name)
        instance.year = validated_data.get('year',instance.year)
        instance.price = validated_data.get('price',instance.price)
        instance.mileage = validated_data.get('mileage',instance.mileage)
        instance.description = validated_data.get('description',instance.description)
        instance.is_avaliable = validated_data.get('is_avaliable',instance.is_avaliable)
        instance.image = validated_data.get('image',instance.image)
        instance.QR_CODE = validated_data.get('QR_CODE',instance.QR_CODE)

        instance.updated = timezone.now()
        instance.save()
        return instance
