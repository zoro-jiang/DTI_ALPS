# DTI_ALPS 计算ALPS指标程序指引

`写在前言：在使用本程序前，请确保您已经安装了FSL（https://fsl.fmrib.ox.ac.uk/fsl/docs/#/install/index）和以下python的库：`

    1. ​nibabel 神经影像数据读写（NIfTI等）
    2. ​numpy 数值计算
    3. ​pandas 数据分析和表格处理

`可通过以下命令安装：`

    pip install nibabel numpy pandas
    

## 我们的程序主要分为两部分：
### （第三部分为可选的自动勾画ROI方法，更推荐手动勾画，手动勾画的准确性更高）

### `一、DTI_preprocessing.py ---用于完成DTI数据的预处理`

### 该部分主要是对原始的DTI数据进行处理，包括：
    1. 提取b0图像
    2. 脑提取
    3. 涡流校正
    4. dtifit拟合 用于生成计算指数的tensor文件

### 该部分的输入（文件夹及文件结构）和输出（文件夹及文件结构）如下：
1. 输入：
/Volumes/med_image/ALPS_Liu/DTI_Data/（这只是一个例子具体代表了您的DTI数据保存的文件夹路径，您在使用DTI_preprocessing.py必须替换为自己电脑中DTI数据文件夹的路径，在DTI数据文件夹中，数据必须以这样的方式排列、命名）

#### ├── Subject1/             # 单个受试者/实验的DTI数据文件夹
#### │   ├── DTI.nii    # DTI原始数据（NIfTI文件）
#### │   ├── bvec          # b向量文件
#### │   └── bval          # b值文件

#### ├── Subject2/
#### │   ├── DTI.nii 
#### │   ├── bvec
#### │   └── bval
## ...
2. 输出：
/Volumes/med_image/ALPS_Liu/Result（这也只是一个例子，您需要像这样建立一个结果文件夹，并修改代码DTI_preprocessing.py里的output_dir这个路径，替换为自己电脑的结果文件夹路径）

#### └── Subject1/    # 示例患者文件夹
####     ├── b0_image.nii.gz                   # 原始b0图像
 ####    ├── b0_image_brain.nii.gz             # BET处理后的脑图像
####     ├── b0_image_brain_mask.nii.gz        # 脑组织二值化掩膜
 ####    ├── eddy_corrected_data.nii.gz        # 涡流校正后的DTI数据
####     ├── eddy_corrected_data.ecclog        # 涡流校正日志文件（新增）
   ####  ├── dti_results_FA.nii.gz             # 各向异性分数
  ####   ├── dti_results_L1.nii.gz             # 纵向扩散系数（λ1）
   ####  ├── dti_results_L2.nii.gz             # 横向扩散系数1（λ2）
   ####  ├── dti_results_L3.nii.gz             # 横向扩散系数2（λ3）
   ####  ├── dti_results_MD.nii.gz             # 平均扩散率
   ####  ├── dti_results_MO.nii.gz             # 扩散模式（Mode）
   ####  ├── dti_results_S0.nii.gz             # 基线信号强度
   ####  ├── dti_results_V1.nii.gz             # 主扩散方向向量（x分量）
   ####  ├── dti_results_V2.nii.gz             # 次扩散方向向量（y分量）
  ####   └── dti_results_V3.nii.gz             # 第三扩散方向向量（z分量）

├── Subject2/
## ...

### `二、Calculation_of_ALPS_Index.py ---用于ALPS指标的计算并生成excel表格显示结果`

在这一步中，您首先需要修改代码Calculation_of_ALPS_Index.py里的input_dir这个路径，替换为您电脑的结果文件夹路径

同时您也需要将您手动勾画的左右脑区的投射纤维和关联纤维的ROI保存为NIfTI格式，并将其放置在每一个个体在第一步生成的结果文件夹中。这4个ROI的命名必须为：

    1. 右侧投射纤维：projection_R.nii
    2. 右侧关联纤维：association_R.nii
    3. 左侧投射纤维：projection_L.nii
    4. 左侧关联纤维：association_L.nii

也就是说现在每个个体的结果文件夹中应该有这些文件：
#### └── Subject1/    # 示例患者文件夹
  ####   ├── b0_image.nii.gz                   # 原始b0图像
   ####  ├── b0_image_brain.nii.gz             # BET处理后的脑图像
  ####   ├── b0_image_brain_mask.nii.gz        # 脑组织二值化掩膜
   ####  ├── eddy_corrected_data.nii.gz        # 涡流校正后的DTI数据
   ####  ├── eddy_corrected_data.ecclog        # 涡流校正日志文件（新增）
  ####   ├── dti_results_FA.nii.gz             # 各向异性分数
  ####   ├── dti_results_L1.nii.gz             # 纵向扩散系数（λ1）
   ####  ├── dti_results_L2.nii.gz             # 横向扩散系数1（λ2）
   ####  ├── dti_results_L3.nii.gz             # 横向扩散系数2（λ3）
  ####   ├── dti_results_MD.nii.gz             # 平均扩散率
 ####    ├── dti_results_MO.nii.gz             # 扩散模式（Mode）
  ####   ├── dti_results_S0.nii.gz             # 基线信号强度
  ####   ├── dti_results_V1.nii.gz             # 主扩散方向向量（x分量）
  ####   ├── dti_results_V2.nii.gz             # 次扩散方向向量（y分量）
  ####   └── dti_results_V3.nii.gz             # 第三扩散方向向量（z分量）
  ####   ├── projection_R.nii                 # 右侧投射纤维
  ####   ├── association_R.nii                # 右侧关联纤维
   ####  ├── projection_L.nii                 # 左侧投射纤维
   ####  └── association_L.nii                # 左侧关联纤维

运行程序后即可在结果文件夹中生成一个名为“ALPS_result.xlsx” 的excel表格，表格中显示了每个个体的左右脑区的ALPS指标结果

### `三、Automatically_mapping_ROI.ipynb ---用于显示自动勾画ROI的方法的流程（追求实验的精确性，更推荐手动勾画）`

思路：先将全部个体的b0文件标准化得到每个个体配准到标准空间的转换矩阵trans_average.mat，再将转换矩阵用在每个个体个体空间的FA图像上得到每个个体标准空间的FA，并制作一个群体平均FA图像
在群体空间手动勾画ROI，再映射回每个个体空间

# 引用 ：为贯彻开源精神，请在使用本仓库后对以下论文进行引用
Wang, M., Jiang, X., Nie, B. et al. Association between movement impairments and glymphatic system dysfunction in spastic diplegic cerebral palsy using DTI-ALPS. Neuroradiology (2025). https://doi.org/10.1007/s00234-025-03628-8
