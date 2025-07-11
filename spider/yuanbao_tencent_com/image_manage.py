import requests
import json


class ImageManage:
    def __init__(self, YuanBao):
        self.yuanbao = YuanBao

    # 图片风格转换
    def image_style_conversion(self, img_path, style:str):
        data = {"imageUrl": img_path, "prompt": f"转换为{style}风格", "style": style + "风格", "agentId": ""}
        data = json.dumps(data)
        response = requests.post(f'{self.yuanbao.domain}/api/image/style', cookies=self.yuanbao.cookies, headers=self.yuanbao.headers,
                                 data=data, stream=True)
        return response

    # 图片去除水印
    def image_remove_watermark(self, img_path):
        data = '{"imageUrl":"' + img_path + '","agentId":""}'
        response = requests.post(f'{self.yuanbao.domain}/api/image/removewatermark', cookies=self.yuanbao.cookies, headers=self.yuanbao.headers,
                                 data=data, stream=True)
        return response

    # 图片变清晰
    def image_sharpen(self, img_path):
        data = '{"imageUrl":"' + img_path + '","agentId":""}'
        response = requests.post(f'{self.yuanbao.domain}/api/image/clarity', cookies=self.yuanbao.cookies, headers=self.yuanbao.headers,
                                 data=data, stream=True)
        return response

    # 生成图片
    def generate_images(self, prompt, chat_id, style=""):
        """
        生成图片
        :param prompt: 提示词
        :param style: 风格
        :param chat_id: 会话id
        """
        data = {
            "model": "gpt_175B_0404",
            "prompt": prompt + "风格是" + style,
            "plugin": "Adaptive",
            "displayPrompt": prompt + "风格是" + style,
            "displayPromptType": 1,
            "options": {
                "imageIntention": {
                    "needIntentionModel": True,
                    "backendUpdateFlag": 2,
                    "intentionStatus": True
                }
            },
            "multimedia": [],
            "agentId": self.yuanbao.yuanbao_id,
            "supportHint": 1,
            "extReportParams": None,
            "isAtomInput": False,
            "version": "v2",
            "chatModelId": "hunyuan_gpt_175B_0404",
            "applicationIdList": [],
            "supportFunctions": ["closeInternetSearch"]
        }
        data = json.dumps(data)
        response = requests.post(f'{self.yuanbao.domain}/api/chat/{chat_id}',
                                 cookies=self.yuanbao.cookies, headers=self.yuanbao.headers, data=data, stream=True)
        return response
        # return response

    # 获取生成图片的风格
    def get_style(self):
        json_data = {
            'agentId': self.yuanbao.GenerateImages_id,
        }

        response = requests.post(f'{self.yuanbao.domain}/api/user/agent/detail', cookies=self.yuanbao.cookies,
                                 headers=self.yuanbao.headers, json=json_data)
        return response.json()



if __name__ == '__main__':
    from main import YuanBao
    yuanbao= YuanBao()
    image_manage = ImageManage(yuanbao)
    print(image_manage.get_style())
