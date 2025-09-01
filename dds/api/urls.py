from rest_framework.routers import DefaultRouter
from .views import CashFlowViewSet, StatusViewSet, OperationTypeViewSet, CategoryViewSet, SubCategoryViewSet

router = DefaultRouter()  # роутер для автоматической генерации путей
router.register(r'cashflows', CashFlowViewSet, basename='cashflows')
router.register(r'statuses', StatusViewSet, basename='statuses')
router.register(r'operationtypes', OperationTypeViewSet,
                basename='operationtypes')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategories')

urlpatterns = router.urls
