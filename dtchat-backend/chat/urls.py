from django.urls import path
from .views import ask_gpt

urlpatterns = [
    path('ask/', ask_gpt, name='ask_gpt'),  # 这里定义了一个 URL 路由
]
