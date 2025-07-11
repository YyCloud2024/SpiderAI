
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path("api/", include("BloodSpiderAPI.api.urls")),
]
# 添加媒体文件URL配置
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
