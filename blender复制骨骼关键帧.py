import bpy

# 设置源骨架和目标骨架的名称
source_armature_name = "Armature"
target_armature_name = "Armature.001"

# 获取源骨架和目标骨架对象
source_armature = bpy.data.objects.get(source_armature_name)
target_armature = bpy.data.objects.get(target_armature_name)

# 确保源骨架和目标骨架都存在
if not source_armature or not target_armature:
    print("请确保源骨架和目标骨架的名称正确")
else:
    # 获取源骨架的动作数据
    source_action = source_armature.animation_data.action

    if not source_action:
        print("源骨架没有关键帧数据")
    else:
        # 确保目标骨架有动作数据
        if not target_armature.animation_data:
            target_armature.animation_data_create()
        if not target_armature.animation_data.action:
            target_action = bpy.data.actions.new(name="TargetAction")
            target_armature.animation_data.action = target_action
        else:
            target_action = target_armature.animation_data.action

        # 清除目标骨架的所有关键帧
        target_action.fcurves.clear()

        # 使用事务批量处理，避免频繁更新视图
        bpy.context.view_layer.objects.active = target_armature
        with bpy.context.temp_override(active_object=target_armature):
            # 复制每个关键帧
            for fcurve in source_action.fcurves:
                new_fcurve = target_action.fcurves.new(data_path=fcurve.data_path, index=fcurve.array_index)
                for keyframe in fcurve.keyframe_points:
                    new_fcurve.keyframe_points.insert(keyframe.co[0], keyframe.co[1], options={'FAST'})

        print("关键帧数据已复制")

        # 直接更新视图层，减少多余操作
        bpy.context.view_layer.update()
