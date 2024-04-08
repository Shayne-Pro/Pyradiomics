import pandas as pd

file1 = 'features_1.xlsx'
file2 = 'features_2.xlsx'

# 载入第一个Excel文件
df1 = pd.read_excel(file1)

# 载入第二个Excel文件
df2 = pd.read_excel(file2)

# 按列合并数据
# 'outer'合并方式会保留所有原始索引，'left'和'right'会分别只保留左表或右表的索引
# 如果想要合并的列名相同，可以使用'merge'函数，并设置'on'参数
merged_df = pd.concat([df1, df2], ignore_index=True)

# 保存合并后的数据到新的Excel文件
merged_df.to_excel('features_merged.xlsx', index=False)
