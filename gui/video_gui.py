# -------------------------------------#
#       调用摄像头检测
# -------------------------------------#
from gui.yolo_gui_vedio import YOLO
from PIL import Image
import numpy as np
import cv2
import time
import tensorflow as tf

def vedio():
    gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

    yolo = YOLO()
    # 调用摄像头
    f = open('D:\pythonfile\yolov4-tiny-tf2-master\gui\camsetup\camset.txt', 'r')
    n = f.read()
    capture = cv2.VideoCapture(int(n))  # capture=cv2.VideoCapture("1.mp4")

    fps = 0.0
    t1 = time.time()
    while (True):
        t1 = time.time()
        # 读取某一帧
        ref, frame = capture.read()
        # 格式转变，BGRtoRGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 转变成Image
        frame = Image.fromarray(np.uint8(frame))

        # 进行检测
        frame = np.array(yolo.detect_image(frame))

        # RGBtoBGR满足opencv显示格式
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        fps = (fps + (1. / (time.time() - t1))) / 2
        print("fps= %.2f" % (fps))
        frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        t1 = time.time()
        cv2.imshow("video", frame)
        c = cv2.waitKey(1) & 0xff
        if c == 27:
            capture.release()
            break
    tf.keras.backend.clear_session()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    fp1 = 'D:\pythonfile\yolov4-tiny-tf2-master\model_data\weight.h5'
    fp2 = 'D:\pythonfile\yolov4-tiny-tf2-master\model_data\classes.txt'
    YOLO.update(fp1=fp1, fp2=fp2)
    vedio()
