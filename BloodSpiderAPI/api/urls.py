
from django.urls import path, include

urlpatterns = [
    path("yuanbao_tencent_com/", include("BloodSpiderAPI.api.yuanbao_tencent_com.urls"))
]
