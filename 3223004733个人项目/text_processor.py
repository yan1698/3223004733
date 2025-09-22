# text_processor.py
import jieba
import re  # 添加这行导入语句

class TextProcessor:
    def __init__(self):
        pass
    
    def process(self, text):
        """
        处理文本，返回分词后的字符串
        
        Args:
            text (str): 输入文本
            
        Returns:
            str: 分词后的字符串，词语用空格分隔
        """
        if not text or not isinstance(text, str):
            return ""
        
        # 清洗文本：去除标点符号和特殊字符
        text = re.sub(r'[^\w\s]', '', text)
        
        # 使用jieba分词
        words = jieba.cut(text)
        
        # 过滤空字符串和空格
        words = [word.strip() for word in words if word.strip()]
        
        # 将词语列表拼接成字符串
        return ' '.join(words)