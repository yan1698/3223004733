import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class SimilarityCalculator:
    def __init__(self):
        # 初始化停用词
        self.stop_words = self._load_stop_words()
        # 设置TF-IDF参数
        self.vectorizer = TfidfVectorizer(
            tokenizer=jieba.cut,
            ngram_range=(1, 2),  # 使用unigram和bigram
            min_df=1,
            max_df=0.8,
            max_features=1000
        )
    
    def _load_stop_words(self):
        """加载停用词表"""
        # 基础中文停用词
        base_stop_words = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
            '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
            '自己', '这个', '那', '他', '她', '它', '我们', '他们', '这', '那', '就', '也',
            '还', '又', '都', '很', '让', '给', '把', '被', '吗', '呢', '啊', '呀', '哦'
        }
        return base_stop_words
    
    def calculate_cosine_similarity(self, text1, text2):
        """
        计算两篇文本的余弦相似度（改进版）
        """
        # 处理空文本的边界情况
        if not text1 and not text2:
            return 1.0
        elif not text1 or not text2:
            return 0.0
        
        # 预处理文本
        processed_text1 = self._preprocess_text(text1)
        processed_text2 = self._preprocess_text(text2)
        
        # 如果预处理后文本过短，使用Jaccard相似度
        if len(processed_text1) < 3 or len(processed_text2) < 3:
            return self.calculate_jaccard_similarity(text1, text2)
        
        try:
            # 使用TF-IDF向量化文本
            tfidf_matrix = self.vectorizer.fit_transform([processed_text1, processed_text2])
            
            # 检查特征数量
            if tfidf_matrix.shape[1] == 0:
                return self.calculate_jaccard_similarity(text1, text2)
            
            # 计算余弦相似度
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            result = float(similarity[0][0])
            
            # 对高相似度结果进行修正（防止乱序文本得分过高）
            if result > 0.95:
                # 结合编辑距离进行修正
                edit_sim = self._calculate_edit_similarity(text1, text2)
                # 如果编辑距离相似度较低，说明文本结构差异大，降低最终得分
                if edit_sim < 0.8:
                    result = result * 0.7 + edit_sim * 0.3
            
            return round(result, 4)
            
        except Exception as e:
            print(f"余弦相似度计算错误: {e}, 使用备用方法")
            return self.calculate_jaccard_similarity(text1, text2)
    
    def _preprocess_text(self, text):
        """文本预处理"""
        if not text:
            return ""
        
        # 1. 去除特殊字符和标点，但保留句子结构信息
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        
        # 2. 分词并过滤停用词
        words = jieba.cut(text)
        filtered_words = [word for word in words if word.strip() and word not in self.stop_words and len(word) > 1]
        
        # 3. 重新组合成文本（保留词序信息）
        return ' '.join(filtered_words)
    
    def _calculate_edit_similarity(self, text1, text2):
        """计算基于编辑距离的相似度（考虑文本结构）"""
        if not text1 and not text2:
            return 1.0
        elif not text1 or not text2:
            return 0.0
        
        # 简单的编辑距离计算（可以使用python-Levenshtein库更精确）
        def simple_edit_distance(s1, s2):
            if len(s1) < len(s2):
                return simple_edit_distance(s2, s1)
            if len(s2) == 0:
                return len(s1)
            
            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            
            return previous_row[-1]
        
        distance = simple_edit_distance(text1, text2)
        max_len = max(len(text1), len(text2))
        return 1.0 - distance / max_len if max_len > 0 else 0.0
    
    def calculate_comprehensive_similarity(self, text1, text2):
        """
        综合相似度计算（推荐使用）
        结合余弦相似度和编辑距离相似度
        """
        # 边界情况处理
        if not text1 and not text2:
            return 1.0
        elif not text1 or not text2:
            return 0.0
        
        # 1. 余弦相似度（词汇层面）
        cosine_sim = self.calculate_cosine_similarity(text1, text2)
        
        # 2. 编辑距离相似度（结构层面）
        edit_sim = self._calculate_edit_similarity(text1, text2)
        
        # 3. 句子长度相似度
        len_sim = 1 - abs(len(text1) - len(text2)) / max(len(text1), len(text2)) if max(len(text1), len(text2)) > 0 else 0
        
        # 加权综合
        # 对于乱序文本，编辑距离相似度更重要
        final_similarity = 0.4 * cosine_sim + 0.5 * edit_sim + 0.1 * len_sim
        
        return round(final_similarity, 4)
    
    def calculate_jaccard_similarity(self, text1, text2):
        """
        计算Jaccard相似度（考虑词序的改进版）
        """
        # 处理空文本边界情况
        if not text1 and not text2:
            return 1.0
        elif not text1 or not text2:
            return 0.0
        
        # 使用bigram来捕获词序信息
        def get_ngrams(text, n=2):
            words = list(jieba.cut(text))
            words = [w for w in words if w.strip() and w not in self.stop_words]
            return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
        
        ngrams1 = set(get_ngrams(text1))
        ngrams2 = set(get_ngrams(text2))
        
        if not ngrams1 and not ngrams2:
            return 1.0
        elif not ngrams1 or not ngrams2:
            return 0.0
        
        intersection = len(ngrams1.intersection(ngrams2))
        union = len(ngrams1.union(ngrams2))
        
        return intersection / union if union > 0 else 0.0