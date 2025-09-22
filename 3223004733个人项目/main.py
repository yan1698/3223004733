import sys
from file_handler import read_file, write_result
from text_processor import TextProcessor
from similarity_calculator import SimilarityCalculator

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py [original_file] [plagiarized_file] [output_file]")
        sys.exit(1)
    
    original_file = sys.argv[1]
    plagiarized_file = sys.argv[2]
    output_file = sys.argv[3]
    
    try:
        # 读取文件内容
        original_text = read_file(original_file)
        plagiarized_text = read_file(plagiarized_file)
        
        # 文本预处理
        processor = TextProcessor()
        original_processed = processor.process(original_text)
        plagiarized_processed = processor.process(plagiarized_text)
        
        # 计算相似度
        calculator = SimilarityCalculator()
        similarity = calculator.calculate_similarity(original_processed, plagiarized_processed)
        
        # 输出结果
        write_result(output_file, similarity)
        
        print(f"相似度计算完成: {similarity:.2f}")
        
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()