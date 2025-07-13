# 基础版, 提供基础的对话能力
import requests
import json
from BloodSpiderModel.SpiderAI.yuanbao_tencent_com_return_params import YuanBaoResponse

class YuanBao:
    def __init__(self, yuanbao_config):
        # 元宝配置
        self.yuanbao_config = yuanbao_config
        # 唯一ID
        self.yuanbao_id = self.yuanbao_config['yuanbao_id']
        # 生成图片ID
        self.GenerateImages_id = self.yuanbao_config['GenerateImages_id']
        # 用户id
        self.hy_user = self.yuanbao_config['hy_user']
        # 密钥
        self.hy_token = self.yuanbao_config['hy_token']
        # 基础url
        self.domain = "https://yuanbao.tencent.com"
        # 基础headers
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'origin': self.domain,
            'priority': 'u=1, i',
            'referer': f'{self.domain}/chat/{self.yuanbao_id}',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            't-userid': self.hy_user,
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/135.0.0.0',
            'x-agentid': self.yuanbao_id,
            'x-id': self.hy_user,
            'x-instance-id': '5',
            'x-language': 'zh-CN',
            'x-os_version': 'iOS(13.2.3)-WebKit',
            'x-platform': 'ios',
            'x-requested-with': 'XMLHttpRequest',
            'x-source': 'web',
        }
        # 基础cookie
        self.cookies = {
            'hy_source': 'web',
            'hy_user': self.hy_user,
            'hy_token': self.hy_token,
        }
        self.yuanbao_tencent_com_return_params = YuanBaoResponse()

    # 创建对话
    def create_chat(self):
        # 接口地址
        chat_api = self.domain + "/api/user/agent/conversation/create"
        # 请求参数
        json_data = {
            'agentId': self.yuanbao_id,
        }

        response = requests.post(chat_api, headers=self.headers, json=json_data, cookies=self.cookies).json()
        return self.yuanbao_tencent_com_return_params.create_chat_id(response['id'])

    # 发送消息
    def send_message(self, message, chat_id, yuanbao_model="hunyuan_gpt_175B_0404", multimedia=[]):
        """
        yuanbao_model模型说明:
        - hunyuan_gpt_175B_0404: 腾讯元宝的基础模型，提供基础的对话能力。
        - hunyuan_t1: 腾讯元宝的T1模型，提供深度思考的回答。
        - deep_seek_v3: 腾讯元宝接入的deep_seel模型V3版本。
        - deep_seek: 腾讯元宝接入的deep_seel模型R1版本,拥有深度思考功能。

        multimedia参数说明:
        {
            "type": "txt",  # 类型,文本是txt,图片是image
            "docType": 和type一样
            "url": 文件url,
            "fileName": 文件名称,
            "size":111 文件大小,
            "width": 0图片专属,
            "height": 0图片专属
        }
        """
        # 接口地址
        send_api = self.domain + f"/api/chat/{chat_id}"
        # 请求参数
        data = {
            "model": "gpt_175B_0404",
            "prompt": message,
            "plugin": "Adaptive",
            "displayPrompt": message,
            "displayPromptType": 1,
            "options": {
                "imageIntention": {
                    "needIntentionModel": True,
                    "backendUpdateFlag": 2,
                    "intentionStatus": True
                }
            },
            "multimedia": multimedia,
            "agentId": self.yuanbao_id,
            "supportHint": 1,
            "version": "v2",
            "chatModelId": yuanbao_model
        }
        data = json.dumps(data)
        response = requests.post(send_api, cookies=self.cookies, headers=self.headers, data=data, stream=True)
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
        # 接口地址
        history_api = self.domain + '/api/user/agent/conversation/list'
        json_data = {
            'agentId': self.yuanbao_id,
            'offset': offset,
            'limit': limit,
            'filterGoodQuestion': True,
        }
        response = requests.post(history_api, cookies=self.cookies, headers=self.headers, json=json_data).json()
        response_dict = self.yuanbao_tencent_com_return_params.get_chat_history(
            limit=limit,
            offset=offset,
            total=response['pagination']['totalResults']
        )
        for item in response['conversations']:
            response_dict["conversations"].append({
                "id": item['id'],
                "title": item['title']
            })
        return response_dict

    # 获取对话内容
    def get_chat_content(self, chat_id, offset=0, limit=60):
        offset = int(offset)
        limit = int(limit)
        # 接口地址
        json_data = {
            'conversationId': chat_id,
            'offset': offset,
            'limit': limit,
        }
        response = requests.post(f'{self.domain}/api/user/agent/conversation/v1/detail', cookies=self.cookies,
                                 headers=self.headers, json=json_data).json()
        response_dict = self.yuanbao_tencent_com_return_params.get_chat_content()
        for item in response['convs']:
            response_dict["convs"].append({
                "id": item["id"],
                "speaker": item["speaker"],
                "content": {
                    "msg": item['speechesV2'][0]['content'][0]['msg'],
                    "type": "text"
                }
            })
        return response_dict

    # 删除对话
    def delete_chat(self, chat_id):
        # 接口地址
        json_data = {
            'conversationIds': [
                chat_id,
            ],
            'uiOptions': {},
        }

        response = requests.post(f'{self.domain}/api/user/agent/conversation/v1/clear', cookies=self.cookies,
                                 headers=self.headers, json=json_data)
        return self.yuanbao_tencent_com_return_params.delete_chat()

    # 处理流式响应: 控制台方法
    def handle_stream_response(self, response):
        for line in response.iter_lines():
            if line:
                try:
                    text = line.decode('utf-8')

                    if text.startswith('data: '):
                        text = text.replace('data: ', '')
                        # print("原始数据: " + text)
                        if text == "[DONE]":
                            # 制作字典
                            chat_dict = {
                                "chat_type": "DONE",
                                "chat_content": "",
                            }
                            print(chat_dict)
                            break
                        text = json.loads(text)
                        if text['type'] == "text":
                            # 普通对话
                            if text.get("msg") is not None:
                                # 制作字典
                                chat_dict = {
                                    "chat_type": "chat",
                                    "chat_content": text["msg"],
                                }
                                print(chat_dict)
                        elif text['type'] == "think":
                            # 思考中
                            # 制作字典
                            chat_dict = {
                                "chat_type": "think",
                                "chat_content": text["content"],
                            }
                            print(chat_dict)
                        elif text['type'] == "progress":
                            # 进度
                            # 制作字典
                            chat_dict = {
                                "chat_type": "progress",
                                "chat_content": str(text['value']),
                            }
                            print(chat_dict)
                        elif text['type'] == "image":
                            # 制作字典 图片
                            chat_dict = {
                                "chat_type": "image",
                                "chat_content": text['imageUrlLow'],
                            }
                            print(chat_dict)
                        elif text['type'] == "style":
                            # 制作字典 风格地址
                            chat_dict = {
                                "chat_type": "image",
                                "chat_content": text['thumbnailUrl'].replace(r'\u0026', '&'),
                            }
                            print(chat_dict)
                        elif text['type'] == "error":
                            # 制作字典 错误
                            chat_dict = {
                                "chat_type": "error",
                                "chat_content": text['msg'],
                            }
                            print(chat_dict)
                        elif text['type'] == "removewatermark":
                            # 制作字典 去除水印成品图
                            chat_dict = {
                                "chat_type": "image",
                                "chat_content": text['imageUrl'],
                            }
                            print(chat_dict)
                        elif text['type'] == "clarity":
                            # 制作字典 变清晰成品图
                            chat_dict = {
                                "chat_type": "image",
                                "chat_content": text['imageUrl'],
                            }
                            print(chat_dict)
                        elif text['type'] == "replace":
                            if text['replace']['multimedias'][0].get("url") is not None:
                                chat_dict = {
                                    "chat_type": "image",
                                    "chat_content": text['replace']['multimedias'],
                                }
                                print(chat_dict)
                        else:
                            continue
                except json.JSONDecodeError as e:
                    pass
                except KeyError as e:
                    pass

    # 处理流式响应: websocket方法
    def handle_stream_response_websocket(self, response):
        for line in response.iter_lines():
            if line:
                try:
                    text = line.decode('utf-8')
                    if text.startswith('data: '):
                        text = text.replace('data: ', '')
                        # print("原始数据: " + text)
                        if text == "[DONE]":
                            yield self.yuanbao_tencent_com_return_params.chat_message("", "DONE")
                            break
                        text = json.loads(text)
                        if text['type'] == "text":
                            # 普通对话
                            if text.get("msg") is not None:
                                # 制作字典
                                yield self.yuanbao_tencent_com_return_params.chat_message(text["msg"], "chat")
                        elif text['type'] == "think":
                            # 思考中
                            # 制作字典
                            yield self.yuanbao_tencent_com_return_params.chat_message(text["content"], "think")
                        elif text['type'] == "replace":
                            if text['replace']['multimedias'][0].get("url") is not None:
                                yield self.yuanbao_tencent_com_return_params.chat_message(text['replace']['multimedias'], "image")
                        elif text['type'] == "progress":
                            # 进度
                            # 制作字典
                            yield self.yuanbao_tencent_com_return_params.chat_message(str(text['value']), "progress")
                        elif text['type'] == "image":
                            # 制作字典 图片
                            yield self.yuanbao_tencent_com_return_params.chat_message(text['imageUrlLow'], "image")
                        elif text['type'] == "style":
                            # 制作字典 风格地址
                            yield self.yuanbao_tencent_com_return_params.chat_message(text['thumbnailUrl'].replace(r'\u0026', '&'), "image")
                        elif text['type'] == "error":
                            # 制作字典 错误
                            yield self.yuanbao_tencent_com_return_params.chat_message(text['msg'], "error")
                        elif text['type'] == "removewatermark":
                            # 制作字典 去除水印成品图
                            yield self.yuanbao_tencent_com_return_params.chat_message(text['imageUrl'], "image")
                        elif text['type'] == "clarity":
                            # 制作字典 变清晰成品图
                            yield self.yuanbao_tencent_com_return_params.chat_message(text['imageUrl'], "image")
                        else:
                            continue
                except json.JSONDecodeError as e:
                    pass
                except KeyError as e:
                    pass


if __name__ == '__main__':
    # 实例化
    yuanbao = YuanBao()
    print(yuanbao.get_chat_history())





