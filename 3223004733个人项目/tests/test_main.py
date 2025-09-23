import os
import sys
import unittest

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from file_handler import read_file, write_result
from similarity_calculator import SimilarityCalculator
from text_processor import TextProcessor


class TestPaperCheckSystem(unittest.TestCase):

    def setUp(self):
        self.processor = TextProcessor()
        self.calculator = SimilarityCalculator()
        # 设置正确的文件路径（相对于项目根目录）
        self.project_root = project_root

    def get_file_path(self, filename):
        """获取文件在项目根目录的完整路径"""
        return os.path.join(self.project_root, filename)

    def test_file_reading_existing_file(self):
        """测试读取存在的文件"""
        file_path = self.get_file_path("orig.txt")
        if not os.path.exists(file_path):
            self.skipTest("orig.txt 文件不存在")
            
        content = read_file(file_path)
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)
        print("原文内容长度:", len(content))

    def test_file_reading_nonexistent_file(self):
        """测试读取不存在的文件"""
        with self.assertRaises(FileNotFoundError):
            read_file(self.get_file_path("nonexistent_file.txt"))

    def test_file_writing(self):
        """测试文件写入功能"""
        # 创建临时文件测试写入
        test_file = self.get_file_path("test_output.txt")
        write_result(test_file, 0.85)

        # 验证写入内容
        content = read_file(test_file)
        self.assertEqual(content.strip(), "0.8500")

        # 清理临时文件
        if os.path.exists(test_file):
            os.remove(test_file)

    def test_text_processing_original(self):
        """测试原文文本处理"""
        file_path = self.get_file_path("orig.txt")
        if not os.path.exists(file_path):
            self.skipTest("orig.txt 文件不存在")
            
        content = read_file(file_path)
        
        # 使用process方法处理文本
        processed = self.processor.process(content)
        # 修正：process方法返回的是字符串，不是列表
        self.assertIsInstance(processed, str)
        self.assertGreater(len(processed), 0)
        print("原文处理后长度:", len(processed))

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
                file_path = self.get_file_path(file)
                if not os.path.exists(file_path):
                    self.skipTest(f"文件 {file} 不存在")
                    
                content = read_file(file_path)
                processed = self.processor.process(content)
                # 修正：process方法返回的是字符串，不是列表
                self.assertIsInstance(processed, str)
                self.assertGreater(len(processed), 0)
                print(f"{file} 处理后长度:", len(processed))

    def test_similarity_calculation_methods(self):
        """测试相似度计算方法"""
        text1 = "这是一个测试文本"
        text2 = "这是另一个测试文本"
        
        # 使用正确的方法名 calculate_cosine_similarity
        similarity = self.calculator.calculate_cosine_similarity(text1, text2)
        self.assertIsInstance(similarity, (int, float))
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
        print(f"相似度计算成功: {similarity:.4f}")

    def test_similarity_edge_cases(self):
        """测试边界情况"""
        # 测试空文本
        empty_similarity = self.calculator.calculate_cosine_similarity("", "")
        self.assertEqual(empty_similarity, 1.0)
        
        # 测试完全不同文本
        text1 = "这是第一个文本"
        text2 = "这是完全不同的第二个文本"
        similarity = self.calculator.calculate_cosine_similarity(text1, text2)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
        
        print("边界情况测试通过")

    def test_similarity_with_original(self):
        """测试原文与自身的相似度"""
        file_path = self.get_file_path("orig.txt")
        if not os.path.exists(file_path):
            self.skipTest("orig.txt 文件不存在")
            
        orig_content = read_file(file_path)
        orig_processed = self.processor.process(orig_content)

        # process方法返回的是字符串，直接使用
        similarity = self.calculator.calculate_cosine_similarity(orig_processed, orig_processed)
        self.assertAlmostEqual(similarity, 1.0, places=2)
        print("原文与自身相似度:", similarity)

    def test_similarity_with_variants(self):
        """测试原文与各变体的相似度"""
        orig_file_path = self.get_file_path("orig.txt")
        if not os.path.exists(orig_file_path):
            self.skipTest("orig.txt 文件不存在")
            
        orig_content = read_file(orig_file_path)
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
                file_path = self.get_file_path(file)
                if not os.path.exists(file_path):
                    self.skipTest(f"文件 {file} 不存在")
                    
                variant_content = read_file(file_path)
                variant_processed = self.processor.process(variant_content)

                similarity = self.calculator.calculate_cosine_similarity(
                    orig_processed, variant_processed
                )

                # 相似度应该在0-1之间
                self.assertGreaterEqual(similarity, 0)
                self.assertLessEqual(similarity, 1)

                print(f"原文与{description}相似度: {similarity:.4f}")

    def test_all_file_accessibility(self):
        """测试所有文件都可访问"""
        files_to_test = [
            "orig.txt", "orig_0.8_add.txt", "orig_0.8_del.txt",
            "orig_0.8_dis_1.txt", "orig_0.8_dis_10.txt", "orig_0.8_dis_15.txt"
        ]

        for file in files_to_test:
            with self.subTest(file=file):
                file_path = self.get_file_path(file)
                # 测试文件是否存在且可读
                self.assertTrue(os.path.exists(file_path), f"文件 {file} 不存在")
                content = read_file(file_path)
                self.assertIsInstance(content, str)
                self.assertGreater(len(content), 0)
                print(f"✓ {file} 可正常访问，内容长度: {len(content)}")

    def test_integration_pipeline(self):
        """测试完整流程集成"""
        print("=== 完整流程测试 ===")
        
        # 1. 读取原文
        orig_path = self.get_file_path("orig.txt")
        orig_content = read_file(orig_path)
        print("✓ 原文读取成功")
        
        # 2. 处理文本
        orig_processed = self.processor.process(orig_content)
        print("✓ 文本处理成功")
        
        # 3. 测试与变体文件的相似度
        test_files = ["orig_0.8_add.txt", "orig_0.8_del.txt", "orig_0.8_dis_1.txt"]
        
        for test_file in test_files:
            test_path = self.get_file_path(test_file)
            if os.path.exists(test_path):
                test_content = read_file(test_path)
                test_processed = self.processor.process(test_content)
                
                similarity = self.calculator.calculate_cosine_similarity(orig_processed, test_processed)
                
                self.assertGreaterEqual(similarity, 0.0)
                self.assertLessEqual(similarity, 1.0)
                print(f"✓ {test_file} 相似度: {similarity:.4f}")


if __name__ == "__main__":
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPaperCheckSystem)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果摘要
    print(f"\n{'='*50}")
    print("测试结果摘要:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    
    # 如果有失败或错误，显示详细信息
    if result.failures:
        print(f"\n失败详情:")
        for test, traceback in result.failures:
            print(f"{test}: {traceback}")
    
    if result.errors:
        print(f"\n错误详情:")
        for test, traceback in result.errors:
            print(f"{test}: {traceback}")