import os
import numpy as np
import SimpleITK as sitk
import radiomics
import pandas as pd 
from radiomics.featureextractor import RadiomicsFeatureExtractor
from radiomics import shape2D
import PIL.Image as Image
from pathlib import Path

# 获取标签的函数
def get_label(image_path):
    image_label_name = str(Path(image_path).parent.parent.name)
    if image_label_name == 'abnormal':
        image_label = 1
    elif image_label_name == 'normal':
        image_label = 0
    else:
        raise Exception("Image label error!")
    return image_label

image_dir = 'Path/to/image_gray'
mask_dir = 'Path/to/mask'

image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('_img.png')]
mask_files = [os.path.join(mask_dir, f) for f in os.listdir(mask_dir) if f.endswith('_mask.png')]

assert len(image_files) == len(mask_files), "Number of images and masks must be equal."

# 确保图像文件和掩膜文件按相同顺序排列
# image_files, mask_files = zip(*sorted(zip(image_files, mask_files)))

# 使用文件名作为排序键，确保图像和掩膜文件按相同的顺序排列
image_files = sorted(image_files, key=lambda x: os.path.splitext(os.path.basename(x))[0])
mask_files = sorted(mask_files, key=lambda x: os.path.splitext(os.path.basename(x))[0])

extractor = RadiomicsFeatureExtractor()
# extractor.featureClasses = ['shape2D']  # 只提取2D形状特征
extractor.settings['force2D'] = True

results = []

for image_path, mask_path in zip(image_files, mask_files):
    # 读取图像和掩膜
    # image_sitk = sitk.ReadImage(image_path)
    # mask_sitk = sitk.ReadImage(mask_path)
    image = Image.open(image_path)
    mask = Image.open(mask_path)
    image_sitk = sitk.GetImageFromArray(image)
    mask_sitk = sitk.GetImageFromArray(mask)

    # 确保图像和掩膜具有相同的空间属性（尺寸、方向等）
    assert image_sitk.GetSize() == mask_sitk.GetSize(), "Image and mask dimensions must match."
    assert image_sitk.GetOrigin() == mask_sitk.GetOrigin(), "Image and mask origins must match."
    assert image_sitk.GetSpacing() == mask_sitk.GetSpacing(), "Image and mask spacings must match."
    assert image_sitk.GetDirection() == mask_sitk.GetDirection(), "Image and mask directions must match."

    # 提取特征
    result = extractor.execute(image_sitk, mask_sitk, label=255)

    # 将结果添加到列表中
    results.append(result)


# 创建一个空的DataFrame来存储所有特征  
all_features_df = pd.DataFrame()  
  
# 遍历results，将每个样本的特征添加到DataFrame中  
for index, features_dict in enumerate(results):  
    # 获取图像的标签
    label = get_label(image_files[index])
    # 转换字典为DataFrame，不指定index  
    sample_df = pd.DataFrame.from_dict(features_dict, orient='index').transpose()  
    # 重命名行索引，如果需要的话  
    sample_df.index = [index]  
    # 添加标签列到DataFrame
    sample_df.insert(0, 'label', label)
    # 将当前样本的特征添加到总DataFrame中  
    all_features_df = pd.concat([all_features_df, sample_df], ignore_index=True)
  
# 设置Excel文件的路径和名称  
output_file = 'features.xlsx'  
  
# 将DataFrame写入Excel文件，不包含索引列  
all_features_df.to_excel(output_file, index=False)  
  
print(f"Features have been saved to {output_file}")