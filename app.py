import tkinter as tk
import tkinter.filedialog as tk_filedialog
import cv2 as cv
from PIL import Image, ImageTk


def select_image_cb():
    global imagePath
    selectImage = tk_filedialog.askopenfilename(title='选择图片', filetypes=[('PNG', '*.png'), ('JPG', '*.jpg')])
    imagePath.set(selectImage)

def analyze_image_cb():
    global container, imageWidth
    global imagePath
    global cannyThereshold1Var, cannyThereshold2Var
    global source_img_tk, sourceImageLabel, result_img_tk, resultImageLabel

    imagePathStr = imagePath.get()
    print('分析中', imagePathStr)

    img = cv.imread(imagePathStr)
    
    img_gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    img_gray_median = cv.medianBlur(img_gray, 9)
    img_gray_bilateral = cv.bilateralFilter(img_gray_median, 9, 150, 150)
    result_img = cv.Canny(img_gray_bilateral, cannyThereshold1Var.get(), cannyThereshold2Var.get())

    source_img_src = Image.fromarray(img)
    source_img_src = source_img_src.resize([imageWidth, int(source_img_src.size[1] / source_img_src.size[0] * imageWidth)])
    source_img_tk = ImageTk.PhotoImage(image=source_img_src)
    sourceImageLabel.config(image=source_img_tk)
    sourceImageLabel.image = source_img_tk

    result_img_src = Image.fromarray(result_img)
    result_img_src = result_img_src.resize([imageWidth, int(result_img_src.size[1] / result_img_src.size[0] * imageWidth)])
    result_img_tk = ImageTk.PhotoImage(image=result_img_src)
    resultImageLabel.config(image=result_img_tk)
    resultImageLabel.image = result_img_tk


def clear_image_cb(val):
    global result_img_tk, resultImageLabel
    result_img_tk = None
    resultImageLabel.config(image=result_img_tk)
    resultImageLabel.image = result_img_tk


def main_fuc():
    global container, imageWidth
    global imagePath
    global cannyThereshold1Var, cannyThereshold2Var
    global source_img_tk, sourceImageLabel, result_img_tk, resultImageLabel

    inputFrame = tk.Frame(container, width=600, pady=20)
    label = tk.Label(inputFrame, text='图片路径', justify='left')
    label.pack(side='left')
    imagePathEntry = tk.Entry(inputFrame, textvariable=imagePath, width=80)
    imagePathEntry.pack(side='left', padx=20)
    selectButton = tk.Button(inputFrame, text='选择图片', command=select_image_cb)
    selectButton.pack(side='left', ipadx=8, ipady=4, padx=4)
    analyzeButton =  tk.Button(inputFrame, text='分析图片', command=analyze_image_cb)
    analyzeButton.pack(side='left', ipadx=8, ipady=4, padx=4)
    inputFrame.pack()

    cannyFrame = tk.Frame(container)
    tk.Label(cannyFrame, text='Canny 参数', justify='left').pack(side='left')
    cannyThereshold1Var = tk.IntVar(value=10)
    cannyThereshold2Var = tk.IntVar(value=20)
    cannyThereshold1Scale = tk.Scale(cannyFrame, variable=cannyThereshold1Var, from_=1, to=200, orient='horizontal', command=clear_image_cb)
    cannyThereshold1Scale.pack(side='left', padx=20)
    cannyThereshold2Scale = tk.Scale(cannyFrame, variable=cannyThereshold2Var, from_=1, to=200, orient='horizontal', command=clear_image_cb)
    cannyThereshold2Scale.pack(side='left', padx=20)
    cannyFrame.pack()

    imageFrame = tk.Frame(container, pady=20)
    sourceImageLabel = tk.Label(imageFrame, image=source_img_tk, width=imageWidth)
    sourceImageLabel.pack(side='left', padx=20)
    resultImageLabel = tk.Label(imageFrame, image=result_img_tk, width=imageWidth)
    resultImageLabel.pack(side='left', padx=20)
    imageFrame.pack()


def get_globalvar_image_path():
    return imagePath

if __name__ == '__main__':
    # 主窗口相关
    window = tk.Tk()                                    # 创建主窗口
    # 设置窗口大小
    winWidth = 1200
    winHeight = 800
    # 获取屏幕分辨率
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    x = int((screenWidth - winWidth) / 2)
    y = int((screenHeight - winHeight) / 2)
    window.title("Tongrang | 螺纹检测 Demo | Whorl Inspection")                   # 设置主窗口标题
    # 设置窗口初始位置在屏幕居中
    window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
    # # 设置窗口图标 TODO 不知道为什么无效
    # window.iconbitmap("./image/icon.ico")
    window.resizable(0, 0)                              # 设置窗口宽高固定

    container = tk.Frame(padx=20, pady=20)
    container.pack()

    # 变量声明
    imagePath = tk.StringVar()
    imagePath.set('/Users/yijun/Downloads/IMG_7844.JPG')
    source_img_tk = None
    result_img_tk = None

    imageWidth = 500

    main_fuc()

    window.mainloop()                                   # 图形界面循环