import os

def rename_png_files_in_folder(folder_path):
    # 获取所有png文件
    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    
    # 按名称排序
    png_files.sort()

    # 重命名文件
    for index, file in enumerate(png_files, start=1):
        # 构造新文件名
        new_name = f"{str(index).zfill(4)}.png"
        # 完整的旧文件路径
        old_file_path = os.path.join(folder_path, file)
        # 完整的新文件路径
        new_file_path = os.path.join(folder_path, new_name)
        # 重命名
        os.rename(old_file_path, new_file_path)

    return f"文件已重命名，从0001.png开始。"

# 假设文件夹路径是"B"，这里只是演示，实际使用时需要替换为正确的路径
folder_path = "B_J_105"
rename_png_files_in_folder(folder_path)
