import tkinter as tk
import tkinter.filedialog as tk_filedialog
import cv2 as cv
from PIL import Image, ImageTk

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def select_image_cb():
    global imagePath, source_img_tk, sourceImageCanvas
    selectImage = tk_filedialog.askopenfilename(title='选择图片', filetypes=[('PNG', '*.png'), ('JPG', '*.jpg'), ('BMP', '*.bmp')])
    imagePath.set(selectImage)

    imagePathStr = imagePath.get()
    print('选择图片：', imagePathStr)

    img = cv.imread(imagePathStr)
    source_img_src = Image.fromarray(img)
    currentSourceWidth = int(source_img_src.size[0] / source_img_src.size[1] * imageHeight)
    currentSourceHeight = int(source_img_src.size[1] / source_img_src.size[0] * imageWidth)
    # source_img_src = source_img_src.resize([imageWidth, currentSourceHeight])
    source_img_src = source_img_src.resize([currentSourceWidth, imageHeight])
    source_img_tk = ImageTk.PhotoImage(image=source_img_src)
    # sourceImageCanvas.config(height=currentSourceHeight)
    sourceImageCanvas.config(width=currentSourceWidth)
    # sourceImageCanvas.create_image((imageWidth/2, currentSourceHeight/2), image=source_img_tk)
    sourceImageCanvas.create_image((currentSourceWidth/2, imageHeight/2), image=source_img_tk)

def analyze_image_cb():
    global container, imageWidth
    global imagePath
    global medianBlurVar_N, bilaterFilterVar_d, bilaterFilterVar_sigmaColor, bilaterFilterVar_sigmaSpace, cannyThereshold1Var, cannyThereshold2Var
    global source_img_tk, sourceImageCanvas, result_img_tk, resultImageCanvas, result_img

    imagePathStr = imagePath.get()
    print('边缘检测中', imagePathStr)

    img = cv.imread(imagePathStr)
    
    img_gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    img_gray_blur = img_gray
    img_gray_blur = cv.medianBlur(img_gray, medianBlurVar_N.get())
    img_gray_bilateral = cv.bilateralFilter(img_gray_blur, bilaterFilterVar_d.get(), bilaterFilterVar_sigmaColor.get(), bilaterFilterVar_sigmaSpace.get())
    result_img = cv.Canny(img_gray_bilateral, cannyThereshold1Var.get(), cannyThereshold2Var.get())

    source_img_src = Image.fromarray(img)
    currentSourceWidth = int(source_img_src.size[0] / source_img_src.size[1] * imageHeight)
    currentSourceHeight = int(source_img_src.size[1] / source_img_src.size[0] * imageWidth)
    # source_img_src = source_img_src.resize([imageWidth, currentSourceHeight])
    source_img_src = source_img_src.resize([currentSourceWidth, imageHeight])
    source_img_tk = ImageTk.PhotoImage(image=source_img_src)
    # sourceImageCanvas.config(height=currentSourceHeight)
    sourceImageCanvas.config(width=currentSourceWidth)
    # sourceImageCanvas.create_image((imageWidth/2, currentSourceHeight/2), image=source_img_tk)
    sourceImageCanvas.create_image((currentSourceWidth/2, imageHeight/2), image=source_img_tk)

    result_img_src = Image.fromarray(result_img)
    currentResultWidth = int(result_img_src.size[0] / result_img_src.size[1] * imageHeight)
    currentResultHeight = int(result_img_src.size[1] / result_img_src.size[0] * imageWidth)
    # result_img_src = result_img_src.resize([imageWidth, currentResultHeight])
    result_img_src = result_img_src.resize([currentResultWidth, imageHeight])
    result_img_tk = ImageTk.PhotoImage(image=result_img_src)
    # resultImageCanvas.config(height=currentResultHeight)
    resultImageCanvas.config(width=currentResultWidth)
    # resultImageCanvas.create_image((imageWidth/2, currentResultHeight/2), image=result_img_tk)
    resultImageCanvas.create_image((currentResultWidth/2, imageHeight/2), image=result_img_tk)

    print('analyze_image_cb: %s' % result_img)


def clear_image_cb(val):
    global result_img_tk, resultImageCanvas
    result_img_tk = None
    # resultImageCanvas

def clear_image_cb_medianBlurVar_N(val):
    global result_img_tk, resultImageCanvas
    result_img_tk = None
    if int(val) % 2 == 0:
        medianBlurScale_n.set(int(val) + 1)

def clear_image_cb_bilaterFilterVar_d(val):
    global result_img_tk, resultImageCanvas
    result_img_tk = None
    if int(val) % 2 == 0:
        bilaterFilterScale_d.set(int(val) + 1)

