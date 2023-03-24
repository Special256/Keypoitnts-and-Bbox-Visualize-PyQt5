# Keypoitnts-and-Bbox-Visualizer-PyQt5
In this repository, I use PyQt5 to visualize the key-points and bbox coordinates by mapping the json file to the images in a directory.

  -> The purpose behind this project was to be able to create bbox grount truth for the task of object detection in cases where the 
  available data set only has key-point attributes. Using the skeleton key-points, we were able to draw bbox that can be used for object detection.
The json file is from the NIA dataset for human activity recognition in unmanned retails, I uploaded a sample with an image.

To try on your dataset; please change some variables in the 'videoJsonUI.py' file to fit your own.

TO DO LIST:
  1. make the event start and event end functions sunctionable
  2. min X, min Y, max X, max Y should be able to automatically show for every image
  3. better the UI, suggestions are welcome.
  4. add saving option, to save bbox cordinates for every object in the image.
