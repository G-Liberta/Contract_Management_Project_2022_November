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
        fields = ('id', 'subject', 'hospital', 'product', 'deadline', 'prot_nr', 'sign_date', 'total_value')


class ContractItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ContractItem
        fields = ('id', 'name', 'quantity', 'price',)

    def validate(self, data):
        if data['quantity'] < 0:
            raise serializers.ValidationError("Product quantity can't be negative")
        return data

class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hospital
        fields = ('id', 'name', 'adress', 'email', 'phone_nr')

    def validate(self, data):
        if data['name'] == None:
            raise serializers.ValidationError("Hospital must have a name")
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
        fields = ('id', 'contract_id', 'date', 'total', 'items')


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InvoiceItem
        fields = ('id', 'warehouse_id','invoice_id', 'quantity', 'price', 'total')
        extra_kwargs = {'total': {'read_only': True}, 'price ': {'read_only': True}}
