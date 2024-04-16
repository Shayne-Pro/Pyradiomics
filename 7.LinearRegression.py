import pandas as pd  
import numpy as np  
from sklearn.linear_model import LinearRegression  
  
# 读取Excel文件  
file_path = r'Path/to/xlsx'  # 替换为你的Excel文件路径  
df = pd.read_excel(file_path, engine='openpyxl')  # 使用openpyxl引擎来读取xlsx文件  
  
# 提取特征列和标签列  
X_cols = [  
    'diagnostics_Image.original_Minimum',  
    'original_firstorder_Median',  
    'original_glcm_ClusterShade',  
    'original_gldm_GrayLevelNonUniformity',  
    'original_gldm_LargeDependenceHighGrayLevelEmphasis',  
    'original_ngtdm_Strength'  
]  
y_col = 'score'  
  
# 确保列名存在于DataFrame中  
assert all(col in df.columns for col in X_cols), "Some column names are not found in the DataFrame."  
assert y_col in df.columns, "The label column is not found in the DataFrame."  
  
# 提取X和y  
X = df[X_cols]  
y = df[y_col]  
  
# 将X和y转换为numpy数组，因为scikit-learn需要numpy数组作为输入  
X = X.values  
y = y.values  
  
# 确保没有缺失值  
assert not np.any(np.isnan(X)), "There are NaN values in the features."  
assert not np.any(np.isnan(y)), "There are NaN values in the labels."  
  
# 创建并拟合线性回归模型  
model = LinearRegression()  
model.fit(X, y)  
  
# 输出模型系数和截距  
print("Coefficients:", model.coef_)  
print("Intercept:", model.intercept_)  
  
# 如果你想要预测新数据，可以这样做：  
# new_data = np.array([[...], [...], ...])  # 替换为你的新数据  
# predictions = model.predict(new_data)  
# print(predictions)