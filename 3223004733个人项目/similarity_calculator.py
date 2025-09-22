"""
相似度计算模块

该模块使用TF-IDF和余弦相似度算法计算文本相似度。
基于scikit-learn库实现高效的向量化计算。
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityCalculator:
    """相似度计算器类，负责文本相似度的计算"""
    
    def calculate_cosine_similarity(self, text1, text2):
        """
        使用余弦相似度算法计算两个文本的相似度
        
        Args:
            text1 (str): 第一个文本
            text2 (str): 第二个文本
            
        Returns:
            float: 相似度得分，范围[0, 1]
        """
        if not text1 or not text2:
            return 0.0
            
        # 创建TF-IDF向量化器
        vectorizer = TfidfVectorizer()
        
        try:
            # 将文本转换为TF-IDF向量
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            
            # 计算余弦相似度
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            
            return similarity_matrix[0][0]
            
        except Exception as e:
            print(f"相似度计算错误: {e}")
            return 0.0