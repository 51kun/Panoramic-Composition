#用于vrm与fbx材质替换
import bpy
import re

# 定义被替换的材质名称的正则表达式模式
source_material_pattern = re.compile(r"(.*)\(Instance\)\.001")

# 创建字典来存储源材质和目标材质的映射
materials_map = {}

# 预处理所有材质，找到符合条件的源材质和对应的目标材质
for mat in bpy.data.materials:
    match = source_material_pattern.match(mat.name)
    if match:
        source_material_name = match.group(1) + "(Instance)"
        if source_material_name in bpy.data.materials:
            materials_map[mat.name] = bpy.data.materials[source_material_name]

# 遍历所有对象并替换材质
for obj in bpy.data.objects:
    if hasattr(obj.data, 'materials'):
        for i, mat in enumerate(obj.data.materials):
            if mat and mat.name in materials_map:
                obj.data.materials[i] = materials_map[mat.name]
                print(f"Replaced material on object '{obj.name}' from '{mat.name}' to '{materials_map[mat.name].name}'")

print("Material replacement completed.")
'''
#用于vrm与usd材质替换
import bpy
import re

# 定义新的材质名称的正则表达式模式
#source_material_pattern = re.compile(r"(.*)__Instance_\.001")
source_material_pattern = re.compile(r"(.*)__Instance_")
# 创建字典来存储源材质和目标材质的映射
materials_map = {}

# 预处理所有材质，找到符合条件的源材质和对应的目标材质
for mat in bpy.data.materials:
    match = source_material_pattern.match(mat.name)
    if match:
        # 提取源材质名称
        source_material_name = match.group(1) + " (Instance)"
        if source_material_name in bpy.data.materials:
            materials_map[mat.name] = bpy.data.materials[source_material_name]

# 遍历所有对象并替换材质
for obj in bpy.data.objects:
    if hasattr(obj.data, 'materials'):
        for i, mat in enumerate(obj.data.materials):
            if mat and mat.name in materials_map:
                obj.data.materials[i] = materials_map[mat.name]
                print(f"Replaced material on object '{obj.name}' from '{mat.name}' to '{materials_map[mat.name].name}'")

print("Material replacement completed.")


'''
