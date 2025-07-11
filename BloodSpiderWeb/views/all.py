from django.shortcuts import render
from BloodSpiderModel.spider_tools.file_operate import FileOperate

file_operate = FileOperate()
# 全部线路
link_list = [file_operate.get_file_name(item) for item in
             file_operate.get_path_contents("BloodSpiderAPI/api", exclude_names=["__pycache__"], folders_only=True)]
config_result = {
    "link_list": link_list
}


# 首页
def index(request):
    result = {**config_result}
    return render(request, "pc/index.html", result)

# 大模型首页
def big_model_index(request, link_name):
    result = {
        **config_result,
        "link_name": link_name
    }
    return render(request, "pc/页面/大模型首页.html", result)