def collect_images_from_live_camera(val):
    print('Collect Images from Live Camera')


def image_preprocessing():
    global imagePath, source_img_tk, sourceImageCanvas, result_img_tk, resultImageCanvas, result_img
    global medianBlurVar_N, bilaterFilterVar_d, bilaterFilterVar_sigmaColor, bilaterFilterVar_sigmaSpace, cannyThereshold1Var, cannyThereshold2Var

    imagePreprocessingFrame = tk.Frame(container, padx=20, pady=20, bg='#efefef')
    imagePreprocessingFrame.grid(column=0, row=0, sticky=tk.NW)

    imagePreprocessingFrame_L = tk.Frame(imagePreprocessingFrame, padx=20, pady=20)
    imagePreprocessingFrame_L.grid(column=0, row=0, sticky=tk.NW)
    imagePreprocessingFrame_C = tk.Frame(imagePreprocessingFrame, padx=20, pady=20)
    imagePreprocessingFrame_C.grid(column=1, row=0, sticky=tk.NW)
    imagePreprocessingFrame_R = tk.Frame(imagePreprocessingFrame, padx=20, pady=20)
    imagePreprocessingFrame_R.grid(column=2, row=0, sticky=tk.NW)
    
    
    # imagePreprocessingFrame_L
    colBtn = tk.Button(imagePreprocessingFrame_L, text='采集摄像头图片(暂无)', command=collect_images_from_live_camera)
    selBtn = tk.Button(imagePreprocessingFrame_L, text='选择本地图片', command=select_image_cb)
    colBtn.grid(column=0, row=0, **btnProps)
    selBtn.grid(column=1, row=0, **btnProps)

    imagePathEntry = tk.Entry(imagePreprocessingFrame_L, textvariable=imagePath, width=28, state='disabled')
    imagePathEntry.grid(column=0, row=1, sticky=tk.NW, columnspan=2)

    sourceImageCanvas = tk.Canvas(imagePreprocessingFrame_L, width=imageWidth, height=imageHeight, bg='blue')
    sourceImageCanvas.grid(column=0, row=2, sticky=tk.NW, columnspan=2)


    # imagePreprocessingFrame_C
    medianBlurRow, bilaterFilterRow, cannyTheresholdRow = 0, 1, 2
    
    # medianBlur
    medianBlurVar_N = tk.IntVar(value=9)
    medianBlurLf = tk.LabelFrame(imagePreprocessingFrame_C, text='中值滤波', padx=8, pady=0)
    medianBlurLf.grid(column=0, row=medianBlurRow, sticky=tk.NW)
    # medianBlur_Layout
    tk.Label(medianBlurLf, text='卷积核 N', justify='left').grid(column=0, row=0, sticky=tk.W)
    global medianBlurScale_n
    medianBlurScale_n = tk.Scale(medianBlurLf, variable=medianBlurVar_N, from_=1, to=99, orient='horizontal', command=clear_image_cb_medianBlurVar_N)
    medianBlurScale_n.grid(column=1, row=0, sticky=tk.W)

    # bilaterFilter
    bilaterFilterVar_d, bilaterFilterVar_sigmaColor, bilaterFilterVar_sigmaSpace = tk.IntVar(value=9), tk.IntVar(value=150), tk.IntVar(value=150)
    bilaterFilterLf = tk.LabelFrame(imagePreprocessingFrame_C, text='双边滤波', padx=8, pady=0)
    bilaterFilterLf.grid(column=0, row=bilaterFilterRow, sticky=tk.NW)
    # bilaterFilter_Layout
    tk.Label(bilaterFilterLf, text='模板大小 d', justify='left').grid(column=0, row=0, sticky=tk.W)
    global bilaterFilterScale_d
    bilaterFilterScale_d = tk.Scale(bilaterFilterLf, variable=bilaterFilterVar_d, from_=1, to=99, orient='horizontal', command=clear_image_cb_bilaterFilterVar_d)
    bilaterFilterScale_d.grid(column=1, row=0, sticky=tk.W)
    tk.Label(bilaterFilterLf, text='颜色空间滤波标准差 sigmaColor', justify='left').grid(column=0, row=1, sticky=tk.W)
    bilaterFilterScale_sigmaColor = tk.Scale(bilaterFilterLf, variable=bilaterFilterVar_sigmaColor, from_=1, to=200, orient='horizontal', command=clear_image_cb)
    bilaterFilterScale_sigmaColor.grid(column=1, row=1, sticky=tk.W)
    tk.Label(bilaterFilterLf, text='空间坐标滤波标准差 sigmaSpace', justify='left').grid(column=0, row=2, sticky=tk.W)
    bilaterFilterScale_sigmaSpace = tk.Scale(bilaterFilterLf, variable=bilaterFilterVar_sigmaSpace, from_=1, to=200, orient='horizontal', command=clear_image_cb)
    bilaterFilterScale_sigmaSpace.grid(column=1, row=2, sticky=tk.W)

    # canny
    cannyThereshold1Var, cannyThereshold2Var = tk.IntVar(value=10), tk.IntVar(value=20)
    cannyLf = tk.LabelFrame(imagePreprocessingFrame_C, text='Canny', padx=8, pady=0)
    cannyLf.grid(column=0, row=cannyTheresholdRow, sticky=tk.NW)
    # canny_Layout
    tk.Label(cannyLf, text='较小阈值 minVal', justify='left').grid(column=0, row=0, sticky=tk.W)
    cannyThereshold1Scale = tk.Scale(cannyLf, variable=cannyThereshold1Var, from_=1, to=200, orient='horizontal', command=clear_image_cb)
    cannyThereshold1Scale.grid(column=1, row=0, sticky=tk.W)
    tk.Label(cannyLf, text='较大阈值 maxVal', justify='left').grid(column=0, row=1, sticky=tk.W)
    cannyThereshold2Scale = tk.Scale(cannyLf, variable=cannyThereshold2Var, from_=1, to=200, orient='horizontal', command=clear_image_cb)
    cannyThereshold2Scale.grid(column=1, row=1, sticky=tk.W)

    # imagePreprocessingFrame_R
    anlBtn = tk.Button(imagePreprocessingFrame_R, text='分析图片', command=analyze_image_cb)
    anlBtn.grid(column=0, row=0, **btnProps)

    imagePathEntry = tk.Entry(imagePreprocessingFrame_R, textvariable=imagePath, width=28, state='disabled')
    imagePathEntry.grid(column=0, row=1, sticky=tk.NW, columnspan=2)

    resultImageCanvas = tk.Canvas(imagePreprocessingFrame_R, width=imageWidth, height=imageHeight, bg='red')
    resultImageCanvas.grid(column=0, row=2, sticky=tk.NW, columnspan=2)

    print('image_preprocessing: %s' % result_img)

