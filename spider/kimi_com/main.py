import requests
import json
from BloodSpiderModel.SpiderAI.yuanbao_tencent_com_return_params import YuanBaoResponse

# 仅限Debug调试使用,不要在线上模式使用!!!
kimi_config = {
    'authorization': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTc1NDgzNjM1OCwiaWF0IjoxNzUyMjQ0MzU4LCJqdGkiOiJkMW9pMTFpaTU5NzAwZ3ZkYmw5ZyIsInR5cCI6ImFjY2VzcyIsImFwcF9pZCI6ImtpbWkiLCJzdWIiOiJjc2t0dnA3ZDBwODhndG5kZDZyMCIsInNwYWNlX2lkIjoiY3NrdHZwN2QwcDg4Z3RuZGQ2cWciLCJhYnN0cmFjdF91c2VyX2lkIjoiY3NrdHZwN2QwcDg4Z3RuZGQ2cTAiLCJyb2xlcyI6WyJmX212aXAiXSwic3NpZCI6IjE3MzEwODY0OTk5NjkwMjM3MDkiLCJkZXZpY2VfaWQiOiI3NTEwODU5Njc3MDQzODY0MDcxIiwicmVnaW9uIjoiY24ifQ.GWmFGzqYi1h6LUAqQuuRCZAWlW14rvhGLJmqN-5-TjQQxl9ydIf3qEvd6y3CLvkHHAmGVsYhoFod_g6c1U_0Zw',
}

