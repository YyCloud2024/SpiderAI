
from django.urls import path
from BloodSpiderAPI.api.yuanbao_tencent_com import yuanbao_tencent_com

# yuanbao_tencent_com
urlpatterns = [

    # 创建对话ID
    path("create_chat_id/", yuanbao_tencent_com.create_chat_id),
    # 对话
    path("chat/completion/", yuanbao_tencent_com.chat_message),
    # 获取历史对话
    path("get_chat_history/", yuanbao_tencent_com.get_chat_history),
    # 获取对话内容
    path("get_chat_content/", yuanbao_tencent_com.get_chat_content),
    # 删除对话
    path("delete_chat/", yuanbao_tencent_com.delete_chat),
    # 上传文件
    path("upload_file/", yuanbao_tencent_com.upload_file),
    # 生成图片 画图
    path("generate_images/", yuanbao_tencent_com.generate_images),
    # 获取生成的图片风格
    path("get_generate_images_style/", yuanbao_tencent_com.get_generate_images_style),
    # 更改图片清晰
    path("sharpen/", yuanbao_tencent_com.sharpen),
    # 去除水印
    path("remove_watermark/", yuanbao_tencent_com.remove_watermark),
    # 图片风格转换
    path("style_conversion/", yuanbao_tencent_com.style_conversion),
]
