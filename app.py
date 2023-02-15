import tkinter as tk
import tkinter.filedialog as tk_filedialog
import cv2 as cv
from PIL import Image, ImageTk

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils import printLog

import threading
import os
 
exitFlag = 0
 
class cannyThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, auditLogInstance, imgPath):
        threading.Thread.__init__(self)
        self.auditLogInstance = auditLogInstance
        self.imgPath = imgPath
        self.srcImg = None
        self.resImg = None
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        printLog(self.auditLogInstance, "Starting " + self.imgPath)
        pathList = self.imgPath.split('/')
        pathList.insert(-1, 'edge_detection_results')
        # print('/'.join(pathList))
        self.srcImg = read_img_from_src(self.imgPath)
        self.resImg = img_edge_detecting(self.srcImg, pathList[-1])
        if not os.path.exists('/'.join(pathList[0: -1])):
            os.mkdir('/'.join(pathList[0: -1]))
        cv.imwrite('/'.join(pathList), self.resImg)
        printLog(self.auditLogInstance, "Exiting " + self.imgPath)


def read_img_from_src(imgPathStr):
    global auditLog
    printLog(auditLog, '读取图片... %s' % imgPathStr)

    img = cv.imread(imgPathStr)
    img = img[750:1750, 1000:3000]
    return img

def img_edge_detecting(img, imgName):
    global auditLog
    printLog(auditLog, '边缘检测... %s' % imagePathsStr[0])

    global medianBlurVar_N, bilaterFilterVar_d, bilaterFilterVar_sigmaColor, bilaterFilterVar_sigmaSpace, cannyThereshold1Var, cannyThereshold2Var
    global curImgs
    img_gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    img_gray_blur = img_gray
    img_gray_blur = cv.medianBlur(img_gray, medianBlurVar_N.get())
    img_gray_bilateral = cv.bilateralFilter(img_gray_blur, bilaterFilterVar_d.get(), bilaterFilterVar_sigmaColor.get(), bilaterFilterVar_sigmaSpace.get())
    result_img = cv.Canny(img_gray_bilateral, cannyThereshold1Var.get(), cannyThereshold2Var.get())
    curImgs[imgName] = result_img
    return result_img

class whorlThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, auditLogInstance, imgName, srcImg):
        threading.Thread.__init__(self)
        self.auditLogInstance = auditLogInstance
        self.imgName = imgName
        self.srcImg = srcImg
        self.resPts = None
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        printLog(self.auditLogInstance, "开始分析数据 " + self.imgName)
        # pathList = self.imgPath.split('/')
        # pathList.insert(-1, 'new')
        self.resPts = analyze_whorl(self.srcImg, self.imgName)
        # pathList = self.imgPath.split('/')
        # pathList.insert(-1, 'new')
        # print('/'.join(pathList))
        # cv.imwrite('/'.join(pathList), self.resPts)
        printLog(self.auditLogInstance, "分析数据结束 " + self.imgName)

def pts_sort_by_x(yx):
    [y, x] = yx
    return [[x[i], y[i]] for i in np.argsort(x)]
    
def pts_sort_by_y(yx):
    [y, x] = yx
    return [[x[i], y[i]] for i in np.argsort(y)]

def analyze_whorl(processedImg, imgName):
    global auditLog
    print('Analyze Whorl', imgName, type(processedImg), processedImg.ndim, processedImg.shape)
    [yPx, xPx] = processedImg.shape
    res_pts = []
    res_yx = [[], []]
    for j in range(yPx):
        thread = countThread(auditLog, res_pts, processedImg, j, res_yx)
        thread.start()
    # print(res_yx[0], res_yx[1])
    print(len(pts_sort_by_x(res_yx)))
    # print(pts_sort_by_y(res_yx))
    # print(pts_sort_by_x(res_yx)[0], pts_sort_by_x(res_yx)[-1])
    # print(pts_sort_by_y(res_yx)[0], pts_sort_by_y(res_yx)[-1])
    pt_sta = pts_sort_by_x(res_yx)[0]
    pt_end = pts_sort_by_x(res_yx)[-1]
    pt_top = pts_sort_by_y(res_yx)[0]
    pt_btm = pts_sort_by_y(res_yx)[-1]
    print(pt_sta, pt_end)
    print(pt_top, pt_btm)
    plt.plot(res_yx[1], res_yx[0], 'o')
    plt.savefig()

    

class countThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, auditLogInstance, res_pts, imgarr, j, res_yx):
        threading.Thread.__init__(self)
        self.auditLogInstance = auditLogInstance
        self.res_pts = res_pts
        self.imgarr = imgarr
        self.j = j
        self.res_yx = res_yx
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        # printLog(self.auditLogInstance, "开始采集点 " + str(self.i))
        get_edge_pts(self.res_pts, self.imgarr, self.j, self.res_yx)
        # printLog(self.auditLogInstance, "采集点结束 " + str(self.i))

def get_edge_pts(res_pts, imgarr, j, res_yx):
    for i in range(len(imgarr[j])):
        if not imgarr[j][i] == 0:
            # print(i, j, imgarr[i][j])
            res_pts.append([j, i])
            res_yx[0].append(j)
            res_yx[1].append(i)


def select_images_cb():
    global auditLog
    global imagePathsVar, imagePathsStr
    global imagePath, source_img_tk, sourceImageCanvas, imagePathList
    selectImages = tk_filedialog.askopenfilenames(title='选择图片', filetypes=[('PNG', '*.png'), ('JPG', '*.jpg'), ('BMP', '*.bmp')])
    # selectDirect = tk_filedialog.askdirectory(title='选择文件夹')
    # print(selectDirect)
    # print(selectImages)

    for i in range(len(selectImages)):
        imagePathsVar.append(tk.StringVar())
        imagePathsVar[i].set(selectImages[i])

    for i in range(len(imagePathsVar)):
        imagePathsStr.append(imagePathsVar[i].get())
        imagePathList.insert(0, imagePathsStr[i].split('/')[-1])
        thread = cannyThread(auditLog, imagePathsStr[i])
        thread.start()
        
    # img = cv.imread(imagePathsStr[0])
    # source_img_src = Image.fromarray(img)
    # currentSourceWidth = int(source_img_src.size[0] / source_img_src.size[1] * imageHeight)
    # currentSourceHeight = int(source_img_src.size[1] / source_img_src.size[0] * imageWidth)
    # # source_img_src = source_img_src.resize([imageWidth, currentSourceHeight])
    # source_img_src = source_img_src.resize([currentSourceWidth, imageHeight])
    # source_img_tk = ImageTk.PhotoImage(image=source_img_src)
    # # sourceImageCanvas.config(height=currentSourceHeight)
    # sourceImageCanvas.config(width=currentSourceWidth)
    # # sourceImageCanvas.create_image((imageWidth/2, currentSourceHeight/2), image=source_img_tk)
    # sourceImageCanvas.create_image((currentSourceWidth/2, imageHeight/2), image=source_img_tk)


def redo_canny():
    global imagePathsVar
    for i in range(len(imagePathsVar)):
        thread = cannyThread(auditLog, imagePathsStr[i])
        thread.start()

def redo_whorl():
    global imagePathsVar
    for i in range(len(imagePathsVar)):
        imgName = imagePathsStr[i].split('/')[-1]
        thread = whorlThread(auditLog, imgName, curImgs[imgName])
        thread.start()

def clear_image_cb(val):
    print('clear_image_cb')
    # redo_canny()

def clear_image_cb_medianBlurVar_N(val):
    # global result_img_tk, resultImageCanvas
    # result_img_tk = None
    if int(val) % 2 == 0:
        medianBlurScale_n.set(int(val) + 1)
    # redo_canny()


