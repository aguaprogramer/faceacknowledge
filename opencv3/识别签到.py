import cv2
import time
import xlrd
import xlwt
from xlutils.copy import copy
from datetime import datetime


class FaceRecognitionSystem:
    def __init__(self, excel_path, classifier_path, trainer_path):
        self.excel_path = excel_path
        self.classifier_path = classifier_path
        self.trainer_path = trainer_path
        self.classfier = cv2.CascadeClassifier(classifier_path)
        self.create = cv2.face_LBPHFaceRecognizer.create()
        self.create.read(trainer_path)
        self.font = cv2.FONT_ITALIC
        self.starttime = time.time()
        self.ID = 'UNKNOW'
        self.name = 'UNKNOW'
        self.count = 0
        self.workbook = xlrd.open_workbook(excel_path)
        self.worksheet = self.workbook.sheet_by_index(0)  # 保存原始的Worksheet对象
        self.stu_id = self.worksheet.col_values(1)
        self.stu_name = self.worksheet.col_values(2)
        self.copied_workbook = copy(self.workbook)

    def sign_in(self, idx, name):
        style0 = xlwt.easyxf('font:height 300,bold on,color_index black', num_format_str='MM:DD HH:MM')
        style1 = xlwt.easyxf('font:height 300,bold on,color_index blue', num_format_str='MM:DD HH:MM')
        wb = xlrd.open_workbook(self.excel_path)
        nwb = copy(wb)
        nbs = nwb.get_sheet(0)
        nbs.write(idx, 4, name, style1)
        nbs.write(idx, 5, datetime.now(), style0)
        nbs.col(4).width = 256 * 20

        # 获取当前学生的学分数据（原有的学分值），使用原始Worksheet对象获取单元格值
        current_credit = None
        try:
            current_credit = float(self.worksheet.cell(idx, 3).value)
        except (IndexError, ValueError):
            print(f"获取学分数据时出错，可能是索引越界或数据格式有误，学生所在行索引为 {idx} 。")

        # 将学分加一（这里假设学分数据是数值类型，如果是其他类型可能需要进一步转换处理）
        if current_credit is not None:
            updated_credit = current_credit + 1
            # 设置学分列的数据格式为数值型
            credit_style = xlwt.easyxf(num_format_str='0')
            nbs.write(idx, 3, updated_credit, credit_style)

        nwb.save(self.excel_path)

    def run(self):
        capture = cv2.VideoCapture(0)
        index = []  # 提前定义index变量，初始化为空列表
        while capture.isOpened():
            kk = cv2.waitKey(1)
            _, frame = capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.classfier.detectMultiScale(gray, 1.2, 5)
            if len(faces)!= 0:
                for x, y, w, h in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (180, 120, 220), 2)
                    gray1 = gray[y:y + h, x:x + w]
                    label, conf = self.create.predict(gray1)
                    print(label, conf)
                    if conf < 50:
                        index = [i for i, item in enumerate(self.stu_id) if item == str(label)]
                        self.ID = str(label)
                        self.name = self.stu_name[index[0]]
                        self.count += 1
                    else:
                        self.ID = 'UNKOWN'
                    cv2.putText(frame, str(self.ID), (x + w // 2 - 50, y + h + 30), self.font, 1.2, (200, 0, 250), 2)

            cv2.putText(frame, 'Press "q" to quit', (30, 60), self.font, 1.2, (200, 0, 250), 2)
            cv2.imshow('picture from capture.', frame)
            if kk == ord('q'):
                break

            if self.count > 30 and index:
                self.sign_in(index[0], self.name)
                print('学号为：' + str(label) + ',姓名为：' + str(self.name))
                break

            if time.time() - self.starttime > 30:
                print('超时未识别')
                break

        capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    frs = FaceRecognitionSystem(r'人脸识别excel.xls', r'D:\python-learning\opencv3\haarcascade_frontalface_default.xml', 'trainer.yml')
    frs.run()