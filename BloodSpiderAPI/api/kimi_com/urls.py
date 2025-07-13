
from django.urls import path
from BloodSpiderAPI.api.kimi_com import kimi_com

# kimi_com
urlpatterns = [

    # 创建对话ID
    path("create_chat_id/", kimi_com.create_chat_id),
    # 对话
    path("chat/completion/", kimi_com.chat_message),
    # 获取历史对话
    path("get_chat_history/", kimi_com.get_chat_history),
    # 获取对话内容
    path("get_chat_content/", kimi_com.get_chat_content),   
    # 删除对话
    path("delete_chat/", kimi_com.delete_chat),
    # 上传文件
    path("upload_file/", kimi_com.upload_file),
]
