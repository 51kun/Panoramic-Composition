import numpy as np
import bpy

frame_1 = 100 #第1个全景图的帧数
frame_2 = 300 #第2个全景图的帧数
L = 2880      #全景图短边像素

object_name = "最终结果"  # 物体名称
# 获取Blender中的krita.txt文本数据块
def get_text_data(text_name="krita.txt"):
    # 获取文本数据块
    text = bpy.data.texts.get(text_name)
    if not text:
        print(f"未找到名为 {text_name} 的文本数据块。")
        return [], []
    
    # 获取文本内容并按行分割
    lines = text.as_string().split("\n")
    
    # 初始化空列表存储数据
    data_1, data_2 = [], []
    
    # 遍历每一行，将行号、文件名和坐标分开，并转换为数字
    for i, line in enumerate(lines, start=1):  # i 是行号
        if line.strip():  # 排除空行
            parts = line.split()
            filename = parts[0]
            x, y = int(parts[1]), int(parts[2])
            # 根据行号的奇偶性分别存储数据
            target_data = data_1 if i % 2 == 1 else data_2
            target_data.append([i, filename, x, y])
    
    return np.array(data_1, dtype=object), np.array(data_2, dtype=object)

# 定义函数获取物体在指定帧的位置信息和旋转矩阵（NumPy 格式）
def get_object_transform_at_frame(object_name, frame):
    # 获取物体对象
    obj = bpy.data.objects.get(object_name)
    
    if obj:
        # 设置当前帧
        bpy.context.scene.frame_set(frame)
        
        # 获取物体在指定帧的精确位置和旋转（高精度）
        location = obj.matrix_world.translation  # 获取世界坐标系下的精确位置
        rotation_quaternion = obj.rotation_quaternion  # 获取四元数旋转
        
        # 将位置转换为 NumPy 格式
        location_np = np.array([location.x, location.y, location.z])
        
        # 将四元数转换为旋转矩阵
        rotation_matrix = rotation_quaternion.to_matrix()
        
        # 将旋转矩阵转换为 NumPy 格式
        rotation_matrix_np = np.array(rotation_matrix)
        
        return location_np, rotation_matrix_np
    else:
        print(f"物体 '{object_name}' 没有找到。")
        return None, None

# 计算交点的函数
def calculate_intersection(location_1, new_dan_1, location_2, new_dan_2):
    # 计算两个直线的方向向量
    dA, dB = new_dan_1, new_dan_2

    # 计算两个直线间的差值
    A = np.array([dA, -dB]).T
    b = location_2 - location_1

    # 通过最小二乘法解线性方程，得到两个参数t和s
    t_s = np.linalg.lstsq(A, b, rcond=None)[0]
    t, s = t_s[0], t_s[1]

    # 计算两条直线上的点
    QA = location_1 + t * dA
    QB = location_2 + s * dB

    # 计算近似交点
    intersection = (QA + QB) / 2
    return intersection

# 球面坐标转为笛卡尔坐标

def spherical_to_cartesian(m, n):
    a = (1 - m / L) * np.pi
    b = (0.5 - n / L) * np.pi

    x = np.cos(b) * np.cos(a)
    y = np.cos(b) * np.sin(a)
    z = np.sin(b)

    return np.array([x, y, z])

# 创建网格物体的函数
def create_points_mesh(name, points):
    # 创建一个新的网格数据块
    mesh = bpy.data.meshes.new(name)
    
    # 创建新的对象
    obj = bpy.data.objects.new(name, mesh)
    
    # 将物体添加到当前场景
    bpy.context.collection.objects.link(obj)
    
    # 确保物体处于活动状态
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # 创建网格数据
    mesh.from_pydata(points, [], [])  # 只有顶点，没有边和面
    
    # 更新网格
    mesh.update()

# 主逻辑
def main(object_name, frame_1, frame_2, data_1_array, data_2_array):
    location_1, rotation_matrix_1 = get_object_transform_at_frame(object_name, frame_1)
    location_2, rotation_matrix_2 = get_object_transform_at_frame(object_name, frame_2)

    print(f"location_1: {location_1}")
    print(f"rotation_matrix_1:\n{rotation_matrix_1}")
    print(f"location_2: {location_2}")
    print(f"rotation_matrix_2:\n{rotation_matrix_2}")

    # 存储所有交点的坐标
    intersections = []

    # 遍历并计算交点
    for i in range(int(data_2_array[-1][0] / 2)):
        print(f"Processing pair {i + 1}")
        
        dan_1 = spherical_to_cartesian(data_1_array[i][-2], data_1_array[i][-1])
        dan_2 = spherical_to_cartesian(data_2_array[i][-2], data_2_array[i][-1])

        new_dan_1 = rotation_matrix_1 @ dan_1
        new_dan_2 = rotation_matrix_2 @ dan_2

        print(f"new_dan_1:\n{new_dan_1}")
        print(f"new_dan_2:\n{new_dan_2}")

        # 调用函数计算交点
        intersection = calculate_intersection(location_1, new_dan_1, location_2, new_dan_2)
        print(f"Approximate intersection: {intersection}")

        # 将交点添加到列表中
        intersections.append(intersection)

    # 将所有交点的坐标作为网格的顶点
    create_points_mesh("两全景图定点", intersections)

# 获取数据并执行主逻辑
data_1_array, data_2_array = get_text_data()
if data_1_array.size > 0 and data_2_array.size > 0:
    main(object_name, frame_1, frame_2, data_1_array, data_2_array)
