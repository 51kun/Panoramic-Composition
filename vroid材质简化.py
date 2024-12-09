import bpy

# 查找名为'Armature'的Armature对象
armature = bpy.data.objects.get('Armature')

def get_armature_and_children_materials(armature):
    materials = set()
    for obj in armature.children:
        if obj.type == 'MESH':
            for slot in obj.material_slots:
                if slot.material:
                    materials.add(slot.material)
    return materials

def remove_invalid_and_reposition_nodes(material):
    if material.node_tree:
        nodes_to_remove = []
        image_nodes = {}
        
        # 第一遍：识别并收集要移除的节点
        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                if not node.image:
                    nodes_to_remove.append(node)
                else:
                    if node.image.name not in image_nodes:
                        image_nodes[node.image.name] = node
                    else:
                        nodes_to_remove.append(node)
            else:
                nodes_to_remove.append(node)
        
        # 移除无效节点
        for node in nodes_to_remove:
            material.node_tree.nodes.remove(node)
        
        connected_nodes = set()
        unconnected_nodes = []
        
        for node in material.node_tree.nodes:
            if any(input.is_linked for input in node.inputs):
                connected_nodes.add(node)
            else:
                unconnected_nodes.append(node)
        
        # 重新定位节点
        x_offset = 0
        spacing = 300
        y_connected = 0
        y_unconnected = -spacing
        
        for node in connected_nodes:
            node.location.x = x_offset
            node.location.y = y_connected
            x_offset += spacing
        
        x_offset = 0
        
        for node in unconnected_nodes:
            node.location.x = x_offset
            node.location.y = y_unconnected
            x_offset += spacing
        
        node_tree = material.node_tree
        
        # 创建Principled BSDF节点
        bsdf_node = node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (x_offset, y_connected)
        
        # 设置糙度和折射率
        bsdf_node.inputs['Roughness'].default_value = 1.0
        bsdf_node.inputs['IOR'].default_value = 1.0  # 设定折射率
        
        # 创建Material Output节点
        output_node = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (x_offset + spacing, y_connected)
        
        # 将Principled BSDF节点连接到Material Output节点
        node_tree.links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        # 查找标记为'Lit Color Texture'的图像纹理，并连接到Principled BSDF的Base Color
        for node in node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.label == 'Lit Color Texture':
                color_socket = bsdf_node.inputs['Base Color']
                alpha_socket = bsdf_node.inputs.get('Alpha', None)
                
                if color_socket:
                    node_tree.links.new(node.outputs['Color'], color_socket)
                
                if alpha_socket and 'Alpha' in node.outputs:
                    node_tree.links.new(node.outputs['Alpha'], alpha_socket)
        
        # 查找标记为'Normal Map Texture'的图像纹理，并连接到Principled BSDF的法线输入
        for node in node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.label == 'Normal Map Texture':
                normal_socket = bsdf_node.inputs.get('Normal', None)
                
                if normal_socket:
                    normal_map_node = node_tree.nodes.new(type='ShaderNodeNormalMap')
                    normal_map_node.location = (x_offset, y_connected + spacing)
                    node_tree.links.new(node.outputs['Color'], normal_map_node.inputs['Color'])
                    node_tree.links.new(normal_map_node.outputs['Normal'], normal_socket)



if armature and armature.type == 'ARMATURE':
    materials_to_process = get_armature_and_children_materials(armature)
    
    for material in materials_to_process:
        remove_invalid_and_reposition_nodes(material)
    
    print("完成了只处理Armature及其子集的材质的操作。")
else:
    print("未找到名为'Armature'的Armature对象。")
