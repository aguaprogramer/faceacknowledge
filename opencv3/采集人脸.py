import cv2
import os
import time


class FaceDataCollector:
    def __init__(self, stu_id, stu_name):
        self.classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.stu_id = stu_id
        self.stu_name = stu_name
        self.count = 0

        # 确保数据存储路径存在
        if not os.path.exists('data'):
            os.makedirs('data')

        # 初始化摄像头
        self.capture = cv2.VideoCapture(0)

    def collect_faces(self):
        while True:
            ret, frame = self.capture.read()

            if not ret:
                print("Failed to grab frame")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            if faces is not None and len(faces) > 0:
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 0, 250), 2)
                    key = cv2.waitKey(1)
                    if key == ord('s'):
                        cv2.imwrite(f'data/{self.stu_name}_{self.stu_id}_{self.count}.jpg', gray[y:y + h, x:x + w])
                        self.count += 1
                        print(f'Collected image number {self.count}')
                    elif key == ord('q'):
                        print(
                            f'Collected a total of images for student ID {self.stu_id} named {self.stu_name}: {self.count}')
                        break
                # 只在检测到人脸时，在最后一个人脸位置显示提示文字
                cv2.putText(frame, 'Press "s" to save', (x + w, y + h), self.font, 1, (200, 0, 250), 2)
            else:
                # 没检测到人脸时，在图像中心位置（示例，可根据实际调整）显示提示文字
                text_x = frame.shape[1] // 2
                text_y = frame.shape[0] // 2
                cv2.putText(frame, 'Press "s" to save', (text_x, text_y), self.font, 1, (200, 0, 250), 2)

            cv2.imshow('Collecting Faces', frame)

            # 把判断退出循环的key判断移到这里，统一处理
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        self.capture.release()
        cv2.destroyAllWindows()


# 使用方式示例
collector = FaceDataCollector(input('输入学号: '), input('输入姓名: '))
start_time = time.perf_counter()
collector.collect_faces()
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"方法调用耗时: {elapsed_time} 秒")