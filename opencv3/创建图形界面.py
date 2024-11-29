import tkinter as tk
import os
from PIL import Image, ImageTk


class FaceRecognitionSystem:
    def __init__(self):
        # 创建窗口
        self.win = tk.Tk()
        self.win.title('人脸识别签到系统')
        self.win.geometry('310x500+800+50')
        self.win.configure(bg='#ffffff')
        tk.Label(self.win, text="自动化人脸识别", font=('黑体', 20, 'bold'), bg='#00BFFF', fg='white').place(x=10, y=10)

        # 设置图片以便使用，添加图片尺寸调整逻辑
        try:
            img = Image.open(r'D:\python-learning\opencv3\jishi.jpg')
            # 获取原始图片的宽和高
            original_width, original_height = img.size
            # 定义缩小后的尺寸，这里可以根据实际需求调整，例如宽度设置为200像素，高度按比例缩放
            new_width = 200
            new_height = int(original_height * (new_width / original_width))
            # 对图片进行尺寸调整
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            print("图片文件未找到，请检查路径是否正确！")
            self.photo = None

        self.create_widgets()

    def create_widgets(self):
        # 大标题相关标签设置
        lab1 = tk.Label(self.win, text="自动化人脸识别", font=('黑体', 20, 'bold'), bg='#00BFFF', fg='white')
        lab1.grid(padx=20, pady=10, sticky=tk.W + tk.E)

        if self.photo:
            lab2 = tk.Label(self.win, image=self.photo)
            lab2.grid(padx=20, pady=10, sticky=tk.W + tk.E)

        # 各个功能按钮创建
        but1 = tk.Button(self.win, text='采 集 人 脸 图 片', activebackground='yellow', command=self.CJRL,
                         font=('黑体', 10, 'bold'), bg='#00BFFF', fg='white')
        but1.grid(padx=20, pady=10, sticky=tk.W + tk.E)

        but2 = tk.Button(self.win, text='训 练 模 型', activebackground='yellow', command=self.XL,
                         font=('黑体', 10, 'bold'), bg='#00BFFF', fg='white')
        but2.grid(padx=20, pady=10, sticky=tk.W + tk.E)

        but3 = tk.Button(self.win, text='识 别 签 到', activebackground='yellow', command=self.SBQD,
                         font=('黑体', 10, 'bold'), bg='#00BFFF', fg='white')
        but3.grid(padx=20, pady=10, sticky=tk.W + tk.E)

        but4 = tk.Button(self.win, text='签 到 表', activebackground='yellow', command=self.QDB,
                         font=('黑体', 10, 'bold'), bg='#00BFFF', fg='white')
        but4.grid(padx=20, pady=10, sticky=tk.W + tk.E)

        but5 = tk.Button(self.win, text='关 闭 窗 口', activebackground='yellow', command=self.GB,
                         font=('黑体', 10, 'bold'), bg='#00BFFF', fg='white')
        but5.grid(padx=20, pady=10, sticky=tk.W + tk.E)

    def CJRL(self):
        """采集人脸子函数"""
        os.system('python 采集人脸.py')

    def XL(self):
        """训练模型子函数"""
        os.system('python 训练模型.py')

    def SBQD(self):
        """识别签到子函数"""
        os.system('python 识别签到.py')

    def QDB(self):
        """创建签到表"""
        os.startfile('人脸识别excel.xls')

    def GB(self):
        """关闭窗口"""
        self.win.destroy()

    def run(self):
        """启动主循环，显示窗口"""
        self.win.mainloop()


if __name__ == "__main__":
    app = FaceRecognitionSystem()
    app.run()
