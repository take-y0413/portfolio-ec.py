from django.urls import path
from store import views as store_v

app_name = 'store'
urlpatterns = [
    path('', store_v.Home.as_view(), name='home'),
    path('add_sessioncart/', store_v.SessionAddToCart.as_view(), name='add_sessioncart'),
    path('sessioncontent/', store_v.SessionCartContent.as_view(), name='sessioncart_content'),
    path('add_modelcart/', store_v.ModelAddToCart.as_view(), name='add_modelcart'),
    path('modelcontent/<int:pk>/', store_v.ModelCartContent.as_view(), name='modelcart_content'), # pk は CartUnitのpk
    path('delete_modelcart/', store_v.ModelCartDelete.as_view(), name='modelcart_delete'),
    path('delete_sessioncart/', store_v.SessionCartDelete.as_view(), name='sessioncart_delete'),
    path('purchase/preview/', store_v.PurchasePreview.as_view(), name='purchase_preview'),
    path('purchase/_process/', store_v.PurchaseProcess.as_view(), name='_purchase_process'),
    path('purchase/done/', store_v.PurchaseDone.as_view(), name='purchase_done'),
]
