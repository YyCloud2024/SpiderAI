# 通用

class GeneralToolkit:
    def __init__(self) -> None:
        pass

    def check_common_substrings(self, input_string, substr_list):
        """
        检查字符串是否包含列表中的任何完整子字符串
        
        参数:
        input_string (str): 需要检查的字符串
        substr_list (list): 用于比较的子字符串列表
        
        返回:
        bool: 如果存在匹配的子字符串返回 True，否则返回 False
        """
        for substr in substr_list:
            if substr in input_string:
                return True
        return False

    def filter_sensitive_words(self, sensitive_words: list[str], text: str, replacement: str = '*') -> str:
        """
        将文本中的敏感词替换为指定字符串，每个敏感词仅替换一次
        
        参数:
            sensitive_words: 敏感词列表
            text: 需要过滤的文本
            replacement: 用于替换敏感词的字符串，默认为星号(*)
        
        返回:
            过滤后的文本
        """
        # 按长度降序排列敏感词，确保长词优先被替换
        sensitive_words = sorted(sensitive_words, key=len, reverse=True)
        
        filtered_text = text
        for word in sensitive_words:
            filtered_text = filtered_text.replace(word, replacement, 1)  # 仅替换一次
        
        return filtered_text