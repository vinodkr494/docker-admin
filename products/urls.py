from django.urls import path
from .views import ProductGenericAPIView,FileUploadView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('products', ProductGenericAPIView.as_view()),
    path('products/<str:pk>', ProductGenericAPIView.as_view()),
    path('upload', FileUploadView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
