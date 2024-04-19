import os
import json
import numpy as np
import cv2

folder_path = 'Path/to/json_folder'

for folder, subfolders, files in os.walk(folder_path):
    for file,subfolder in zip(files, subfolders):
        if file.endswith(".json"):
            json_path = os.path.join(folder, file)
            # print(json_path)

            with open(json_path, 'r') as f:
                data = f.read()
            data = json.loads(data)

            points = data["shapes"][0]["points"]
            points = np.array(points,dtype=np.int32)

            dir_path = os.path.join(folder, subfolder)
            # print(dir_path)

            img_path = dir_path + "/" +subfolder.replace("_json","") + "_img.png"
            # print(img_path)

            image = cv2.imread(img_path)
            
            height, width, _ = image.shape
            mask = np.zeros((height,width),dtype=np.uint8)

            pts = points.reshape((-1, 1, 2))

            cv2.fillPoly(mask, [pts], 255)

            mask_path = dir_path + "/" +subfolder.replace("_json","") + "_mask.png"
            # print(mask_path)

            cv2.imwrite(mask_path, mask)
            print(mask_path+" saved")