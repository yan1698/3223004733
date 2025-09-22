def read_file(file_path):
    """
    读取文件内容，自动处理编码问题
    """
    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'ascii']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            raise Exception(f"文件未找到: {file_path}")
    
    # 如果所有编码都失败，尝试二进制读取
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            # 尝试检测编码
            import chardet
            result = chardet.detect(content)
            encoding = result['encoding']
            return content.decode(encoding)
    except Exception as e:
        raise Exception(f"无法读取文件 {file_path}，编码问题: {str(e)}")

def write_result(file_path, similarity):
    """
    将结果写入文件 使用UTF-8编码
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"{similarity:.2f}")
    except IOError:
        raise Exception(f"文件写入错误: {file_path}")