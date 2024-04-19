import os

count = 0
def rename_png_files(folder_path, end_name):
    global count
    # 遍历文件夹中的所有内容，包括子文件夹
    for root, dirs, files in os.walk(folder_path):
        # 获取当前文件夹的名称
        folder_name = os.path.basename(root)
        
        # 遍历当前文件夹中的所有文件
        for filename in files:
            # 检查文件是否为PNG图片
            if filename.endswith(end_name):
                # 构建新的文件名
                folder_name = folder_name.replace('_json', '')
                new_filename = f"{folder_name}_{filename}"
                
                # 构建原文件路径和新文件路径
                old_filepath = os.path.join(root, filename)
                new_filepath = os.path.join(root, new_filename)
                
                # 重命名文件
                os.rename(old_filepath, new_filepath)
                count += 1
                print(f"Renamed: {old_filepath} -> {new_filepath}")
                print(count)

# 指定要遍历的文件夹路径
folder_path = 'Path/to/json_folder'

# 调用函数进行重命名
rename_png_files(folder_path,'img.png')
