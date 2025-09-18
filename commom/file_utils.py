import os

def read_file(path):
    """
        以二进制模式读取文件，并返回一个元组，用于requests库的files参数。
        :param file_path: 文件在本地的路径
        :return: 一个元组，格式为 (文件名, 文件对象)
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件未找到: {path}")
    file_name = os.path.basename(path)
    file_object = open(path,'rb')

    return (file_name,file_object)
