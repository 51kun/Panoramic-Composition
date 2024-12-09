import bpy
import numpy as np

#需要改，环境纹理勾选自动刷新，3DEqualizer4追踪insta360x3外镜头初始参数：胶片高度5.9962，焦距33.4592
start_frame = 1          #起始帧
end_frame = 90           #结束帧
jiequ = "摄像机"          #截取全景图的摄像机
xiangji_3de = "0001_1_1" #3de导出的摄像机

#不需要改
fanxiangqiuti = "反向球体"
zuizhongjieguo = "最终结果"
obj = bpy.data.objects.get(jiequ)
empty_object = bpy.data.objects.new(fanxiangqiuti, None)
bpy.context.collection.objects.link(empty_object)

def R(quaternion):
    w, x, y, z = quaternion
    return np.array([
        [1 - 2 * (y**2 + z**2), 2 * (x * y - w * z), 2 * (x * z + w * y)],
        [2 * (x * y + w * z), 1 - 2 * (x**2 + z**2), 2 * (y * z - w * x)],
        [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x**2 + y**2)]
    ])

def W(R):
    trace = np.trace(R)
    if trace > 0:
        w = np.sqrt(1 + trace) / 2
        x = (R[2, 1] - R[1, 2]) / (4 * w)
        y = (R[0, 2] - R[2, 0]) / (4 * w)
        z = (R[1, 0] - R[0, 1]) / (4 * w)
    elif R[0, 0] > max(R[1, 1], R[2, 2]):
        x = np.sqrt(1 + R[0, 0] - R[1, 1] - R[2, 2]) / 2
        w = (R[2, 1] - R[1, 2]) / (4 * x)
        y = (R[0, 1] + R[1, 0]) / (4 * x)
        z = (R[0, 2] + R[2, 0]) / (4 * x)
    elif R[1, 1] > R[2, 2]:
        y = np.sqrt(1 + R[1, 1] - R[0, 0] - R[2, 2]) / 2
        w = (R[0, 2] - R[2, 0]) / (4 * y)
        x = (R[0, 1] + R[1, 0]) / (4 * y)
        z = (R[1, 2] + R[2, 1]) / (4 * y)
    else:
        z = np.sqrt(1 + R[2, 2] - R[0, 0] - R[1, 1]) / 2
        w = (R[1, 0] - R[0, 1]) / (4 * z)
        x = (R[0, 2] + R[2, 0]) / (4 * z)
        y = (R[1, 2] + R[2, 1]) / (4 * z)
    return w, x, y, z

def get_quaternion_data(obj, start_frame, end_frame):
    num_frames = end_frame - start_frame + 1
    quaternions = np.empty((num_frames, 4), dtype=np.float64)

    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        quat = obj.rotation_quaternion
        b = R([quat.w, quat.x, quat.y, quat.z])
        c = R([0.5, 0.5, -0.5, -0.5])

        b_inv = np.linalg.inv(b)
        a = c @ b_inv
        quaternions[frame - start_frame] = W(a)

    return quaternions

def apply_quaternion_to_empty(empty_obj, quaternions, start_frame):
    for i, quat in enumerate(quaternions):
        empty_obj.rotation_quaternion = quat
        empty_obj.keyframe_insert(data_path="rotation_quaternion", frame=start_frame + i)

quaternions = get_quaternion_data(obj, start_frame, end_frame)
apply_quaternion_to_empty(empty_object, quaternions, start_frame)

empty_object.rotation_mode = 'QUATERNION'

arrow_object = bpy.data.objects.new("箭头", None)
bpy.context.collection.objects.link(arrow_object)
empty_object.parent = arrow_object

copy_location = arrow_object.constraints.new(type='COPY_LOCATION')
copy_location.target = bpy.data.objects.get(xiangji_3de)

copy_rotation = arrow_object.constraints.new(type='COPY_ROTATION')
copy_rotation.target = bpy.data.objects.get(xiangji_3de)
copy_rotation.mix_mode = 'BEFORE'

arrow_object.rotation_euler = (np.radians(-90), np.radians(90), 0)

