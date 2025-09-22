from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SimilarityCalculator:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
    
    def calculate_similarity(self, original_words, plagiarized_words):
        """
        计算两个文本的相似度
        """
        # 将分词结果转换为字符串
        original_text = ' '.join(original_words)
        plagiarized_text = ' '.join(plagiarized_words)
        
        # 创建TF-IDF向量
        tfidf_matrix = self.vectorizer.fit_transform([original_text, plagiarized_text])
        
        # 计算余弦相似度
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return similarity