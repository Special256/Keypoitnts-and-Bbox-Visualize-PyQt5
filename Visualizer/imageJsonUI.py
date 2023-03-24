import os
import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QMovie
from videoJsonUI import i2j
from PIL.ImageQt import ImageQt
from PIL import Image
import json
import numpy as np

folderPath = os.getcwd()         # path to folder with images

def visualizer():

    # create the instance of QApplication
    app = QApplication([])

    # creating the application’s GUI.
    window = QWidget()
    
    # .setWindowTitle() sets the window’s title in your application
    window.setWindowTitle("Tool to display keypoints and bounding boxes in images")
    
    # .setGeometry() to define the window’s size and screen position. 
    # The first two arguments are the x and y screen coordinates where the window will 
    # be placed. The third and fourth arguments are the window’s width and height.
    #window.setGeometry(100,100,1920,1080)

    imgLabel = QLabel()
    imgLabel.setFixedHeight(640)
    imgLabel.setFixedWidth(960)
    imgLabel.setScaledContents(True)
    imgLabel.setStyleSheet("border: 2px solid grey;")

    contents = QTextEdit()

    def getImage(fileNames):
        for i in fileNames:
            pixmap = QPixmap(i)
            imgLabel.setPixmap(pixmap)
        
        return fileNames[0]

    def getJsons(filenames):
        with open(filenames[0], 'r') as f:
            data = f.read()
            contents.setText(data)

            return filenames[0]

    def getImageFiles():
        global returnedImage
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("Images (*.png *.jpg)")
        dialog.setViewMode(QFileDialog.Detail)

        if dialog.exec():
            fileNames = dialog.selectedFiles()
            returnedImage = getImage(fileNames)
            print('image -> ', returnedImage )

    def getJsonFiles():
        global returnedJson
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("Json files (*.json)")
        dlg.setViewMode(QFileDialog.Detail)

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            returnedJson = getJsons(filenames)

            print('json -> ', returnedJson)
    
    def loadImgFiles():
        getImageFiles()
        
    def loadJsonFiles():
        getJsonFiles()
        
    def drawer():
        global returnedImage
        global returnedJson
        global j
        
        if returnedImage:
            try:
                print('image -> ', returnedImage )
                newImage, maximum_kps, minimun_kps = i2j(returnedImage, returnedJson)
                print("new image -> ", newImage)
                print("max kps -> ", maximum_kps[0])
                print("min kps -> ", minimun_kps[0])
                
                # convert the PIL image to numpy array
                im = np.asarray(newImage)
                im2 = np.require(im, np.uint8, 'c')

                # convert numpy array to QImage
                qimg = QImage(im2, 1920, 1080, QImage.Format_RGB888)

                pixmap = QPixmap(qimg)
                imgLabel.setPixmap(pixmap)
            except ValueError as e:
                print("No image selected")
                
    def openDir():
        global list_of_images
        global folderPath
        global input_img_raw_string
        global j
        global returnedImage
        print(folderPath)
        folderPath = QFileDialog.getExistingDirectory()        
        
        #get the list of images in the folder and sort them
        list_of_images = os.listdir(folderPath)
        list_of_images = sorted(list_of_images)

        #print length of images
        print("Number of images in the selected folder -> {}".format(len(list_of_images)) )
        input_img_raw_string = '{}/{}'.format(folderPath, list_of_images[0])
        
        returnedImage = input_img_raw_string
        
        #show first image in the same window
        pixmap = QPixmap(input_img_raw_string)
        imgLabel.setPixmap(pixmap)
        j = 0
        
    def nextImage():
        global list_of_images
        global folderPath
        global j
        global returnedImage
        print(folderPath)
        if list_of_images:
            if j < len(list_of_images)-1:
                j += 1
                input_img_raw_string = '{}/{}'.format(folderPath, list_of_images[j])
                returnedImage = input_img_raw_string
                pixmap = QPixmap(input_img_raw_string)
                imgLabel.setPixmap(pixmap)
                print("Next image -> {}".format(list_of_images[j]))
            else:
                print("No more images")

        else:
            print("No folder selected")
    
    def prevImage():
        global list_of_images
        global folderPath
        global j
        global returnedImage
        if list_of_images:
            if j > 0:
                j -= 1
                input_img_raw_string = '{}/{}'.format(folderPath, list_of_images[j])
                returnedImage = input_img_raw_string
                pixmap = QPixmap(input_img_raw_string)
                imgLabel.setPixmap(pixmap)
                print("Previous image -> {}".format(list_of_images[j]))
            else:
                print("No more images")
        else:
             print("No folder selected")
             
    # create layouts
    
    imgBtn = QPushButton("Load Image Folder")
    imgBtn.setStyleSheet("background-color: skyblue; color : black; font: bold 20px; border: 1px solid grey;")
    imgBtn.clicked.connect(openDir)
    imgBtn.resize(imgBtn.sizeHint())
    imgBtn.setFixedHeight(30)
    imgBtn.setFixedWidth(250)
    
    nxtBtn = QPushButton("Next Image")
    nxtBtn.setStyleSheet("background-color: lightgrey; color : black; font: bold 20px; border: 1px solid grey;")
    nxtBtn.clicked.connect(nextImage)
    nxtBtn.resize(nxtBtn.sizeHint())
    nxtBtn.setFixedHeight(30)
    nxtBtn.setFixedWidth(200)

    prevBtn = QPushButton("Previous Image")
    prevBtn.setStyleSheet("background-color: lightgrey; color : black; font: bold 20px; border: 1px solid grey;")
    prevBtn.clicked.connect(prevImage)
    prevBtn.resize(nxtBtn.sizeHint())
    prevBtn.setFixedHeight(30)
    prevBtn.setFixedWidth(200)
    
    loadImgBtn = QPushButton("Load Single Image")
    loadImgBtn.setStyleSheet("background-color: skyblue; font: bold 20px; border: 1px solid grey;")
    loadImgBtn.clicked.connect(loadImgFiles)
    loadImgBtn.resize(loadImgBtn.sizeHint())
    loadImgBtn.setFixedHeight(30)
    loadImgBtn.setFixedWidth(250)
    
    loadJsonBtn = QPushButton("Load Json")
    loadJsonBtn.setStyleSheet("background-color: skyblue; font: bold 20px; border: 1px solid grey;")
    loadJsonBtn.clicked.connect(loadJsonFiles)
    loadJsonBtn.resize(loadJsonBtn.sizeHint())
    loadJsonBtn.setFixedHeight(30)
    loadJsonBtn.setFixedWidth(200)
    
    drawBtn = QPushButton("Click to draw keypoints and bbox")
    drawBtn.setShortcut('Ctrl+D')
    drawBtn.setStyleSheet("background-color: grey; font: bold 20px; border: 1px solid grey;")
    drawBtn.clicked.connect(drawer)
    drawBtn.resize(drawBtn.sizeHint())
    drawBtn.setFixedHeight(30)
    drawBtn.setFixedWidth(400) 

    event_start = QLineEdit()
    event_start.setStyleSheet("background-color: white; color : black; font: bold 15px; border: 1px solid grey;")
    event_start.setFixedHeight(30)
    event_start.setFixedWidth(100)
    event_start.setPlaceholderText("Event Start")
    
    event_end = QLineEdit()
    event_end.setStyleSheet("background-color: white; color : black; font: bold 15px; border: 1px solid grey;")
    event_end.setFixedHeight(30)
    event_end.setFixedWidth(100)
    event_end.setPlaceholderText("Event End")
    
    eventLayout = QHBoxLayout()
    eventLayout.addWidget(event_start)
    eventLayout.addWidget(event_end)
    
    min_x_label = QLabel('Min X :')
    min_x_label.setAlignment(QtCore.Qt.AlignRight)
    min_x_label.setStyleSheet("QLabel { color : black; font: bold 15px;}")
    min_x_value = QLabel('')
    min_x_value.setAlignment(QtCore.Qt.AlignLeft)
    min_x_value.setStyleSheet("QLabel { background-color : lightgrey; color : black; font: bold 15px;}")
    min_y_label = QLabel('Min Y :')
    min_y_label.setAlignment(QtCore.Qt.AlignRight)
    min_y_label.setStyleSheet("QLabel { color : black; font: bold 15px;}")
    min_y_value = QLabel('')
    min_y_value.setAlignment(QtCore.Qt.AlignLeft)
    min_y_value.setStyleSheet("QLabel { background-color : lightgrey; color : black; font: bold 15px;}")
    max_x_label = QLabel('Max X :')
    max_x_label.setAlignment(QtCore.Qt.AlignRight)
    max_x_label.setStyleSheet("QLabel { color : black; font: bold 15px;}")
    max_x_value = QLabel('')
    max_x_value.setAlignment(QtCore.Qt.AlignLeft)
    max_x_value.setStyleSheet("QLabel { background-color : lightgrey; color : black; font: bold 15px;}")
    max_y_label = QLabel('Max Y :')
    max_y_label.setAlignment(QtCore.Qt.AlignRight)
    max_y_label.setStyleSheet("QLabel { color : black; font: bold 15px;}")
    max_y_value = QLabel('')
    max_y_value.setAlignment(QtCore.Qt.AlignLeft)
    max_y_value.setStyleSheet("QLabel { background-color : lightgrey; color : black; font: bold 15px;}")

    bbox_layout = QGridLayout()
    bbox_layout.addWidget(min_x_label, 0, 0)
    bbox_layout.addWidget(min_x_value, 0, 1)
    bbox_layout.addWidget(min_y_label, 0, 2)
    bbox_layout.addWidget(min_y_value, 0, 3)
    bbox_layout.addWidget(max_x_label, 0, 4)
    bbox_layout.addWidget(max_x_value, 0, 5)
    bbox_layout.addWidget(max_y_label, 0, 6)
    bbox_layout.addWidget(max_y_value, 0, 7)

    btn_layout = QHBoxLayout()
    btn_layout.addWidget(prevBtn)
    btn_layout.addWidget(drawBtn)
    btn_layout.addWidget(nxtBtn)
    
    button_layout = QHBoxLayout()
    button_layout.addWidget(loadImgBtn)
    button_layout.addWidget(imgBtn)    
    
    boxLayout = QVBoxLayout()
    boxLayout.addLayout(button_layout)
    boxLayout.addWidget(imgLabel)
    boxLayout.addLayout(btn_layout)
    boxLayout.addLayout(bbox_layout)
    boxLayout.addLayout(eventLayout)
    boxLayout.addWidget(loadJsonBtn)
    boxLayout.addWidget(contents)
    boxLayout.setAlignment(QtCore.Qt.AlignCenter)
    
    window.setStyleSheet("background-color: aliceblue;")
    window.setFixedWidth(985)
    window.setLayout(boxLayout)
    window.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    visualizer()