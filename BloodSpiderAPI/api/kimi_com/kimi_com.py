import json
from spider.kimi_com import main as kimi_main
from spider.kimi_com.upload import UploadTool
from BloodSpiderModel.spider_tools.file_operate import FileOperate
from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict
from django.http import StreamingHttpResponse
from django.conf import settings


# 文件操作工具初始化
file_operate = FileOperate()

# 读取kimi配置
kimi_config = json.loads(file_operate.read_file("config.json"))['kimi_com']

# 初始化kimi核心服务
kimi = kimi_main.KiMi_JiChuBan(kimi_config)

# 初始化上传工具
upload_tools = UploadTool(kimi)


# 验证必要参数是否存在
def validate_required_params(params, required):
    for param in required:
        if param not in params or not params[param]:
            return False
    return True

# 创建对话ID
def create_chat_id(request):
    try:
        chat_response = kimi.create_chat()
        chat_id = chat_response
        return response_dict(data=chat_id, message="创建对话ID成功")
    except Exception as e:
        return response_dict(3, f"创建对话ID时出现错误: {str(e)}", None)

# 对话消息交互
def chat_message(request):
    if request.method != "POST":
        return response_dict(2, "请求方式错误，此接口仅支持POST请求", None)
    required_params = ['chat_id', 'message']
    if not validate_required_params(request.POST, required_params):
        return response_dict(1, f"缺少必要参数，需要参数: {', '.join(required_params)}", None)
    
    chat_id = request.POST.get('chat_id')
    message = request.POST.get('message')
    kimi_model = request.POST.get('kimi_model', "kimi")
    use_search = request.POST.get('use_search', 'false').lower() == 'true'
    multimedia_str = request.POST.get('multimedia', '[]')
    
    try:
        multimedia = json.loads(multimedia_str)
    except json.JSONDecodeError:
        return response_dict(1, "多媒体参数格式错误，请提供有效的JSON数组", None)
    
    try:
        response = kimi.handle_stream_response_websocket(
            kimi.send_message(chat_id, message, use_search, kimi_model, multimedia)
        )
        return StreamingHttpResponse(response, content_type="text/event-stream")
    except Exception as e:
        return response_dict(3, f"对话时出现错误: {str(e)}", None)

# 上传文件
def upload_file(request):
    if request.method != "POST":
        return response_dict(2, "请求方式错误，此接口仅支持POST请求", None)
    file = request.FILES.get("file")
    if not file:
        return response_dict(1, "缺少文件，请上传有效的文件", None)
    
    try:
        # 保存到本地临时目录
        file_path = file_operate.save_file(file, settings.MEDIA_ROOT + "/temp_upload/file")
        # 调用kimi上传工具
        response = upload_tools.upload_File(file.name, file_path)
        # 删除本地临时文件
        file_operate.delete_file(file_path)
        return response_dict(0, "上传成功", data=response)
    except Exception as e:
        return response_dict(3, f"上传文件时出现错误: {str(e)}", None)

# 获取历史对话列表
def get_chat_history(request):
    if request.method != "GET":
        return response_dict(2, "请求方式错误，此接口仅支持GET请求", None)
    required_params = ['offset', 'limit']
    if not validate_required_params(request.GET, required_params):
        return response_dict(1, f"缺少必要参数，需要参数: {', '.join(required_params)}", None)
    
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')
    
    try:
        response = kimi.get_chat_history(offset, limit)
        return response_dict(data=response, message='获取历史对话成功')
    except Exception as e:
        return response_dict(3, f"获取历史对话时出现错误: {str(e)}", None)

# 获取对话内容详情
def get_chat_content(request):
    if request.method != "GET":
        return response_dict(2, "请求方式错误，此接口仅支持GET请求", None)
    required_params = ['chat_id',  'limit']
    if not validate_required_params(request.GET, required_params):
        return response_dict(1, f"缺少必要参数，需要参数: {', '.join(required_params)}", None)
    
    chat_id = request.GET.get('chat_id')
    limit = request.GET.get('limit')
    
    try:
        response = kimi.get_chat_content(chat_id, limit)
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
        response = kimi.delete_chat(chat_id)
        return response_dict(data=response, message='删除对话成功')
    except Exception as e:
        return response_dict(3, f"删除对话时出现错误: {str(e)}", None)