from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from dds.models import CashFlow, Status, OperationType, Category, SubCategory
from .serializers import CashFlowSerializer, StatusSerializer, OperationTypeSerializer, CategorySerializer, SubcategorySerializer

# берем только активные записи из справочников


class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Status.objects.filter(is_active=True)
    serializer_class = StatusSerializer


class OperationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OperationType.objects.filter(is_active=True)
    serializer_class = OperationTypeSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.filter(is_active=True)
    serializer_class = SubcategorySerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):  # убираем csrf
    def enforce_csrf(self, request):
        return


class CashFlowViewSet(viewsets.ModelViewSet):
    queryset = CashFlow.objects.all()
    serializer_class = CashFlowSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        # фильтруем по параметрам
        qs = super().get_queryset()
        params = self.request.query_params
        if params.get('start_date'):
            qs = qs.filter(created_at__gte=params['start_date'])
        if params.get('end_date'):
            qs = qs.filter(created_at__lte=params['end_date'])
        if params.get('status'):
            qs = qs.filter(status_id=params['status'])
        if params.get('operation_type'):
            qs = qs.filter(operation_type_id=params['operation_type'])
        if params.get('category'):
            qs = qs.filter(category_id=params['category'])
        if params.get('subcategory'):
            qs = qs.filter(subcategory_id=params['subcategory'])
        qs = qs.order_by('-created_at')  # сортировка от новых к старым
        return qs
