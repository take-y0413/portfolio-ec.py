from django.urls import path
from book import views as book_v

app_name = 'book'
urlpatterns = [
    path('detail/<int:pk>/', book_v.BookDetail.as_view(), name='detail'),
]
