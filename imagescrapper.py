import os
import json
import pandas as pd
from colorthief import ColorThief

headers = ['IMG_Name','Type','IMG_URL','State', 'Setting','Dominant Color', 'Color_Palette']
rows = []


def extractColors(folder_name, image_path, image_name):
    try:
        if "json" not in image_path:
            state, setting = folder_name.split()
            name, fileType = image_name.split('.')
            row = []
            img = ColorThief(image_path)
            
            row.append(name)
            row.append(fileType)
            row.append(None)
        
            row.append(state)
            row.append(setting)
        
            dominant_color = img.get_color()
            row.append(dominant_color)

            #default of color palette is 10 colors
            palette_color = img.get_palette(color_count=5)
            row.append(palette_color)
            rows.append(row)
        else:
            if len(rows) == 0:
                return
            if rows[-1][0] == image_name.split('.')[0]:
                json_file = open(image_path)
                data = json.load(json_file)
                row = rows[-1]
                row[2] = data['url']
    except:
        raise Exception("Error occurred")

parent_folder_path = os.getcwd()

for f in os.listdir(parent_folder_path):
    if os.path.isdir(os.path.join(parent_folder_path,f)):
        #ignore folders that start with . e.g. .git
        if f[0] != '.':
            curr_folder_path = os.path.join(parent_folder_path,f)
            for file in os.listdir(curr_folder_path):
                filePath = os.path.join(curr_folder_path, file)
                #uncomment below if want to see current folder and file
                # print(f"folder name: {f}\nimage path: {filePath}\nimage name: {file}")
                extractColors(f, filePath, file)


table = pd.DataFrame(rows, columns=headers)

table.to_csv('States_images.csv', index=False)