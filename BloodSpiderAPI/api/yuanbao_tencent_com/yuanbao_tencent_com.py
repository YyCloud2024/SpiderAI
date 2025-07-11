import json
from spider.yuanbao_tencent_com import main as yuanbao_tencent
from spider.yuanbao_tencent_com.upload import UploadTool
from spider.yuanbao_tencent_com.image_manage import ImageManage
from BloodSpiderModel.spider_tools.file_operate import FileOperate
from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict
from django.http import StreamingHttpResponse
from django.conf import settings

# 文件脚本
file_operate = FileOperate()

# 元宝配置
yuanbao_config = json.loads(file_operate.read_file("config.json"))['yuanbao_tencent_com']
# 初始化
yuanbao = yuanbao_tencent.YuanBao(yuanbao_config)

# 上传文件脚本
upload_tools = UploadTool(yuanbao)

# 图片管理
image_manage = ImageManage(yuanbao)


# 生成图片 画图
def generate_images(request):
    if request.method == "GET":
        prompt = request.GET.get("prompt")
        style = request.GET.get("style")
        chat_id = request.GET.get("chat_id")
        response = yuanbao.handle_stream_response_websocket(image_manage.generate_images(prompt, chat_id, style))
        return StreamingHttpResponse(response, content_type="text/event-stream")
    else:
        return response_dict(2, "请求方式错误", None)


# 获取生成的图片风格
def get_generate_images_style(request):
    if request.method == "GET":
        response = image_manage.get_style()
        return response_dict(0, "获取成功", response)
    else:
        return response_dict(2, "请求方式错误", None)


# 更改图片清晰
def sharpen(request):
    if request.method == "POST":
        image_url = request.POST.get("image_url")
        response = yuanbao.handle_stream_response_websocket(image_manage.image_sharpen(image_url))
        return StreamingHttpResponse(response, content_type="text/event-stream")
    else:
        return response_dict(2, "请求方式错误", None)


# 去除水印
def remove_watermark(request):
    if request.method == "POST":
        image_url = request.POST.get("image_url")
        response = yuanbao.handle_stream_response_websocket(image_manage.image_remove_watermark(image_url))
        return StreamingHttpResponse(response, content_type="text/event-stream")
    else:
        return response_dict(2, "请求方式错误", None)


# 图片风格转换
def style_conversion(request):
    if request.method == "POST":
        image_url = request.POST.get("image_url")
        style = request.POST.get("style")
        response = yuanbao.handle_stream_response_websocket(image_manage.image_style_conversion(image_url, style))
        return StreamingHttpResponse(response, content_type="text/event-stream")
    else:
        return response_dict(2, "请求方式错误", None)


# 上传文件
def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        # 保存到本地
        file_path = file_operate.save_file(file, settings.MEDIA_ROOT + "/temp_upload/file")
        response = upload_tools.upload_file(file_path)
        # 删除本地文件
        file_operate.delete_file(file_path)
        return response_dict(0, "上传成功", data=response)
    else:
        return response_dict(2, "请求方式错误", None)


# 创建对话ID
def create_chat_id(request):
    chat_id = yuanbao.create_chat()
    return response_dict(data=chat_id, message="创建对话ID成功")


# 对话
def chat_message(request):
    if request.method == "GET":
        chat_id = request.GET.get('chat_id')
        message = request.GET.get('message', "Hi，你是谁?")
        yuanbao_model = request.GET.get('yuanbao_model', "hunyuan_gpt_175B_0404")
        multimedia = request.GET.get('multimedia') if json.loads(request.GET.get('multimedia')) else []

        response = yuanbao.handle_stream_response_websocket(
            yuanbao.send_message(message, chat_id, yuanbao_model, multimedia))

        return StreamingHttpResponse(response, content_type="text/event-stream")


# 获取历史对话
def get_chat_history(request):
    if request.method == "GET":
        offset = request.GET.get('offset')
        limit = request.GET.get('limit')
        response = yuanbao.get_chat_history(offset, limit)
        return response_dict(data=response, message='获取历史对话成功')


# 获取对话内容
def get_chat_content(request):
    if request.method == "GET":
        chat_id = request.GET.get('chat_id')
        offset = request.GET.get('offset')
        limit = request.GET.get('limit')
        response = yuanbao.get_chat_content(chat_id, offset, limit)
        return response_dict(data=response, message='获取对话内容')


# 删除对话
def delete_chat(request):
    chat_id = request.GET.get('chat_id')
    response = yuanbao.delete_chat(chat_id)
    return response_dict(data=response, message='删除对话成功')
