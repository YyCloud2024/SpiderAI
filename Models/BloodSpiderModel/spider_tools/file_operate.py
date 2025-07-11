# 文件操作
import json
import os
import datetime
import uuid

class FileOperate:
    def __init__(self) -> None:
        pass

    # 获取文件名 | 扩展名
    def get_file_name(self, file_path: str, extension: bool = False):
        if extension:
            # 获取文件扩展名
            return os.path.splitext(file_path)[1]
        else:
            # 获取文件名
            return os.path.basename(file_path).split(".")[0]

    # 获取路径下有多少个文件夹 | 文件 | 指定类型的文件
    def get_path_contents(self, path: str, file_type: str = None, exclude_names: list = None, folders_only: bool = False) -> list:
        """
        获取路径下的所有文件夹和文件
        :param path: 目标路径
        :param file_type: 可选，指定文件扩展名(如'.txt')
        :param exclude_names: 可选，要排除的文件名或文件夹名列表
        :param folders_only: 可选，是否只返回文件夹，默认为False
        :return: 包含所有绝对路径的列表
        """
        if not os.path.exists(path):
            return []
        
        # 初始化排除列表
        if exclude_names is None:
            exclude_names = []
            
        contents = []
        for item in os.listdir(path):
            # 检查是否在排除列表中
            if item in exclude_names:
                continue
                
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                # 如果只查找文件夹，或者不指定文件类型时包含文件夹
                if folders_only or file_type is None:
                    contents.append(full_path)
            elif not folders_only and (file_type is None or item.endswith(file_type)):
                # 只有在不查找文件夹时才添加文件
                contents.append(full_path)
        
        return contents

    # 在指定路径下创建文件夹并且返回当前绝对路径
    def create_directory(self, path: str) -> str:
        """
        在指定路径下创建文件夹并返回绝对路径
        :param path: 要创建的文件夹路径
        :return: 创建成功的文件夹绝对路径
        :raises FileExistsError: 如果文件夹已存在且自动重命名失败
        :raises PermissionError: 如果没有创建权限
        """
        try:
            os.makedirs(path, exist_ok=False)
            return os.path.abspath(path)
        except FileExistsError:
            # 生成时间戳后缀 (精确到微秒)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            # 分割路径和文件名
            dir_name, base_name = os.path.split(path)
            # 创建新的文件夹名称
            new_base_name = f"{base_name}_{timestamp}"
            new_path = os.path.join(dir_name, new_base_name)
            # 递归创建新文件夹
            return self.create_directory(new_path)
        except PermissionError:
            raise PermissionError(f"没有权限创建文件夹 '{path}'")
        except Exception as e:
            raise RuntimeError(f"创建文件夹失败: {str(e)}")

    # 读取文件并read返回文件内容
    def read_file(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    # 保存文件到本地并且返回文件路径
    def save_file(self, file, path_dir:str):
        # 文件夹
        file_dir = path_dir
        # 如果文件夹不存在，则创建文件夹
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # 如果路径下有文件，则new文件名
        file_name = uuid.uuid4().hex + "." + file.name.split(".")[-1]
        while os.path.exists(os.path.join(file_dir, file_name)):
            file_name = f"{uuid.uuid4()}.{file.name.split('.')[-1]}"
        file_path = os.path.join(file_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(file.read())
        return file_path

    # 删除本地文件
    def delete_file(self, path: str):
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
    
    
if __name__ == "__main__":
    file_operate = FileOperate()
    print(file_operate.get_file_name(r"X:\BloodSpider\Script\TemplateMax\projects\星影汇/首页.html"))