if zuizhongjieguo in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[zuizhongjieguo], do_unlink=True)

result_obj = bpy.data.objects.new(zuizhongjieguo, None)
bpy.context.scene.collection.objects.link(result_obj)

for frame in range(start_frame, end_frame + 1):
    bpy.context.scene.frame_set(frame)

    matrix_world = empty_object.matrix_world

    location = matrix_world.to_translation()
    rotation = matrix_world.to_quaternion()

    result_obj.location = location
    result_obj.rotation_mode = 'QUATERNION'
    result_obj.rotation_quaternion = rotation

    result_obj.keyframe_insert(data_path="location", frame=frame)
    result_obj.keyframe_insert(data_path="rotation_quaternion", frame=frame)

def create_panorama_sphere():
    sphere_name = "全景视频球"
    if sphere_name in bpy.data.objects:
        return
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=64,
        ring_count=32,
        radius=1,
        location=(0, 0, 0)
    )

    sphere = bpy.context.active_object

    sphere.name = sphere_name

    sphere.scale = (10, 10, 10)

    material = bpy.data.materials.new(name="Panorama_Material")
    material.use_nodes = True
    sphere.data.materials.append(material)

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    for node in nodes:
        nodes.remove(node)

    texture_coord_node = nodes.new(type="ShaderNodeTexCoord")
    mapping_node = nodes.new(type="ShaderNodeMapping")
    env_texture_node = nodes.new(type="ShaderNodeTexEnvironment")
    shader_output_node = nodes.new(type="ShaderNodeOutputMaterial")

    texture_coord_node.location = (-400, 0)
    mapping_node.location = (-200, 0)
    env_texture_node.location = (0, 0)
    shader_output_node.location = (300, 0)

    links.new(texture_coord_node.outputs[3], mapping_node.inputs[0])
    links.new(mapping_node.outputs[0], env_texture_node.inputs[0])
    links.new(env_texture_node.outputs[0], shader_output_node.inputs[0])

    target_object = bpy.data.objects[zuizhongjieguo]

    copy_location_constraint = sphere.constraints.new(type='COPY_LOCATION')
    copy_location_constraint.target = target_object

    copy_rotation_constraint = sphere.constraints.new(type='COPY_ROTATION')
    copy_rotation_constraint.target = target_object

create_panorama_sphere()

bpy.ops.object.camera_add()
camera = bpy.context.object
camera.name = "主_摄像机"

camera.data.lens = 25

wyk = bpy.data.objects.get(zuizhongjieguo)

if wyk:
    copy_location_constraint = camera.constraints.new(type='COPY_LOCATION')
    copy_location_constraint.target = wyk

bpy.ops.object.empty_add(type='ARROWS', radius=1)
tracking_empty = bpy.context.object
tracking_empty.name = "摄像机跟踪"

tracking_constraint = camera.constraints.new(type='TRACK_TO')
tracking_constraint.target = tracking_empty
tracking_constraint.track_axis = 'TRACK_NEGATIVE_Z'
tracking_constraint.up_axis = 'UP_Y'

bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100

empty_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'EMPTY' and obj.name.startswith('p') and obj.name[1:].isdigit()]

mesh_data = bpy.data.meshes.new(name="标记点2")
mesh_object = bpy.data.objects.new("标记点", mesh_data)

bpy.context.collection.objects.link(mesh_object)

vertices = []

for empty in empty_objects:
    world_location = empty.matrix_world.translation
    vertices.append((world_location.x, world_location.y, world_location.z))

mesh_data.from_pydata(vertices, [], [])

mesh_data.update()

mesh_object.select_set(True)
bpy.context.view_layer.objects.active = mesh_object

if "拍摄集合" not in bpy.data.collections:
    collection = bpy.data.collections.new("拍摄集合")
    bpy.context.scene.collection.children.link(collection)
else:
    collection = bpy.data.collections["拍摄集合"]

objects_to_move = ["主_摄像机", "全景视频球", "最终结果", "摄像机跟踪","标记点"]

for obj_name in objects_to_move:
    obj = bpy.data.objects.get(obj_name)
    if obj:
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        
        collection.objects.link(obj)