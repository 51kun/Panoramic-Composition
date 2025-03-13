import cv2
import numpy as np
import os

def overlay_blend(bottom_img, top_img):
    """
    实现 CSP 叠加（Overlay）模式
    bottom_img: 底层图像（背景）
    top_img: 顶层图像（前景）
    """
    bottom = bottom_img.astype(np.float32) / 255.0
    top = top_img.astype(np.float32) / 255.0
    
    mask = bottom < 0.5
    result = np.where(mask, 2.0 * bottom * top, 1.0 - 2.0 * (1.0 - bottom) * (1.0 - top))
    
    return (result * 255).astype(np.uint8)

def process_images(input_folder, overlay_image, output_folder):
    """
    对文件夹A中的所有图片，叠加文件overlay_image并保存到文件夹B
    确保透明度与底层图像一致。
    """
    # 获取文件夹A中所有文件
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 读取叠加图像并调整大小
    overlay_img = cv2.imread(overlay_image, cv2.IMREAD_UNCHANGED)
    if overlay_img.shape[2] == 4:
        overlay_rgb, overlay_alpha = overlay_img[:, :, :3], overlay_img[:, :, 3:]
    else:
        overlay_rgb, overlay_alpha = overlay_img, None
    
    for filename in os.listdir(input_folder):
        img_path = os.path.join(input_folder, filename)
        
        # 确保只处理图片文件
        if img_path.lower().endswith(('png', 'jpg', 'jpeg')):
            # 读取底层图片
            img1 = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            
            # 调整图像大小一致
            h, w = img1.shape[:2]
            img2_resized_rgb = cv2.resize(overlay_rgb, (w, h))
            
            # 叠加（仅对 RGB 计算，不包含 Alpha 通道）
            if img1.shape[2] == 4:
                img1_rgb, alpha1 = img1[:, :, :3], img1[:, :, 3:]
            else:
                img1_rgb, alpha1 = img1, None
            
            # 计算 Overlay 叠加
            blended_rgb = overlay_blend(img1_rgb, img2_resized_rgb)
            
            # 如果原图有 Alpha 通道，则保留
            if alpha1 is not None:
                # 保证透明度通道不丢失，且输出图像透明度与底层一致
                blended = np.dstack((blended_rgb, alpha1))
            else:
                blended = blended_rgb
            
            # 保存结果
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, blended)
            print(f"保存完成: {output_path}")

def main():
    input_folder = "A"  # 文件夹A
    overlay_image = "p.png"  # 要叠加的柏林噪声图片
    output_folder = "B"  # 文件夹B
    
    process_images(input_folder, overlay_image, output_folder)

if __name__ == "__main__":
    main()
