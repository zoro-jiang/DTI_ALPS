import os
import subprocess
import pandas as pd
input_path = "/Volumes/med_image/ALPS_Liu/Result"

all_subjects = os.listdir(input_path)
excel_data = []
for subject in all_subjects:
    subject_path = os.path.join(input_path, subject)
    try:
        dti_tensor_file = os.path.join(subject_path, 'dti_results_tensor.nii.gz')
        roi_tousheR = os.path.join(subject_path, 'projection_R.nii')
        roi_lianheR = os.path.join(subject_path, 'association_R.nii')
        roi_tousheL = os.path.join(subject_path, 'projection_L.nii')
        roi_lianheL = os.path.join(subject_path, 'association_L.nii')
        
        Dxx_file = os.path.join(subject_path, 'Dxx.nii.gz')
        Dyy_file = os.path.join(subject_path, 'Dyy.nii.gz')
        Dzz_file = os.path.join(subject_path, 'Dzz.nii.gz')
        
        # 1.提取Dxx、Dyy、Dzz
        subprocess.run(["fslroi", dti_tensor_file, Dxx_file, "0", "1"], check=True)
        subprocess.run(["fslroi", dti_tensor_file, Dyy_file, "3", "1"], check=True)
        subprocess.run(["fslroi", dti_tensor_file, Dzz_file, "5", "1"], check=True)
        
        # 2.计算右侧ROI的ALPS值
        a = subprocess.check_output(["fslstats", Dxx_file, "-k", roi_tousheR, "-M"]).decode('utf-8').strip()
        b = subprocess.check_output(["fslstats", Dxx_file, "-k", roi_lianheR, "-M"]).decode('utf-8').strip()
        c = subprocess.check_output(["fslstats", Dyy_file, "-k", roi_tousheR, "-M"]).decode('utf-8').strip()
        d = subprocess.check_output(["fslstats", Dzz_file, "-k", roi_lianheR, "-M"]).decode('utf-8').strip()
        resultR = (float(a) + float(b)) / (float(c) + float(d))
        
        # 3. 计算左侧ROI的ALPS值
        q = subprocess.check_output(["fslstats", Dxx_file, "-k", roi_tousheL, "-M"]).decode('utf-8').strip()
        w = subprocess.check_output(["fslstats", Dxx_file, "-k", roi_lianheL, "-M"]).decode('utf-8').strip()
        e = subprocess.check_output(["fslstats", Dyy_file, "-k", roi_tousheL, "-M"]).decode('utf-8').strip()
        r = subprocess.check_output(["fslstats", Dzz_file, "-k", roi_lianheL, "-M"]).decode('utf-8').strip()
        resultL = (float(q) + float(w)) / (float(e) + float(r))
        
        # 将结果加入excel列表
        excel_data.append([subject, resultL, resultR])
        print(f"处理完毕：{subject}")
    except Exception as e:
        print(f"处理:{subject}时出错:{e}")
print("批处理完成！")
# 将数据写入Excel文件
df = pd.DataFrame(excel_data, columns=['被试名', '左侧ALPS', '右侧ALPS'])
excel_output_path = os.path.join(input_path,'ALPS_result.xlsx')
df.to_excel(excel_output_path, index=False) 