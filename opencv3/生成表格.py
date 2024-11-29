import xlwt
import time
from xlutils.copy import copy

class ExcelManager:
    def __init__(self, filename='人脸识别excel.xls'):
        self.workbook = xlwt.Workbook()
        self.sheet = self.workbook.add_sheet('成绩表')
        self.filename = filename

    def setup_header(self):
        header_row = ['序号','学号', '姓名', '学分','签名', '签到时间']
        self.sheet.write_merge(0, 0, 0, 5, '成绩表')
        for col_index, header in enumerate(header_row):
            self.sheet.write(1, col_index, header)

    def write_data(self, students_info):
        row_start = 2
        for index, (student_id, name) in enumerate(students_info.items(), start=row_start):
            self.sheet.write(index, 0, index - 1)
            self.sheet.write(index, 1, student_id)
            self.sheet.write(index, 2, name)
            style = xlwt.easyxf(num_format_str='0')
            self.sheet.write(index, 3, 0, style)


    def save_file(self):
        self.workbook.save(self.filename)


# 数据字典，key 是学号，value 是姓名
students_info = {"1": "a", "2": "b", "3": "c", "4": "d"}

# 使用示例
manager = ExcelManager()

manager.setup_header()
manager.write_data(students_info)
manager.save_file()