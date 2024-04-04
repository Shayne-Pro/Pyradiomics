from PIL import Image
import os

# 检查并创建目标文件夹
output_folder = 'Path/to/image_gray'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历原始图片文件夹中的所有文件
input_folder = 'Path/to/image'
for filename in os.listdir(input_folder):
    if filename.endswith('.png'):
        # 打开图片并转换为灰度
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path).convert('L')  # 'L'表示转换为灰度图像

        # 保存转换后的图片到目标文件夹，保持原文件名
        output_path = os.path.join(output_folder, filename)
        img.save(output_path)

print('转换完成！')
