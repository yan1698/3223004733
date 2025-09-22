import os
import sys
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from file_handler import read_file, write_result
from similarity_calculator import SimilarityCalculator
from text_processor import TextProcessor


class TestPaperCheckSystem(unittest.TestCase):

    def setUp(self):
        self.processor = TextProcessor()
        self.calculator = SimilarityCalculator()

    def test_file_reading_existing_file(self):
        """测试读取存在的文件"""
        content = read_file("orig.txt")
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)
        print("原文内容长度:", len(content))

    def test_file_reading_nonexistent_file(self):
        """测试读取不存在的文件"""
        with self.assertRaises(Exception):
            read_file("nonexistent_file.txt")

    def test_file_writing(self):
        """测试文件写入功能"""
        # 创建临时文件测试写入
        test_file = "test_output.txt"
        write_result(test_file, 0.85)

        # 验证写入内容
        content = read_file(test_file)
        self.assertEqual(content, "0.85")

        # 清理临时文件
        if os.path.exists(test_file):
            os.remove(test_file)

    def test_text_processing_original(self):
        """测试原文文本处理"""
        content = read_file("orig.txt")
        processed = self.processor.process(content)
        self.assertIsInstance(processed, list)
        self.assertGreater(len(processed), 0)
        print("原文处理后词语数量:", len(processed))

    def test_text_processing_variant_files(self):
        """测试所有变体文件的文本处理"""
        variant_files = [
            "orig_0.8_add.txt",
            "orig_0.8_del.txt",
            "orig_0.8_dis_1.txt",
            "orig_0.8_dis_10.txt",
            "orig_0.8_dis_15.txt",
        ]

        for file in variant_files:
            with self.subTest(file=file):
                content = read_file(file)
                processed = self.processor.process(content)
                self.assertIsInstance(processed, list)
                self.assertGreater(len(processed), 0)
                print(f"{file} 处理后词语数量:", len(processed))

    def test_similarity_with_original(self):
        """测试原文与自身的相似度"""
        orig_content = read_file("orig.txt")
        orig_processed = self.processor.process(orig_content)

        similarity = self.calculator.calculate_similarity(
            orig_processed, orig_processed
        )
        self.assertAlmostEqual(similarity, 1.0, places=2)
        print("原文与自身相似度:", similarity)

    def test_similarity_with_variants(self):
        """测试原文与各变体的相似度"""
        orig_content = read_file("orig.txt")
        orig_processed = self.processor.process(orig_content)

        variant_files = [
            ("orig_0.8_add.txt", "添加文本的变体"),
            ("orig_0.8_del.txt", "删除文本的变体"),
            ("orig_0.8_dis_1.txt", "dis1变体"),
            ("orig_0.8_dis_10.txt", "dis10变体"),
            ("orig_0.8_dis_15.txt", "dis15变体"),
        ]

        for file, description in variant_files:
            with self.subTest(file=file):
                variant_content = read_file(file)
                variant_processed = self.processor.process(variant_content)

                similarity = self.calculator.calculate_similarity(
                    orig_processed, variant_processed
                )

                # 相似度应该在0-1之间
                self.assertGreaterEqual(similarity, 0)
                self.assertLessEqual(similarity, 1)

                print(f"原文与{description}相似度: {similarity:.4f}")

    def test_all_file_accessibility(self):
        """测试所有文件都可访问"""
        files_to_test = [
            "orig.txt",
            "orig_0.8_add.txt",
            "orig_0.8_del.txt",
            "orig_0.8_dis_1.txt",
            "orig_0.8_dis_10.txt",
            "orig_0.8_dis_15.txt",
        ]

        for file in files_to_test:
            with self.subTest(file=file):
                # 测试文件是否存在且可读
                self.assertTrue(os.path.exists(file), f"文件 {file} 不存在")
                content = read_file(file)
                self.assertIsInstance(content, str)
                self.assertGreater(len(content), 0)
                print(f"{file} 可正常访问，内容长度: {len(content)}")


if __name__ == "__main__":
    unittest.main()
