"""
文件处理模块

该模块负责文件的读写操作，支持多种编码格式的自动检测和处理。
"""

import chardet


class FileHandler:
    """文件处理器类，负责文件的读取和写入操作"""
    
    def read_file(self, file_path):
        """
        读取文件内容并自动检测编码
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            str: 文件内容
            
        Raises:
            FileNotFoundError: 当文件不存在时
            UnicodeDecodeError: 当文件编码无法识别时
            IOError: 当文件读取失败时
        """
        try:
            # 检测文件编码
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                encoding = chardet.detect(raw_data)['encoding']
                
            # 使用检测到的编码读取文件
            with open(file_path, 'r', encoding=encoding or 'utf-8') as file:
                return file.read()
                
        except FileNotFoundError as e:
            raise FileNotFoundError(f"文件未找到: {file_path}") from e
        except UnicodeDecodeError as e:
            # 尝试使用其他常见编码
            for encoding in ['gbk', 'gb2312', 'utf-16']:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        return file.read()
                except UnicodeDecodeError:
                    continue
            raise UnicodeDecodeError(f"无法解码文件 {file_path}，尝试了多种编码") from e
        except IOError as e:
            raise IOError(f"文件读取错误: {file_path}") from e
    
    def write_file(self, file_path, content):
        """
        将内容写入文件
        
        Args:
            file_path (str): 文件路径
            content (str): 要写入的内容
            
        Raises:
            IOError: 当文件写入失败时
            PermissionError: 当没有写入权限时
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        except IOError as e:
            raise IOError(f"文件写入错误: {file_path}") from e
        except PermissionError as e:
            raise PermissionError(f"没有写入权限: {file_path}") from e


# 创建全局实例
file_handler = FileHandler()

# 提供函数接口
def read_file(file_path):
    """
    读取文件内容的函数接口
    
    Args:
        file_path (str): 文件路径
        
    Returns:
        str: 文件内容
    """
    return file_handler.read_file(file_path)

def write_result(file_path, result):
    """
    写入结果的函数接口
    
    Args:
        file_path (str): 文件路径
        result (float): 相似度结果
    """
    # 将浮点数转换为字符串，保留4位小数
    if isinstance(result, float):
        content = f"{result:.4f}"
    else:
        content = str(result)
    file_handler.write_file(file_path, content)