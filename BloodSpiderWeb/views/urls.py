from django.urls import path
from BloodSpiderWeb.views import all
urlpatterns = [
    path('', all.index),
    path('index/', all.index),
    # 大模型首页
    path('link/<str:link_name>/', all.big_model_index),
]
