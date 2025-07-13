import requests
import json
from BloodSpiderModel.SpiderAI.yuanbao_tencent_com_return_params import YuanBaoResponse



class UploadTool:
    def __init__(self, kimi_confg):
        """
        kimi_config: kimi的配置
        """
        self.kimi_confg = kimi_confg
        self.yuanbao_tencent_com_return_params = YuanBaoResponse()

    # 上传图片到Kimi
    def upload_image(self, image_name, image_path):
        """
        上传图片到Kimi
        image_name: 图片名称
        image_path: 图片路径
        """
        json_data = {
            'name': image_name,
            'action': 'image',
        }

        response = requests.post(f'{self.kimi_confg.domain}/api/pre-sign-url', headers=self.kimi_confg.headers, json=json_data).json()
        image_data = None
        # 读取图片文件
        file_name = image_path  # 替换为你的图片文件路径
        with open(file_name, 'rb') as f:
            image_data = f.read()

        # 上传链接
        upload_url = response['url']
        # 文件名
        object_name = response['object_name']

        # file_id
        file_id = response['file_id']
        # 上传图片
        response = requests.put(upload_url, data=image_data)
        json_data = {
            'name': file_name,
            'object_name': object_name,
            'type': 'image',
            'file_id': file_id,
            'meta': {
                'width': '0',
                'height': '0',
            },
        }

        response = requests.post(f'{self.kimi_confg.domain}/api/file', headers=self.kimi_confg.headers, json=json_data).json()
        # 根据腾讯元宝的返回格式构建返回数据
        response_dict = self.yuanbao_tencent_com_return_params.upload_file()
        response_dict["resourceUrl"] = response["presigned_url"]
        return response_dict

    # 上传文件到Kimi
    def upload_File(self, image_name, image_path):
        json_data = {
            'name': image_name,
            'action': 'file',
        }

        response = requests.post(f'{self.kimi_confg.domain}/api/pre-sign-url', headers=self.kimi_confg.headers, json=json_data).json()
        image_data = None
        # 读取图片文件
        file_name = image_path  # 替换为你的图片文件路径
        with open(file_name, 'rb') as f:
            image_data = f.read()

        # 上传链接
        upload_url = response['url']
        # 文件名
        object_name = response['object_name']

        # file_id
        file_id = response['file_id']
        # 上传图片
        response = requests.put(upload_url, data=image_data)
        json_data = {
            'name': file_name,
            'object_name': object_name,
            'type': 'file',
            'file_id': file_id,
        }

        response = requests.post(f'{self.kimi_confg.domain}/api/file', headers=self.kimi_confg.headers, json=json_data).json()
        # 根据腾讯元宝的返回格式构建返回数据
        response_dict = self.yuanbao_tencent_com_return_params.upload_file()
        response_dict["resourceUrl"] = response["presigned_url"]
        return response_dict

if __name__ == '__main__':
    import main
    kimi = main.KiMi_JiChuBan(main.kimi_config)
    upload = UploadTool(kimi)
    print(upload.upload_File('config.json', 'config.json'))