import requests
import hashlib
import hmac
import json
import os
from urllib.parse import quote
import xml.etree.ElementTree as ET


class UploadTool:
    """
    腾讯元宝文件上传工具类，封装了图片和文件上传功能
    """

    def __init__(self, YuanBao):
        """
        初始化上传工具
        :param YuanBao: YuanBao实例，包含域名、cookies和headers等信息
        """
        self._yuanbao = YuanBao

    def upload_image(self, img_path):
        """
        上传图片文件
        :param img_path: 图片文件路径
        :return: 上传结果字典，包含状态码、消息和数据
        """
        if not os.path.exists(img_path):
            return {"code": 404, "message": "图片不存在"}

        try:
            upload_info = self._get_upload_info(img_path, 'image')
            signature = self._generate_image_signature(upload_info, img_path)
            headers = self._build_image_headers(upload_info, signature)

            with open(img_path, 'rb') as f:
                response = requests.put(
                    f"https://{upload_info['bucketName']}.{upload_info['accelerateDomain']}/{upload_info['location']}",
                    headers=headers,
                    data=f.read()
                )

            return upload_info
        except Exception as e:
            return {
                "code": 500,
                "message": f"上传失败: {str(e)}"
            }

    def upload_file(self, file_path):
        """
        上传普通文件
        :param file_path: 文件路径
        :return: 上传结果字典，包含状态码、消息和数据
        """
        if not os.path.exists(file_path):
            return {"code": 404, "message": "文件不存在"}

        try:
            upload_info = self._get_upload_info(file_path, 'file')
            signature = self._generate_file_signature(upload_info, file_path)
            headers = self._build_file_headers(upload_info, signature, file_path)

            with open(file_path, 'rb') as f:
                response = requests.put(
                    f"https://{upload_info['bucketName']}.{upload_info['accelerateDomain']}{upload_info['location']}",
                    headers=headers,
                    data=f.read()
                )

            return upload_info
        except Exception as e:
            return {
                "code": 500,
                "message": f"服务器错误: {str(e)}"
            }

    def _get_upload_info(self, file_path, file_type):
        """
        获取上传所需的信息
        :param file_path: 文件路径
        :param file_type: 文件类型('image'或'file')
        :return: 上传信息字典
        """
        json_data = {
            'fileName': file_path,
            'docFrom': 'localDoc',
        }
        if file_type == 'file':
            json_data['docOpenId'] = ''

        response = requests.post(
            f'{self._yuanbao.domain}/api/resource/genUploadInfo',
            cookies=self._yuanbao.cookies,
            headers=self._yuanbao.headers,
            json=json_data
        )
        return response.json()

    def _generate_image_signature(self, upload_info, img_path):
        """
        生成图片上传的签名
        :param upload_info: 上传信息字典
        :param img_path: 图片路径
        :return: 签名字符串
        """
        times = f"{upload_info['startTime']};{upload_info['expiredTime']}"
        b = self._hmac_sha1(times, upload_info['encryptTmpSecretKey'])
        x = '\n'.join(['put', upload_info['location'], '', self._build_image_str(upload_info, img_path), ''])
        s = '\n'.join(["sha1", times, self._sha1_string(x), ""])
        return self._hmac_sha1(s, b)

    def _generate_file_signature(self, upload_info, file_path):
        """
        生成文件上传的签名
        :param upload_info: 上传信息字典
        :param file_path: 文件路径
        :return: 签名字符串
        """
        times = f"{upload_info['startTime']};{upload_info['expiredTime']}"
        b = self._hmac_sha1(times, upload_info['encryptTmpSecretKey'])
        s = "\n".join([
            "sha1",
            times,
            self._sha1_string("\n".join([
                'put',
                upload_info['location'],
                '',
                self._build_file_str(os.path.getsize(file_path), upload_info),
                ""
            ])),
            ""
        ])
        return self._hmac_sha1(s, b)

    def _build_image_headers(self, upload_info, signature):
        """
        构建图片上传的请求头
        :param upload_info: 上传信息字典
        :param signature: 签名字符串
        :return: 请求头字典
        """
        return {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Authorization': f'q-sign-algorithm=sha1&q-ak={upload_info["encryptTmpSecretId"]}&q-sign-time={upload_info["startTime"]};{upload_info["expiredTime"]}&q-key-time={upload_info["startTime"]};{upload_info["expiredTime"]}&q-header-list=content-length;host;pic-operations&q-url-param-list=&q-signature={signature}',
            'Connection': 'keep-alive',
            'Pic-Operations': json.dumps({
                "is_pic_info": 1,
                "rules": [{
                    "fileid": upload_info['location'],
                    "rule": "imageMogr2/format/jpg"
                }]
            }).replace(" ", ""),
            'Referer': self._yuanbao.domain,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-cos-security-token': upload_info['encryptToken'],
        }

    def _build_file_headers(self, upload_info, signature, file_path):
        """
        构建文件上传的请求头
        :param upload_info: 上传信息字典
        :param signature: 签名字符串
        :param file_path: 文件路径
        :return: 请求头字典
        """
        return {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Authorization': f'q-sign-algorithm=sha1&q-ak={upload_info["encryptTmpSecretId"]}&q-sign-time={upload_info["startTime"]};{upload_info["expiredTime"]}&q-key-time={upload_info["startTime"]};{upload_info["expiredTime"]}&q-header-list=content-length;host&q-url-param-list=&q-signature={signature}',
            'Connection': 'keep-alive',
            'Content-Length': str(os.path.getsize(file_path)),
            'Content-Type': 'application/octet-stream',
            'Referer': self._yuanbao.domain,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
            'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-cos-security-token': upload_info['encryptToken'],
        }

    def _build_image_str(self, upload_info, img_path):
        """
        构建图片上传的参数字符串
        :param upload_info: 上传信息字典
        :param img_path: 图片路径
        :return: 参数字符串
        """
        content_length = os.path.getsize(img_path)
        host = f"{upload_info['bucketName']}.{upload_info['accelerateDomain']}"
        pic_operations = json.dumps({
            "is_pic_info": 1,
            "rules": [{
                "fileid": upload_info['location'],
                "rule": "imageMogr2/format/jpg"
            }]
        }).replace(" ", "")

        return f"content-length={content_length}&host={host}&pic-operations={quote(pic_operations, encoding='utf-8', safe='')}"

    def _build_file_str(self, file_size, upload_info):
        """
        构建文件上传的参数字符串
        :param file_size: 文件大小
        :param upload_info: 上传信息字典
        :return: 参数字符串
        """
        host = f"{upload_info['bucketName']}.{upload_info['accelerateDomain']}"
        return f"content-length={file_size}&host={host}"

    def _hmac_sha1(self, value, key):
        """
        HMAC-SHA1加密
        :param value: 要加密的值
        :param key: 加密密钥
        :return: 加密后的十六进制字符串
        """
        if isinstance(value, str):
            value = value.encode('utf-8')
        if isinstance(key, str):
            key = key.encode('utf-8')
        return hmac.new(key, value, hashlib.sha1).hexdigest()

    def _sha1_string(self, x):
        """
        SHA1加密
        :param x: 要加密的字符串
        :return: 加密后的十六进制字符串
        """
        return hashlib.sha1(x.encode('utf-8')).hexdigest()

    def _xml_to_dict(self, element):
        """
        将XML元素转换为字典
        :param element: XML元素
        :return: 转换后的字典
        """
        result = {}
        for child in element:
            result[child.tag] = child.text if len(child) == 0 else self._xml_to_dict(child)
        return result


if __name__ == "__main__":
    # 示例用法
    from main import YuanBao

    yuanbao = YuanBao()
    upload_tool = UploadTool(yuanbao)

    # 上传图片
    print(upload_tool.upload_image("demo.jpg"))

    # 上传文件
    print(upload_tool.upload_file("main.py"))