import cv2
import numpy as np
from PIL import Image
import os
import time

class FaceTrainer:
    def __init__(self, path):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.path = path

    def _load_images_and_labels(self):
        face_samples = []
        ids = []

        files = [os.path.join(self.path, f) for f in os.listdir(self.path)]
        for file_path in files:
            img_pil = Image.open(file_path).convert('L')
            img_np = np.array(img_pil, 'uint8')
            label = int(os.path.splitext(os.path.basename(file_path))[0].split('_')[1])  # 根据实际文件命名方式解析标签
            face_samples.append(img_np)
            ids.append(label)

        return face_samples, np.array(ids)

    def train_model(self):
        print('训练中')
        faces, labels = self._load_images_and_labels()
        self.recognizer.train(faces, labels)
        self.recognizer.save('trainer.yml')
        print('训练完成')


# 使用示例
if __name__ == '__main__':
    trainer = FaceTrainer(r'D:\python-learning\opencv3\data')
    start_time=time.perf_counter()
    trainer.train_model()
    end_time=time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"方法调用耗时: {elapsed_time} 秒")