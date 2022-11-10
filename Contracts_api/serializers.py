from rest_framework import serializers
from Contracts_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing out APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user


class ContractSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        """meta class"""
        model = models.Contract
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}


class ContractItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ContractItems
        fields = ('id', 'name', 'price', 'quantity')

    def validate(self, data):
        if data['quantity'] < 0:
            raise serializers.ValidationError("Product quantity can't be negative")
        return data

class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hospital
        fields = ('id', 'name', 'price', 'quantity')

    def validate(self, data):
        if data['quantity'] < 0:
            raise serializers.ValidationError("Product quantity can't be negative")
        return data

class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Warehouse
        fields = ('id', 'name', 'price', 'quantity')

    def validate(self, data):
        if data['quantity'] < 0:
            raise serializers.ValidationError("Product quantity can't be negative")
        return data

class InvoiceSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, invoice):
        return InvoiceItemSerializer(invoice.invoiceitem_set.all(), many=True).data

    class Meta:
        model = models.Invoice
        fields = ('id', 'client', 'date', 'total', 'items')


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InvoiceItem
        fields = ('id', 'product', 'invoice', 'quantity', 'price', 'total')
        extra_kwargs = {'total': {'read_only': True}, 'price ': {'read_only': True}}
