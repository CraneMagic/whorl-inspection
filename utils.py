import tkinter as tk
import time

# from app import read_img_from_src, img_edge_detecting

def printLog(auditLogInstance, logMsg):
    log = '[%s] %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), logMsg)
    auditLogInstance.insert(tk.END, log)
    auditLogInstance.yview(tk.END)
    print(log)

# import threading
 
# exitFlag = 0
 
# class cannyThread (threading.Thread):   #继承父类threading.Thread
#     def __init__(self, auditLogInstance, imgPath, srcImg, resImg):
#         threading.Thread.__init__(self)
#         self.auditLogInstance = auditLogInstance
#         self.imgPath = imgPath
#         self.srcImg = srcImg
#         self.resImg = resImg
#     def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
#         printLog(self.auditLogInstance, "Starting " + self.imgPath)
#         self.srcImg = read_img_from_src(self.imgPath)
#         self.resImg = img_edge_detecting(self.srcImg)
#         printLog(self.auditLogInstance, "Exiting " + self.imgPath)
