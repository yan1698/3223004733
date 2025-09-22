import jieba
import re

class TextProcessor:
    def __init__(self):
        # 停用词列表（实际应用中应该从文件加载更多停用词）
        self.stop_words = set(['的', '了', '在', '是', '我', '有', '和', '就', 
                              '不', '人', '都', '一', '一个', '上', '也', '很', 
                              '到', '说', '要', '去', '你', '会', '着', '没有', 
                              '看', '好', '自己', '这'])
    
    def process(self, text):
        """
        文本预处理流程
        """
        # 清洗文本
        cleaned_text = self.clean_text(text)
        # 分词
        words = self.segment_text(cleaned_text)
        # 去除停用词
        filtered_words = self.remove_stop_words(words)
        
        return filtered_words
    
    def clean_text(self, text):
        """
        清洗文本：去除标点符号、数字等无关字符
        """
        # 去除标点符号
        text = re.sub(r'[^\w\s]', '', text)
        # 去除数字
        text = re.sub(r'\d+', '', text)
        # 转换为小写
        text = text.lower()
        return text
    
    def segment_text(self, text):
        """
        使用结巴分词进行中文分词
        """
        return list(jieba.cut(text))
    
    def remove_stop_words(self, words):
        """
        去除停用词
        """
        return [word for word in words if word not in self.stop_words and len(word) > 1]