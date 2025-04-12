import os
import subprocess
from glob import glob

dti_folders_path = "/Volumes/med_image/ALPS_Liu/DTI_Data"
output_dir = "/Volumes/med_image/ALPS_Liu/Result"

# 获取所有子目录
dti_folders = [f.path for f in os.scandir(dti_folders_path) if f.is_dir()]



for dti_folder in dti_folders:
    # 获取文件夹名称
    result_folder = os.path.basename(os.path.normpath(dti_folder))
    # 创建输出文件夹
    current_output_dir = os.path.join(output_dir, result_folder)
    os.makedirs(current_output_dir, exist_ok=True)
    
    # 查找文件
    dti_files = glob(os.path.join(dti_folder, "DTI.nii")) 
    if len(dti_files) != 1:
        print(f"Error: 找到 {len(dti_files)} 个DTI文件于 {dti_folder}")
        continue
    dti_file = dti_files[0]
    
    bval_files = glob(os.path.join(dti_folder, "bval"))
    if len(bval_files) != 1:
        print(f"Error: 找不到或找到多个bval文件在 {dti_folder}")
        continue
    bval_file = bval_files[0]
    
    bvec_files = glob(os.path.join(dti_folder, "bvec"))
    if len(bvec_files) != 1:
        print(f"Error: 找不到或找到多个bvec文件在 {dti_folder}")
        continue
    bvec_file = bvec_files[0]
    
    # 步骤1: 提取b0图像
    b0_path = os.path.join(current_output_dir, "b0_image.nii.gz")
    cmd_fslroi = ["fslroi", dti_file, b0_path, "0", "1"]
    subprocess.run(cmd_fslroi, check=True)
    
    # 步骤2: 脑提取
    b0_brain_path = os.path.join(current_output_dir, "b0_image_brain.nii.gz")
    cmd_bet = ["bet", b0_path, b0_brain_path, "-m"]
    subprocess.run(cmd_bet, check=True)
    
    # 步骤3: 涡流校正
    eddy_corrected_path = os.path.join(current_output_dir, "eddy_corrected_data.nii.gz")
    cmd_eddy = ["eddy_correct", dti_file, eddy_corrected_path, "0"]
    subprocess.run(cmd_eddy, check=True)
    
    # 步骤4: DTI拟合
    cmd_dtifit = [
        "dtifit",
        "-k", eddy_corrected_path,
        "-o", os.path.join(current_output_dir, "dti_results"),
        "-m", os.path.join(current_output_dir, "b0_image_brain_mask.nii.gz"),
        "-r", bvec_file,
        "-b", bval_file,
        "--save_tensor"
    ]
    subprocess.run(cmd_dtifit, check=True)
    
    print(f"处理完毕：{result_folder}")

print("批处理完成！")