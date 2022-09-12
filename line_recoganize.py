import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def get_radiant_winrate(dir_name,file_name,to_name):
    files=os.listdir("D:\\Desktop\\"+dir_name)
    files.sort(key=lambda x: int(x.split('.')[0]))
    df = pd.read_csv("D:\\Desktop\\duration\\" + file_name)
    for ii in range(len(files)):
        src=cv2.imread("D:\\Desktop\\"+dir_name+"\\"+files[ii])
        img = cv2.blur(src, (5, 5))  # 降噪
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 色彩空间转换为hsv，分离.

        # 色相（H）是色彩的基本属性，就是平常所说的颜色名称，如红色、黄色等。
        # 饱和度（S）是指色彩的纯度，越高色彩越纯，低则逐渐变灰，取0-100%的数值。
        # 明度（V），取0-100%。
        # OpenCV中绿色的H,S,V范围是35-77,43-255,46-255
        low = np.array([35, 43, 46])
        high = np.array([77, 255, 255])

        dst = cv2.inRange(src=hsv, lowerb=low, upperb=high)  # HSV高低阈值，提取图像部分区域

        # 寻找白色的像素点坐标。
        # 白色像素值是255，所以np.where(dst==255)
        R = 255
        G = 255
        B = 255
        xy = np.column_stack(np.where(dst == R * 0.3 + G * 0.59 + B * 0.11))
        # print(xy)

        # 在原图的红色数字上用 金黄色 描点填充。
        win_rate = []
        for c in xy:
            win_rate.append([c[1], c[0]])

        win_rate = sorted(win_rate, key=lambda x: x[0])
        print(win_rate)

        i = 0
        while win_rate[i][1] < 300 or win_rate[i][1] > 500:
            i += 1

        result_x = []
        result_y = []
        while i < len(win_rate):
            if win_rate[i][0] == win_rate[i - 1][0] or win_rate[i][1] - win_rate[i - 1][1] >= 30 or win_rate[i][1] - \
                    win_rate[i - 1][1] <= -30:
                i += 1
                continue
            # print(win_rate[i])
            result_x.append(win_rate[i][0])
            result_y.append(win_rate[i][1])
            # cv2.circle(img=img, center=(int(win_rate[i][0]), int(win_rate[i][1])), radius=1, color=(0, 215, 255), thickness=1)
            i += 1
            # 注意颜色值是(b,g,r)，不是(r,g,b)
            # 坐标:c[1]是x,c[0]是y

        x = np.array(result_x)
        y = np.array(result_y)
        x2 = np.array(range(win_rate[0][0], x[-1]))
        y2 = np.interp(x2, x, y)
        duration = df['duration'][ii] / 60
        x3 = x2 * (duration / x2[-1])
        if y2[-1]<y2[0]:
            b = 50 / (y2[0] - y2[-1])
            a = 100 + y2[-1] * b
        if y2[-1]>y2[0]:
            b = 50/(y2[-1]-y2[0])
            a = y2[-1]*b
        y3 = a - y2 * b
        # print(x3,y3)
        # plt.scatter(x,y,color='b')
        plt.plot(x3, y3, 'o', markersize=1)
        plt.show()
        # x3和y3是最终的坐标：

        for j in range(len(x2)):
            print('{:.2f},{:.2f}'.format(x3[j], y3[j]))
            cv2.circle(img=img, center=(int(x2[j]), int(y2[j])), radius=1, color=(0, 215, 255), thickness=1)

        dirs = "D:\\Desktop\\" + to_name
        if not os.path.exists(dirs):
            os.makedirs(dirs)

        lst=zip(x3,y3)
        data=pd.DataFrame(lst,columns=['time','win_rate'])
        data.to_csv(dirs+"\\"+str(df['match_id'][ii])+".csv", index=None)

        # cv2.imshow('dst', dst)
        # cv2.imshow('result', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


