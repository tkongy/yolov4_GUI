from gui.yolo_gui import  YOLO
from PIL import Image
import tensorflow as tf
import os

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
def runimage(fn):
    yolo = YOLO()
    image = Image.open(fn)
    r_image = yolo.detect_image(image)
    #filename, extension = os.path.splitext(fn)
    #newfn = filename+'_out'+extension
    filepath, filename = os.path.split(fn)
    filename, extension = os.path.splitext(filename)
    newfn = 'D:\pythonfile\yolov4-tiny-tf2-master\gui\outimage\\'+filename+'_out'+extension
    r_image.save(newfn)
    return newfn

