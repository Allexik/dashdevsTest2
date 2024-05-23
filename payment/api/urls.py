from rest_framework.routers import DefaultRouter

from .views import BalanceViewSet, TransactionViewSet

router = DefaultRouter()

router.register(r'balance', BalanceViewSet, basename='balance')
router.register(r'transaction', TransactionViewSet, basename='transaction')

urlpatterns = router.urls