def clear_image_cb_bilaterFilterVar_d(val):
    # global result_img_tk, resultImageCanvas
    # result_img_tk = None
    if int(val) % 2 == 0:
        bilaterFilterScale_d.set(int(val) + 1)
    # redo_canny()


def collect_images_from_live_camera(val):
    print('Collect Images from Live Camera')


def image_preprocessing():
    global imagePathsVar, imagePathList, source_img_tk, sourceImageCanvas, result_img_tk, resultImageCanvas, result_img
    global medianBlurVar_N, bilaterFilterVar_d, bilaterFilterVar_sigmaColor, bilaterFilterVar_sigmaSpace, cannyThereshold1Var, cannyThereshold2Var

    imagePreprocessingFrame = tk.Frame(container, padx=20, pady=20, 
        # bg='#efefef'
    )
    imagePreprocessingFrame.grid(column=0, row=0, sticky=tk.NW)

    imagePreprocessingFrame_L = tk.Frame(imagePreprocessingFrame, padx=20, pady=20)
    imagePreprocessingFrame_L.grid(column=0, row=0, sticky=tk.NW)
    imagePreprocessingFrame_C = tk.Frame(imagePreprocessingFrame, padx=20, pady=20)
    imagePreprocessingFrame_C.grid(column=1, row=0, sticky=tk.NW)
    imagePreprocessingFrame_R = tk.Frame(imagePreprocessingFrame, padx=20, pady=20)
    imagePreprocessingFrame_R.grid(column=2, row=0, sticky=tk.NW)
    
    
    # imagePreprocessingFrame_L
    colBtn = tk.Button(imagePreprocessingFrame_L, text='采集摄像头图片(暂无)', command=collect_images_from_live_camera)
    selBtn = tk.Button(imagePreprocessingFrame_L, text='选择本地图片', command=select_images_cb)
    colBtn.grid(column=0, row=0, **btnProps)
    selBtn.grid(column=1, row=0, **btnProps)

    # imagePathEntry = tk.Entry(imagePreprocessingFrame_L, textvariable=imagePath, width=28, state='disabled')
    # imagePathEntry.grid(column=0, row=1, sticky=tk.NW, columnspan=2)

    imagePathList = tk.Listbox(imagePreprocessingFrame_L, width=32)
    imagePathList.grid(column=0, row=1, sticky=tk.NW, columnspan=2)

    sourceImageCanvas = tk.Canvas(imagePreprocessingFrame_L, width=imageWidth, height=imageHeight, bg='blue')
    # sourceImageCanvas.grid(column=0, row=2, sticky=tk.NW, columnspan=2)


    # imagePreprocessingFrame_C
    medianBlurRow, bilaterFilterRow, cannyTheresholdRow = 0, 1, 2
    
    # medianBlur
    medianBlurVar_N = tk.IntVar(value=35)
    medianBlurLf = tk.LabelFrame(imagePreprocessingFrame_C, text='中值滤波', padx=16, pady=8)
    medianBlurLf.grid(column=0, row=medianBlurRow, sticky=tk.NW)
    # medianBlur_Layout
    tk.Label(medianBlurLf, text='卷积核 N', justify='left').grid(column=0, row=0, sticky=tk.W)
    global medianBlurScale_n
    medianBlurScale_n = tk.Scale(medianBlurLf, variable=medianBlurVar_N, from_=1, to=99, orient='horizontal', command=clear_image_cb_medianBlurVar_N)
    medianBlurScale_n.grid(column=1, row=0, sticky=tk.W)

    # bilaterFilter
    bilaterFilterVar_d, bilaterFilterVar_sigmaColor, bilaterFilterVar_sigmaSpace = tk.IntVar(value=15), tk.IntVar(value=150), tk.IntVar(value=150)
    bilaterFilterLf = tk.LabelFrame(imagePreprocessingFrame_C, text='双边滤波', padx=16, pady=8)
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
    cannyThereshold1Var, cannyThereshold2Var = tk.IntVar(value=10), tk.IntVar(value=40)
    cannyLf = tk.LabelFrame(imagePreprocessingFrame_C, text='Canny', padx=16, pady=8)
    cannyLf.grid(column=0, row=cannyTheresholdRow, sticky=tk.NW)
    # canny_Layout
    tk.Label(cannyLf, text='较小阈值 minVal', justify='left').grid(column=0, row=0, sticky=tk.W)
    cannyThereshold1Scale = tk.Scale(cannyLf, variable=cannyThereshold1Var, from_=0, to=60, orient='horizontal', command=clear_image_cb)
    cannyThereshold1Scale.grid(column=1, row=0, sticky=tk.W)
    tk.Label(cannyLf, text='较大阈值 maxVal', justify='left').grid(column=0, row=1, sticky=tk.W)
    cannyThereshold2Scale = tk.Scale(cannyLf, variable=cannyThereshold2Var, from_=0, to=60, orient='horizontal', command=clear_image_cb)
    cannyThereshold2Scale.grid(column=1, row=1, sticky=tk.W)

    # imagePreprocessingFrame_R
    anlBtn = tk.Button(imagePreprocessingFrame_R, text='分析图片', command=redo_canny)
    anlBtn.grid(column=0, row=0, **btnProps)
    anlBtn = tk.Button(imagePreprocessingFrame_R, text='分析数据', command=redo_whorl)
    anlBtn.grid(column=1, row=0, **btnProps)

    imagePathEntry = tk.Entry(imagePreprocessingFrame_R, textvariable=imagePath, width=28, state='disabled')
    imagePathEntry.grid(column=0, row=1, sticky=tk.NW, columnspan=2)

    resultImageCanvas = tk.Canvas(imagePreprocessingFrame_R, width=imageWidth, height=imageHeight, bg='red')
    # resultImageCanvas.grid(column=0, row=2, sticky=tk.NW, columnspan=2)

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
    global container, imageWidth, imageHeight, imagePathsVar
    # global btnProps

    # global imagePath
    # global medianBlurVar_N, bilaterFilterVar_d, bilaterFilterVar_sigmaColor, bilaterFilterVar_sigmaSpace, cannyThereshold1Var, cannyThereshold2Var
    # global source_img_tk, sourceImageCanvas, result_img_tk
    global result_img, chartFrame
    
    image_preprocessing()

    print('main_fuc: %s' % result_img)

    # printBtn = tk.Button(container, text='打印结果', command=print_result_img)
    # printBtn.grid(column=0, row=1, sticky=tk.NW)

    # chartFrame = tk.Frame(container)
    # chartFrame.grid(column=0, row=2, sticky=tk.NW)

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
    winHeight = 900
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
        # background='#aaeeaa'
    )
    container.pack()

    # # create a scrollbar widget and set its command to the text widget
    # scrollbar = tk.Scrollbar(window, orient='vertical', command=container.yview)
    # scrollbar.grid(row=0, column=1, sticky=tk.NS)

    # #  communicate back to the scrollbar
    # container['yscrollcommand'] = scrollbar.set

    btnProps = { 'ipadx': 8, 'ipady': 4, 'padx': 0, 'sticky': tk.W }


    # 变量声明
    imagePathsVar = []
    imagePathsStr = []
    curImgs = {}


    imagePath = tk.StringVar()
    imagePath.set('')
    source_img_tk = None
    result_img_tk = None
    result_img = [[]]

    imageWidth = 250
    imageHeight = 200

    main_fuc()

    auditLogFrame = tk.LabelFrame(window, text='日志输出', padx=20, pady=10)
    auditLog = tk.Listbox(auditLogFrame, width=100, bd=0)
    auditLog.pack()
    auditLogFrame.pack()

    window.mainloop()                                   # 图形界面循环