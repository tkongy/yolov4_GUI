import cv2

def Camera(n=5):
        cam_preset_num = n
        cnt = 0
        useful = []
        for device in range(0, cam_preset_num):
            capture = cv2.VideoCapture(device, cv2.CAP_DSHOW)

            ref, frame = capture.read()
            capture.release()
            if not ref:
                break
            cnt = cnt + 1
            useful.append(str(device))

        return str(cnt), useful
if __name__ == '__main__':
    n1, n2 = Camera()
    print(n2)
    print(n1)
