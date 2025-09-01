from rest_framework import serializers
from dds.models import CashFlow, Status, OperationType, Category, SubCategory


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']


class OperationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationType
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    operation_type = serializers.IntegerField(
        source='operation_type.id')  # связанный тип операции

    class Meta:
        model = Category
        fields = ['id', 'name', 'operation_type']


class SubcategorySerializer(serializers.ModelSerializer):
    category = serializers.IntegerField(
        source='category.id')  # связанная категория

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']


class CashFlowSerializer(serializers.ModelSerializer):
    # связанные поля
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())
    operation_type = serializers.PrimaryKeyRelatedField(
        queryset=OperationType.objects.all())
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all())

    class Meta:
        model = CashFlow
        fields = ['id', 'created_at', 'status', 'operation_type',
                  'category', 'subcategory', 'amount', 'comment']
