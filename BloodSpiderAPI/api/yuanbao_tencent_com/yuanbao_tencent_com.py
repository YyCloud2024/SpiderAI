import json
import time

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

# 验证必要参数是否存在
def validate_required_params(params, required):
    for param in required:
        if param not in params or not params[param]:
            return False
    return True

# 生成图片 画图
def generate_images(request):
    if request.method != "GET":
        return response_dict(2, "请求方式错误，此接口仅支持GET请求", None)
    required_params = ['prompt', 'chat_id']
    if not validate_required_params(request.GET, required_params):
        return response_dict(1, f"缺少必要参数，需要参数: {', '.join(required_params)}", None)
    prompt = request.GET.get("prompt")
    style = request.GET.get("style")
    chat_id = request.GET.get("chat_id")
    try:
        response = yuanbao.handle_stream_response_websocket(image_manage.generate_images(prompt, chat_id, style))
        return StreamingHttpResponse(response, content_type="text/event-stream")
    except Exception as e:
        return response_dict(3, f"生成图片时出现错误: {str(e)}", None)

# 获取生成的图片风格
def get_generate_images_style(request):
    if request.method != "GET":
        return response_dict(2, "请求方式错误，此接口仅支持GET请求", None)
    try:
        response = image_manage.get_style()
        return response_dict(0, "获取成功", response)
    except Exception as e:
        return response_dict(3, f"获取图片风格时出现错误: {str(e)}", None)

# 更改图片清晰
def sharpen(request):
    if request.method != "POST":
        return response_dict(2, "请求方式错误，此接口仅支持POST请求", None)
    required_params = ['image_url']
    if not validate_required_params(request.POST, required_params):
        return response_dict(1, f"缺少必要参数，需要参数: {', '.join(required_params)}", None)
    image_url = request.POST.get("image_url")
    try:
        response = yuanbao.handle_stream_response_websocket(image_manage.image_sharpen(image_url))
        return StreamingHttpResponse(response, content_type="text/event-stream")
    except Exception as e:
        return response_dict(3, f"更改图片清晰度时出现错误: {str(e)}", None)

# 去除水印
def remove_watermark(request):
    if request.method != "POST":
        return response_dict(2, "请求方式错误，此接口仅支持POST请求", None)
    required_params = ['image_url']
    if not validate_required_params(request.POST, required_params):
        return response_dict(1, f"缺少必要参数，需要参数: {', '.join(required_params)}", None)
    image_url = request.POST.get("image_url")
    try:
        response = yuanbao.handle_stream_response_websocket(image_manage.image_remove_watermark(image_url))
        return StreamingHttpResponse(response, content_type="text/event-stream")
    except Exception as e:
        return response_dict(3, f"去除水印时出现错误: {str(e)}", None)

# 图片风格转换
def style_conversion(request):
    if request.method != "POST":
        return response_dict(2, "请求方式错误，此接口仅支持POST请求", None)
    required_params = ['image_url', 'style']
    if not validate_required_params(request.POST, required_params):
        return response_dict(1, f"缺少必要参数，需要参数: {', '.join(required_params)}", None)
    image_url = request.POST.get("image_url")
    style = request.POST.get("style")
    try:
        response = yuanbao.handle_stream_response_websocket(image_manage.image_style_conversion(image_url, style))
        return StreamingHttpResponse(response, content_type="text/event-stream")
    except Exception as e:
        return response_dict(3, f"图片风格转换时出现错误: {str(e)}", None)

# 上传文件
def upload_file(request):
    if request.method != "POST":
        return response_dict(2, "请求方式错误，此接口仅支持POST请求", None)
    file = request.FILES.get("file")
    if not file:
        return response_dict(1, "缺少文件，请上传有效的文件", None)
    try:
        # 保存到本地
        file_path = file_operate.save_file(file, settings.MEDIA_ROOT + "/temp_upload/file")
        response = upload_tools.upload_file(file_path)
        # 删除本地文件
        file_operate.delete_file(file_path)
        return response_dict(0, "上传成功", data=response)
    except Exception as e:
        return response_dict(3, f"上传文件时出现错误: {str(e)}", None)

# 创建对话ID
def create_chat_id(request):
    try:
        chat_id = yuanbao.create_chat()
        return response_dict(data=chat_id, message="创建对话ID成功")
    except Exception as e:
        return response_dict(3, f"创建对话ID时出现错误: {str(e)}", None)

# 对话
def chat_message(request):
    if request.method != "POST":
        return response_dict(2, "请求方式错误，此接口仅支持GET请求", None)
    required_params = ['chat_id', 'message']
    if not validate_required_params(request.POST, required_params):
        return response_dict(1, f"缺少必要参数，需要参数: {', '.join(required_params)}", None)
    chat_id = request.POST.get('chat_id')
    message = request.POST.get('message')
    yuanbao_model = request.POST.get('yuanbao_model', "hunyuan_gpt_175B_0404")
    multimedia_str = request.POST.get('multimedia', '[]')
    try:
        multimedia = json.loads(multimedia_str)
    except json.JSONDecodeError:
        return response_dict(1, "多媒体参数格式错误，请提供有效的JSON数组", None)
    try:
        response = yuanbao.handle_stream_response_websocket(
            yuanbao.send_message(message, chat_id, yuanbao_model, multimedia))
        return StreamingHttpResponse(response, content_type="text/event-stream")
    except Exception as e:
        return response_dict(3, f"对话时出现错误: {str(e)}", None)

# 获取历史对话
def get_chat_history(request):
    if request.method != "GET":
        return response_dict(2, "请求方式错误，此接口仅支持GET请求", None)
    required_params = ['offset', 'limit']
    if not validate_required_params(request.GET, required_params):
        return response_dict(1, f"缺少必要参数，需要参数: {', '.join(required_params)}", None)
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')
    try:
        response = yuanbao.get_chat_history(offset, limit)
        return response_dict(data=response, message='获取历史对话成功')
    except Exception as e:
        return response_dict(3, f"获取历史对话时出现错误: {str(e)}", None)

# 获取对话内容
def get_chat_content(request):
    if request.method != "GET":
        return response_dict(2, "请求方式错误，此接口仅支持GET请求", None)
    required_params = ['chat_id', 'offset', 'limit']
    if not validate_required_params(request.GET, required_params):
        return response_dict(1, f"缺少必要参数，需要参数: {', '.join(required_params)}", None)
    chat_id = request.GET.get('chat_id')
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')
    try:
        response = yuanbao.get_chat_content(chat_id, offset, limit)
        return response_dict(data=response, message='获取对话内容成功')
    except Exception as e:
        return response_dict(3, f"获取对话内容时出现错误: {str(e)}", None)

# 删除对话
def delete_chat(request):
    if request.method != "GET":
        return response_dict(2, "请求方式错误，此接口仅支持GET请求", None)
    required_params = ['chat_id']
    if not validate_required_params(request.GET, required_params):
        return response_dict(1, f"缺少必要参数，需要参数: {', '.join(required_params)}", None)
    chat_id = request.GET.get('chat_id')
    try:
        response = yuanbao.delete_chat(chat_id)
        return response_dict(data=response, message='删除对话成功')
    except Exception as e:
        return response_dict(3, f"删除对话时出现错误: {str(e)}", None)