from krita import *
import os  # 导入os模块以处理文件路径

# 获取当前活动文档
doc = Krita.instance().activeDocument()

if doc:
    # 获取当前文档的完整文件名（包括路径）
    doc_file_path = doc.fileName()
    if doc_file_path:
        # 从文档路径中提取目录路径
        save_dir = os.path.dirname(doc_file_path)
        # 设置krita.txt的保存路径与图片路径相同
        out_file_path = os.path.join(save_dir, "krita.txt")
    else:
        print("文档没有保存路径。")
        save_dir = None
        out_file_path = None

    if save_dir and out_file_path:
        # 获取选区（返回的是选区的QImage对象）
        selection = doc.selection()

        # 检查是否有选区（如果选区为空，宽度和高度会为 0）
        if selection.width() > 0 and selection.height() > 0:
            # 获取当前文档名称（只保留文件名，不包括路径）
            filename = os.path.basename(doc_file_path)

            # 打印文档名称
            print(f"当前文档: {filename}")

            # 获取选区的矩形区域
            x = selection.x()
            y = selection.y()
            width = selection.width()
            height = selection.height()

            # 计算选区的中心坐标
            center_x = x + width // 2
            center_y = y + height // 2

            # 打印中心坐标
            print(f"选区中心坐标: ({center_x}, {center_y}) 像素")

        else:
            print("当前没有选区。")
            filename = os.path.basename(doc_file_path)
            center_x = None
            center_y = None

        # 创建要保存的数据行，使用空格分隔
        data_line = f"{filename} {center_x} {center_y}\n"

        # 尝试将数据追加保存到krita.txt文件中
        try:
            with open(out_file_path, "a") as f:  # 使用'a'模式进行追加写入
                f.write(data_line)
            print(f"数据已保存到: {out_file_path}")
        except Exception as e:
            print(f"保存krita.txt时发生错误: {e}")
    else:
        print("无法保存krita.txt，因为文档没有指定保存路径。")
else:
    print("没有打开的文档。")
