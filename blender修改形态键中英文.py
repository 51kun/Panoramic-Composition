import bpy

# 创建中英文对照字典
shape_key_translation = {
    "Basis": "基础",
    "Fcl_ALL_Neutral": "全部_中性",
    "Fcl_ALL_Angry": "全部_愤怒",
    "Fcl_ALL_Fun": "全部_开心",
    "Fcl_ALL_Joy": "全部_喜悦",
    "Fcl_ALL_Sorrow": "全部_悲伤",
    "Fcl_ALL_Surprised": "全部_惊讶",
    "Fcl_BRW_Angry": "眉毛_愤怒",
    "Fcl_BRW_Fun": "眉毛_开心",
    "Fcl_BRW_Joy": "眉毛_喜悦",
    "Fcl_BRW_Sorrow": "眉毛_悲伤",
    "Fcl_BRW_Surprised": "眉毛_惊讶",
    "Fcl_EYE_Natural": "眼睛_自然",
    "Fcl_EYE_Angry": "眼睛_愤怒",
    "Fcl_EYE_Close": "眼睛_闭眼",
    "Fcl_EYE_Close_R": "眼睛_右闭眼",
    "Fcl_EYE_Close_L": "眼睛_左闭眼",
    "Fcl_EYE_Fun": "眼睛_开心",
    "Fcl_EYE_Joy": "眼睛_喜悦",
    "Fcl_EYE_Joy_R": "眼睛_右喜悦",
    "Fcl_EYE_Joy_L": "眼睛_左喜悦",
    "Fcl_EYE_Sorrow": "眼睛_悲伤",
    "Fcl_EYE_Surprised": "眼睛_惊讶",
    "Fcl_EYE_Spread": "眼睛_扩散",
    "Fcl_EYE_Iris_Hide": "眼睛_隐藏虹膜",
    "Fcl_EYE_Highlight_Hide": "眼睛_隐藏高光",
    "Fcl_MTH_Close": "嘴_闭嘴",
    "Fcl_MTH_Up": "嘴_向上",
    "Fcl_MTH_Down": "嘴_向下",
    "Fcl_MTH_Angry": "嘴_愤怒",
    "Fcl_MTH_Small": "嘴_小",
    "Fcl_MTH_Large": "嘴_大",
    "Fcl_MTH_Neutral": "嘴_中性",
    "Fcl_MTH_Fun": "嘴_开心",
    "Fcl_MTH_Joy": "嘴_喜悦",
    "Fcl_MTH_Sorrow": "嘴_悲伤",
    "Fcl_MTH_Surprised": "嘴_惊讶",
    "Fcl_MTH_SkinFung": "嘴_皮肤皱褶",
    "Fcl_MTH_SkinFung_R": "嘴_右皮肤皱褶",
    "Fcl_MTH_SkinFung_L": "嘴_左皮肤皱褶",
    "Fcl_MTH_A": "嘴_A音",
    "Fcl_MTH_I": "嘴_I音",
    "Fcl_MTH_U": "嘴_U音",
    "Fcl_MTH_E": "嘴_E音",
    "Fcl_MTH_O": "嘴_O音",
    "Fcl_HA_Hide": "头发_隐藏",
    "Fcl_HA_Fung1": "吸血鬼牙齿",
    "Fcl_HA_Fung1_Low": "吸血鬼牙齿_低",
    "Fcl_HA_Fung1_Up": "吸血鬼牙齿_高",
    "Fcl_HA_Fung2": "鲨鱼牙齿",
    "Fcl_HA_Fung2_Low": "鲨鱼牙齿_低",
    "Fcl_HA_Fung2_Up": "鲨鱼牙齿_高",
    "Fcl_HA_Fung3": "门牙变尖",
    "Fcl_HA_Fung3_Up": "门牙变尖_高",
    "Fcl_HA_Fung3_Low": "门牙变尖_低",
    "Fcl_HA_Short": "头发_短",
    "Fcl_HA_Short_Up": "头发_短_高",
    "Fcl_HA_Short_Low": "头发_短_低"
}

# 获取指定的网格体对象
obj_name = "Face"
obj = bpy.data.objects.get(obj_name)

# 检查对象是否存在以及是否是网格体
if obj is not None and obj.type == 'MESH':
    # 检查对象是否有形态键
    if obj.data.shape_keys:
        shape_keys = obj.data.shape_keys.key_blocks
        for shape_key in shape_keys:
            # 获取对应的中文名称
            new_name = shape_key_translation.get(shape_key.name, shape_key.name)
            # 打印旧名称和新名称（可选）
            print(f"Renaming '{shape_key.name}' to '{new_name}'")
            # 修改形态键名称
            shape_key.name = new_name
        print("Shape key names have been renamed.")
    else:
        print("No shape keys found in the selected mesh object.")
else:
    print("The selected object is not a mesh or it does not exist.")
