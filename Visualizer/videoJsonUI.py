import os
import sys
import json
import numpy as np
from PIL import Image, ImageDraw

def i2j(imageFileName, jsonFileName):

    img = Image.open(imageFileName)
    # img = img.resize((1900, 1200))        # resize to change image size if necessary

    draw = ImageDraw.Draw(img)

    # load the json file
    with open(jsonFileName, 'r') as data:
        data_dict = json.load(data)

    imageName = (imageFileName[-7:])[:-4]
    print(imageName)

    kps = []
    for i in data_dict["track"]:
        for itembox in i["shape"]:
            if itembox["frame"] == imageName:
                if itembox["type"] == "box":
                    
                    text = i["label"]
                    x = np.array(itembox["xtl"])
                    y = np.array(itembox["ytl"])
                    w = np.array(itembox["xbr"])
                    h = np.array(itembox["ybr"])

                    # draw bbox and object label on the objects
                    draw.rectangle([(x, y), (w, h)], outline='green', width=2)
                    draw.text([w, h], text, fill ="blue", stroke_width=15)

                if itembox["type"] == "points" and itembox["outside"] == "1":
                    text = i["label"]
                    x  = itembox["points"]
                    # print(x)
                    my_list = [float(item) for item in x.split(',')]
                    kps.append(my_list)

                    # draw key points on the body
                    draw.ellipse((my_list[0], my_list[1], my_list[0] + 8, my_list[1] + 8), fill = (255,255,0) )

    # get the min and max keypoint cordinates
    result = [max(elem) for elem in zip(*kps)]
    print('maximum -> ', result)
    result_new = [min(elem) for elem in zip(*kps)]
    print('minimum -> ', result_new)
    if result != []:
        x_new = np.array(result_new[0]-30)
        y_new = np.array(result_new[1]-100)
        w_new = np.array(result[0]+30)
        h_new = np.array(result[1]+80)

        # draw a bbox on the person
        draw.rectangle([(x_new, y_new), (w_new, h_new)], outline='red', width=4)

    return img, result, result_new