def get_dire_winrate(dir_name,file_name,to_name):
    files = os.listdir("D:\\Desktop\\" + dir_name)
    files.sort(key=lambda x: int(x.split('.')[0]))
    df = pd.read_csv("D:\\Desktop\\duration\\" + file_name)
    for ii in range(len(files)):
        src = cv2.imread("D:\\Desktop\\" + dir_name + "\\" + files[ii])
        img = cv2.blur(src, (5, 5))  # 降噪
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 色彩空间转换为hsv，分离.

        # 色相（H）是色彩的基本属性，就是平常所说的颜色名称，如红色、黄色等。
        # 饱和度（S）是指色彩的纯度，越高色彩越纯，低则逐渐变灰，取0-100%的数值。
        # 明度（V），取0-100%。
        # OpenCV中绿色的H,S,V范围是35-77,43-255,46-255
        low = np.array([35, 43, 46])
        high = np.array([77, 255, 255])

        dst = cv2.inRange(src=hsv, lowerb=low, upperb=high)  # HSV高低阈值，提取图像部分区域

        # 寻找白色的像素点坐标。
        # 白色像素值是255，所以np.where(dst==255)
        R = 255
        G = 255
        B = 255
        xy = np.column_stack(np.where(dst == R * 0.3 + G * 0.59 + B * 0.11))
        # print(xy)

        # 在原图的红色数字上用 金黄色 描点填充。
        win_rate = []
        for c in xy:
            win_rate.append([c[1], c[0]])

        win_rate = sorted(win_rate, key=lambda x: x[0])
        print(win_rate)

        i = 0
        while win_rate[i][1] < 300 or win_rate[i][1] > 500:
            i += 1

        result_x = []
        result_y = []
        while i < len(win_rate):
            if win_rate[i][0] == win_rate[i - 1][0] or win_rate[i][1] - win_rate[i - 1][1] >= 30 or win_rate[i][1] - \
                    win_rate[i - 1][1] <= -30:
                i += 1
                continue
            # print(win_rate[i])
            result_x.append(win_rate[i][0])
            result_y.append(win_rate[i][1])
            # cv2.circle(img=img, center=(int(win_rate[i][0]), int(win_rate[i][1])), radius=1, color=(0, 215, 255), thickness=1)
            i += 1
            # 注意颜色值是(b,g,r)，不是(r,g,b)
            # 坐标:c[1]是x,c[0]是y

        x = np.array(result_x)
        y = np.array(result_y)
        x2 = np.array(range(win_rate[0][0], x[-1]))
        y2 = np.interp(x2, x, y)
        duration = df['duration'][ii] / 60
        x3 = x2 * (duration / x2[-1])
        if y2[-1] < y2[0]:
            b = 50 / (y2[0] - y2[-1])
            a = 100 + y2[-1] * b
        if y2[-1] > y2[0]:
            b = 50 / (y2[-1] - y2[0])
            a = y2[-1] * b
        y3 = a - y2 * b
        # print(x3,y3)
        # plt.scatter(x,y,color='b')
        plt.plot(x3, y3, 'o', markersize=1)
        plt.show()
        # x3和y3是最终的坐标：

        for j in range(len(x2)):
            print('{:.2f},{:.2f}'.format(x3[j], y3[j]))
            cv2.circle(img=img, center=(int(x2[j]), int(y2[j])), radius=1, color=(0, 215, 255), thickness=1)

        lst=zip(x3,100-y3)
        data=pd.DataFrame(lst,columns=['time','win_rate'])

        dirs = "D:\\Desktop\\"+to_name
        if not os.path.exists(dirs):
            os.makedirs(dirs)

        data.to_csv(dirs + "\\"+str(df['match_id'][ii])+".csv", index=None)

        # cv2.imshow('dst', dst)
        # cv2.imshow('result', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

if __name__ == "__main__":
    dir_name="pic13"
    file_name="rng_radiant_duration.csv"
    to_name="rng_radiant_winrate"
    get_radiant_winrate(dir_name,file_name,to_name)