class KiMi_JiChuBan:
    def __init__(self, kimi_config):
        self.kimi_config = kimi_config
        self.domain = "https://www.kimi.com/"
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'authorization': f'Bearer {self.kimi_config['authorization']}',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': self.domain,
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'r-timezone': 'Asia/Shanghai',
            'referer': self.domain,
            'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        }
        self.yuanbao_tencent_com_return_params = YuanBaoResponse()

    # 创建对话
    def create_chat(self):
        json_data = {
            'name': '未命名会话',
            'born_from': 'home',
            'kimiplus_id': 'kimi',
            'is_example': False,
            'source': 'web',
            'tags': [],
        }
        response = requests.post(self.domain + "api/chat", headers=self.headers, json=json_data).json()
        return self.yuanbao_tencent_com_return_params.create_chat_id(response['id'])

    # 发送消息
    def send_message(self,chat_id: str,message: str,use_search: bool = False,AI_model="kimi",refs=None):
        """
        chat_id: 对话ID
        message: 提问的文本
        AI_model:
        目前研究发现的值是
        kimi: 正常快捷模型
        k1.5-thinking: k1.5长链路快捷模型
        k2: kimi的新旗舰模型

        use_search: 是否开启联网模式,开启后会通过互联网检索资料
        refs: 引用上传的文件, 如果上传的是图片就是 file_id 如果上传的是文件,那么值就是id

        """
        if refs is None:
            refs = []
        json_data = {
            'kimiplus_id': 'kimi',
            'extend': {
                'sidebar': True,
            },
            'model': AI_model,
            'use_search': use_search,
            'messages': [
                {
                    'role': 'user',
                    'content': message,
                },
            ],
            'refs': refs,  # 引用图片、文件等
            'history': [],
            'scene_labels': [],
            'use_semantic_memory': False,
        }
        response = requests.post(
            f'{self.domain}/api/chat/{chat_id}/completion/stream',
            headers=self.headers,
            json=json_data,
            stream=True,
        )
        return response

    # 获取历史对话
    def get_chat_history(self, offset=0, limit=40):
        """
        参数说明:
        - offset: 偏移量，用于分页查询，默认为0,例如limit是1，那么此时offset就是0(0就是1)，如果想查询第二页，那么offset就是2。
        - limit: 每页的记录数，默认为40。
        """
        offset = int(offset)
        limit = int(limit)
        json_data = {
            'kimiplus_id': '',
            'offset': offset,
            'q': '',
            'size': limit,
            'with_last_segment': True,
        }

        response = requests.post(f'{self.domain}api/chat/list', headers=self.headers, json=json_data).json()
        # 按照腾讯元宝的返回数据结构进行转换
        response_dict = self.yuanbao_tencent_com_return_params.get_chat_history(
            limit=limit,
            offset=offset,
            total=response['total'],
        )
        for item in response['items']:
            id = item['id']
            title = item['name']
            response_dict["conversations"].append({
                "id": id,
                "title": title,
            })
        return response_dict

    # 获取对话内容

    def get_chat_content(self, chat_id, limit=60):
        limit = int(limit)
        json_data = {
            'last': limit,
        }

        response = requests.post(
            f'{self.domain}api/chat/{chat_id}/segment/scroll',
            headers=self.headers,
            json=json_data,
        ).json()
        # 按照腾讯元宝的返回数据结构进行转换
        response_dict = self.yuanbao_tencent_com_return_params.get_chat_content()
        for item in response['items']:
            speaker = None
            id = item['id']

            if item['role'] == 'user':
                speaker = "user"
            elif item['role'] == 'assistant':
                speaker = "ai"
            else:
                speaker = "ai"
            content = {
                "msg": item['content'],
                "type": "text",
            }
            response_dict["convs"].append({
                "id": id,
                "speaker": speaker,
                "content": content
            })

        return response_dict

    # 删除对话
    def delete_chat(self, chat_id):
        # 接口地址
        response = requests.delete(f'{self.domain}api/chat/{chat_id}',headers=self.headers).text
        return self.yuanbao_tencent_com_return_params.delete_chat()


    # 流式输出
    def handle_stream_response(self, response):

        """处理流式响应，生成SSE格式的数据"""
        for line in response.iter_lines(chunk_size=1024, decode_unicode=False):
            if not line:
                continue  # 跳过空行
            try:
                # 解码并解析JSON数据
                text = line.decode('utf-8').lstrip('data:').strip()
                if not text:
                    continue  # 跳过空的data行
                data = json.loads(text)

                # 验证数据结构
                if not isinstance(data, dict):
                    raise ValueError(f"无效的数据格式: {data}")

                event_type = data.get('event')

                if event_type == "cmpl":

                    # 处理普通回复
                    message = data.get('text', '')
                    chat_dict = {
                        "chat_type": "chat",
                        "chat_content": message,
                    }
                    print(chat_dict)
                elif event_type == "k1":

                    # 处理K1事件
                    message = data.get('text', '')
                    chat_dict = {
                        "chat_type": "chat",
                        "chat_content": message,
                    }
                    print(chat_dict)
                elif event_type == "all_done":
                    # 处理结束信号
                    print("对话结束")
                    chat_dict = {
                        "chat_type": "DONE",
                        "chat_content": message,
                    }
                    break  # 终止循环
                else:
                    # 未知事件类型
                    print(f"未知事件类型: {event_type}")
                    pass

            except UnicodeDecodeError as e:
                # 编码错误
                chat_dict = {
                    "chat_type": "error",
                    "chat_content": f"字符编码错误: {str(e)}",
                }
                print(chat_dict)
                break  # 严重错误，终止处理

            except Exception as e:
                # 其他错误
                chat_dict = {
                    "chat_type": "error",
                    "chat_content": f"处理响应时发生错误: {str(e)}",
                }
                print(chat_dict)

    # 流式输出
    def handle_stream_response_websocket(self, response):

        """处理流式响应，生成SSE格式的数据"""
        for line in response.iter_lines(chunk_size=1024, decode_unicode=False):
            if not line:
                continue  # 跳过空行
            try:
                # 解码并解析JSON数据
                text = line.decode('utf-8').lstrip('data:').strip()
                if not text:
                    continue  # 跳过空的data行
                data = json.loads(text)

                # 验证数据结构
                if not isinstance(data, dict):
                    raise ValueError(f"无效的数据格式: {data}")

                event_type = data.get('event')

                if event_type == "cmpl":
                    # 处理普通回复
                    yield self.yuanbao_tencent_com_return_params.chat_message(
                        data.get('text', ''),
                        "chat"
                    )
                elif event_type == "k1":
                    # 处理K1事件
                    yield self.yuanbao_tencent_com_return_params.chat_message(
                        data.get('text', ''),
                        "chat"
                    )
                elif event_type == "all_done":
                    # 处理结束信号
                    yield self.yuanbao_tencent_com_return_params.chat_message(
                        "",
                        "DONE"
                    )
                    break  # 终止循环
                else:
                    # 未知事件类型
                    print(f"未知事件类型: {event_type}")
                    pass

            except UnicodeDecodeError as e:
                # 编码错误
                yield self.yuanbao_tencent_com_return_params.chat_message(
                    f"字符编码错误: {str(e)}",
                    "error"
                )
                break  # 严重错误，终止处理

            except Exception as e:
                # 其他错误
                yield self.yuanbao_tencent_com_return_params.chat_message(
                    f"处理响应时发生错误: {str(e)}",
                    "error"
                )


if __name__ == "__main__":
    kimiban = KiMi_JiChuBan(kimi_config)
    a = kimiban.get_chat_history(0, 2)
    print(a)
