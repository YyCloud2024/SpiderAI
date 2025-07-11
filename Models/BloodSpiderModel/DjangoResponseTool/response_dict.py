from django.http import JsonResponse


def response_dict(code : int = 0, message : str = "", data : dict = None):
    return JsonResponse({
        "code": code,
        "message": message,
        "data": data,
    })

