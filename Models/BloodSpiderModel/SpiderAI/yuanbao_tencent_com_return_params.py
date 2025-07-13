# 统一腾讯元宝构建返回参数
import json
class YuanBaoResponse:
    def __init__(self):
        pass

    # 文件上传返回参数
    def upload_file(self):
        """
        参考文档: https://cpn16feg6a.apifox.cn/320942255e0 -> 上传文件页
        """
        return {
        "error": {}, # 错误信息
        "isUploaded": False, # 是否上传成功. False 就是上传成功
        "bucketName": "",    # 存储桶名称
        "region": "ap-guangzhou",   # 存储桶区域
        "location": "", # 存储桶位置
        "encryptTmpSecretId": "",   # 临时密钥
        "encryptTmpSecretKey": "",   # 临时密钥
        "encryptToken": "",  # 临时密钥
        "startTime": 1752220610, # 临时密钥开始时间
        "expiredTime": 1752242210, # 临时密钥结束时间
        "resourceUrl": "", # 临时密钥访问地址
        "cosURL": "", # 临时密钥访问地址
        "supportAccelerate": True, # 是否支持加速
        "accelerateDomain": "", # 加速域名
        "eoSupportAccelerate": False, # 是否支持加速
        "eoAccelerateDomain": "", # 加速域名
        "resourceID": "" # 临时密钥对应的资源ID
    }

    # 创建对话id
    def create_chat_id(self, chat_id):
        return {
            "chat_id": chat_id
        }

    # 对话
    def chat_message(self, chat_content, chat_type):
        """
        chat_content: 回复的返回内容
        chat_type: 回复类型
        """
        chat_dict = {
            "chat_type": chat_type,
            "chat_content": chat_content,
        }
        return f"data: {json.dumps(chat_dict, ensure_ascii=False)} \n\n"

    # 获取历史对话
    def get_chat_history(self, limit, offset, total):
        """
        conversations
            {id:str,title:str}
        """
        response_dict = {
            "conversations": [],
            "pagination": {
                "limit": limit,
                "offset": offset,
                "totalResults": total
            }
        }
        return response_dict

    # 删除对话
    def delete_chat(self):
        return "{}"

    # 获取对话内容
    def get_chat_content(self):
        """
        convs
            id:str ID
            speaker: str 是谁在回复 ai、user

            content[dict]: 回复的内容
                msg 回复的内容
                type 默认text


        """
        response_dict = {
            "convs": []
        }
        return response_dict