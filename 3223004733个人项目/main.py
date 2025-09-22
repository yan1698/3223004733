"""
论文查重系统主程序模块

该模块提供命令行界面，用于计算两篇论文的相似度。
支持多种文件格式，使用余弦相似度算法进行文本比对。
"""

import argparse
import sys
from file_handler import FileHandler
from similarity_calculator import SimilarityCalculator
from text_processor import TextProcessor


def setup_argument_parser():
    """设置和配置命令行参数解析器"""
    parser = argparse.ArgumentParser(description='论文查重系统')
    parser.add_argument('original_file', help='原始论文文件路径')
    parser.add_argument('comparison_file', help='待比较论文文件路径')
    parser.add_argument('output_file', help='结果输出文件路径')
    return parser


def calculate_similarity(original_path, comparison_path, output_path):
    """
    计算两篇论文的相似度并保存结果
    
    Args:
        original_path (str): 原始论文文件路径
        comparison_path (str): 待比较论文文件路径
        output_path (str): 结果输出文件路径
    
    Returns:
        float: 相似度百分比
    """
    try:
        # 读取文件内容
        file_handler = FileHandler()
        original_text = file_handler.read_file(original_path)
        comparison_text = file_handler.read_file(comparison_path)
        
        # 文本处理
        text_processor = TextProcessor()
        processed_original = text_processor.process(original_text)
        processed_comparison = text_processor.process(comparison_text)
        
        # 计算相似度
        calculator = SimilarityCalculator()
        similarity = calculator.calculate_cosine_similarity(
            processed_original, processed_comparison
        )
        
        # 保存结果
        result_text = f"相似度: {similarity:.2%}"
        file_handler.write_file(output_path, result_text)
        
        print(f"查重完成！相似度: {similarity:.2%}")
        return similarity
        
    except FileNotFoundError as e:
        print(f"错误：文件未找到 - {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"错误：文件权限不足 - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误：处理过程中发生未知错误 - {e}")
        sys.exit(1)


def main():
    """主函数，程序入口点"""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    calculate_similarity(args.original_file, args.comparison_file, args.output_file)


if __name__ == "__main__":
    main()