import os
import json
import pandas as pd
from colorthief import ColorThief

headers = ['IMG_Name','IMG_URL','State', 'Setting','Dominant Color', 'Color_Palette']
rows = []


def extractColors(folder_name, image_path, image_name):
    print(image_path)
    if "json" not in image_path:
        state, setting = folder_name.split()
        row = []
        img = ColorThief(image_path)
        row.append(image_name)
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
        json_file = open(image_path)
        data = json.load(json_file)
        print(data)
        row = rows[-1]
        row[1] = data['url']

parent_folder_path = os.getcwd()

for f in os.listdir(parent_folder_path):
    if os.path.isdir(os.path.join(parent_folder_path,f)):
        curr_folder_path = os.path.join(parent_folder_path,f)
        for file in os.listdir(curr_folder_path):
            filePath = os.path.join(curr_folder_path, file)
            extractColors(f, filePath, file)


table = pd.DataFrame(rows, columns=headers)

table.to_csv('States_images.csv', index=False)