def print_result_img():
    global result_img, chartFrame
    print('print_result_img: %s' % result_img)
    # result_np = np.array(result_img)
    f = plt.Figure(figsize=(6,3), dpi=100)
    a = f.add_subplot(131)
    a.matshow(result_img)
    b = f.add_subplot(132)
    b.imshow(result_img, cmap='gray', vmin=0, vmax=255)
    hist = plt.hist(result_img.ravel(), bins=256, range=(0.0, 1.0), fc='k', ec='k')
    c = f.add_subplot(133)
    c.imshow(result_img, clim=(0.0, 0.7))
    # plt.show()
    canvas = FigureCanvasTkAgg(f, chartFrame)
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

def main_fuc():
    global container, imageWidth, imageHeight
    # global btnProps

    # global imagePath
    # global medianBlurVar_N, bilaterFilterVar_d, bilaterFilterVar_sigmaColor, bilaterFilterVar_sigmaSpace, cannyThereshold1Var, cannyThereshold2Var
    # global source_img_tk, sourceImageCanvas, result_img_tk
    global result_img, chartFrame
    
    image_preprocessing()

    print('main_fuc: %s' % result_img)

    printBtn = tk.Button(container, text='打印结果', command=print_result_img)
    printBtn.grid(column=0, row=1, sticky=tk.NW)

    chartFrame = tk.Frame(container)
    chartFrame.grid(column=0, row=2, sticky=tk.NW)

    # result_np = np.array(result_img)
    # f = plt.Figure(figsize=(5,5), dpi=64)
    # a = f.add_subplot(111)
    # a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

    

    # canvas = FigureCanvasTkAgg(f, chartFrame)
    # canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    



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

    container = tk.Frame(
        # padx=20, 
        # pady=20, 
        background='#aaeeaa'
    )
    container.pack()

    # # create a scrollbar widget and set its command to the text widget
    # scrollbar = tk.Scrollbar(window, orient='vertical', command=container.yview)
    # scrollbar.grid(row=0, column=1, sticky=tk.NS)

    # #  communicate back to the scrollbar
    # container['yscrollcommand'] = scrollbar.set

    btnProps = { 'ipadx': 8, 'ipady': 4, 'padx': 0, 'sticky': tk.W }


    # 变量声明
    imagePath = tk.StringVar()
    imagePath.set('')
    source_img_tk = None
    result_img_tk = None
    result_img = [[]]

    imageWidth = 250
    imageHeight = 200

    main_fuc()

    window.mainloop()                                   # 图形界面循环