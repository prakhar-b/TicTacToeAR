# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 16:19:25 2020

@author: prakhar
"""

import tkinter as tk
from tkinter import messagebox
import os
os.system('clear')
import cv2
import numpy as np


def build_squares(img):
    x, y, w, h = 420, 140, 10, 10
    d = 10
    imgCrop = None
    crop = None
    for i in range(10):
        for j in range(5):
            if np.any(imgCrop == None):
                imgCrop = img[y:y+h, x:x+w]
            else:
                imgCrop = np.hstack((imgCrop, img[y:y+h, x:x+w]))
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 1)
            x+=w+d
        if np.any(crop == None):
            crop = imgCrop
        else:
            crop = np.vstack((crop, imgCrop))
        imgCrop = None
        x = 420
        y+=h+d
    return crop

def get_hand_hist():
    global hist
    cam = cv2.VideoCapture(1)
    if cam.read()[0]==False:
        cam = cv2.VideoCapture(0)
    x, y, w, h = 300, 100, 300, 300
    flagPressedC, flagPressedS = False, False
    imgCrop = None
    while True:
        img = cam.read()[1]
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (640, 480))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        keypress = cv2.waitKey(1)
        if keypress == ord('c'):
            hsvCrop = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2HSV)
            flagPressedC = True
            hist = cv2.calcHist([hsvCrop], [0, 1], None, [180, 256], [0, 180, 0, 256])
            cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
        elif keypress == ord('s'):
            flagPressedS = True
            break
        if flagPressedC:
            dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)
            dst1 = dst.copy()
            disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
            cv2.filter2D(dst,-1,disc,dst)
            blur = cv2.GaussianBlur(dst, (11,11), 0)
            blur = cv2.medianBlur(blur, 15)
            ret,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            thresh = cv2.merge((thresh,thresh,thresh))
            cv2.imshow("Thresh", thresh)
            cv2.imshow("DST", dst)
        if not flagPressedS:
               imgCrop = build_squares(img)
               cv2.imshow("Set hand histogram", img)
    cam.release()
    cv2.destroyAllWindows()
    return hist

def check():                #Checks for victory or Draw
    c=0
    global b
    for i in range(3):
        for j in range(3):
            if b[i][j] == -1:
                c=1        
    if b==[[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]:
        return 0
    for i in range(3):
            if(b[i][0]==b[i][1]==b[i][2] != -1):
                sendMessage(2, xp[b[i][0]])
                return 1
            elif (b[0][i]==b[1][i]==b[2][i] != -1):
                sendMessage(2, xp[b[0][i]])
                return 1
    if(b[0][0]==b[1][1]==b[2][2] != -1):
        sendMessage(3, xp[b[0][0]])
        return 1
    elif (b[0][2]==b[1][1]==b[2][0] != -1):
        sendMessage(3, xp[b[1][1]])
        return 1
    if c==0:
        sendMessage(1, 2)
        return 1

def sendMessage(a, s):
    # top = Tk()
    # top.geometry("100x100")
    if a==1:
        messagebox.showinfo("Tied!!","The match ended in a draw")
    elif a==2:
        messagebox.showinfo("Congrats!!","'"+str(s)+"' has won")
    elif a==3:
        messagebox.showinfo("Congrats!!","'"+str(s)+"' has won")
    else:
        messagebox.showerror("Invalid Input!")
    #top.mainloop()
        

def findContour(frame, roi,  hist, mark, clr):
    if (mark==0):
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)
        dst1 = dst.copy()
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
        cv2.filter2D(dst,-1,disc,dst)
        blur = cv2.GaussianBlur(dst, (11,11), 0)
        blur = cv2.medianBlur(blur, 15)
        ret,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        (_, cnts, _) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imshow("In Loop", thresh)
        if len(cnts) > 0:
            contour = max(cnts, key = cv2.contourArea)
            if cv2.contourArea(contour) > 2000:
                mark = 1
    return(frame, mark, clr)

def change():
    global clr
    if clr ==0:
        clr = 1
    else:
        clr=0
    return clr

def init():
    global m9,m8,m7,m6,m5,m4,m3,m2,m1
    global clr
    global p9,p8,p7,p6,p5,p4,p3,p2,p1
    global color
    global cp, b, xp
    m9=m8=m7=m6=m5=m4=m3=m2=m1=0
    clr=0
    p9=p8=p7=p6=p5=p4=p3=p2=p1=0
    color = [(0,0,255), (0,255,100)]
    cp = [0,0,0,0,0,0,0,0,0,0]
    b=[[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
    xp = ["red", "green"]
    return

def game():
    global cam
    global hist
    cam = cv2.VideoCapture(0)
    global m9,m8,m7,m6,m5,m4,m3,m2,m1
    global clr
    global p9,p8,p7,p6,p5,p4,p3,p2,p1
    global color
    global cp, b, xp
    global b
    m9=m8=m7=m6=m5=m4=m3=m2=m1=0
    clr=0
    p9=p8=p7=p6=p5=p4=p3=p2=p1=0
    color = [(0,0,255), (0,255,100)]
    cp = [0,0,0,0,0,0,0,0,0,0]
    b=[[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
    xp = ["red", "green"]
    while(True):
        ret, frame = cam.read()
        if not ret:
            break
        frame = cv2.flip(frame,1)
        frame = cv2.resize(frame, (640, 480))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height,width,_ = frame.shape
        h = int(height)
        w = int(width)
        start = (int(w/3),0)
        end = (int(w/3), h)
        colour = (100,100,100)
        thickness = 5
        frame = cv2.line(frame, start, end,colour, thickness)
        roi1 = frame[0:0+int(h/3), 0:0+int(w/3)]
        c1 = ( int(w/6), int(h/6) )
        roi2 = frame[0:0+int(h/3), int(w/3):2*int(w/3)]
        c2 = ( int(w/2), int(h/6) )
        roi3 = frame[0:0+int(h/3), 2*int(w/3):3*int(w/3)]
        c3 = ( 5*int(w/6), int(h/6) )
        roi4 = frame[int(h/3):2*int(h/3), 0:0+int(w/3)]
        c4 = ( int(w/6), int(h/2) )
        roi5 = frame[int(h/3):2*int(h/3), int(w/3):2*int(w/3)]
        c5 = ( int(w/2), int(h/2) )
        roi6 = frame[int(h/3):2*int(h/3), 2*int(w/3):3*int(w/3)]
        c6 = ( 5*int(w/6), int(h/2) )
        roi7 = frame[2*int(h/3):3*int(h/3), 0:0+int(w/3)]
        c7 = ( int(w/6), 5*int(h/6) )
        roi8 = frame[2*int(h/3):3*int(h/3), int(w/3):2*int(w/3)]
        c8 = ( int(w/2), 5*int(h/6) )
        roi9 = frame[2*int(h/3):3*int(h/3), 2*int(w/3):3*int(w/3)]
        c9 = ( 5*int(w/6), 5*int(h/6) )
        
    
        if m9==0:
            frame, m9, clr = findContour(frame, roi9, hist, m9, clr)
            if (m9==1):
                cp[9] = change()
                b[2][2] = cp[9]
        if (m9==1):
            if b[2][2] == 0:
                frame = cv2.drawMarker(frame, c9, color[cp[9]] ,markerType=cv2.MARKER_TILTED_CROSS, markerSize=90, thickness=3, line_type=cv2.LINE_AA )
            elif b[2][2] == 1:
                frame = cv2.circle(frame, c9,50, color[cp[9]], 3 )
        if m8==0:
            frame, m8, clr = findContour(frame, roi8, hist, m8, clr)
            if (m8==1):
                cp[8] = change()
                b[2][1] = cp[8]
        if (m8==1):
            if cp[8] == 1:
                frame = cv2.circle(frame, c8,50, color[cp[8]], 3 )
            else:
                frame = cv2.drawMarker(frame, c8, color[cp[8]] ,markerType=cv2.MARKER_TILTED_CROSS, markerSize=90, thickness=3, line_type=cv2.LINE_AA )
        if m7==0:
            frame, m7, clr = findContour(frame, roi7, hist, m7, clr)
            if m7==1:
                cp[7] = change()
                b[2][0] = cp[7]
        if (m7==1):
            if cp[7] == 1:
                frame = cv2.circle(frame, c7,50, color[cp[7]], 3 )
            else:
                frame = cv2.drawMarker(frame, c7, color[cp[7]] ,markerType=cv2.MARKER_TILTED_CROSS, markerSize=90, thickness=3, line_type=cv2.LINE_AA )
        if m6==0:
            frame, m6, clr = findContour(frame, roi6, hist, m6, clr)
            if m6==1:
                cp[6] = change()
                b[1][2] = cp[6]
        if (m6==1):
            if cp[6] ==1:
                frame = cv2.circle(frame, c6,50, color[cp[6]], 3 )
            else:
                frame = cv2.drawMarker(frame, c6, color[cp[6]] ,markerType=cv2.MARKER_TILTED_CROSS, markerSize=90, thickness=3, line_type=cv2.LINE_AA )
        if m5==0:
            frame, m5, clr = findContour(frame, roi5, hist, m5, clr)
            if m5==1:
                cp[5] = change()
                b[1][1] = cp[5]
        if (m5==1):
            if cp[5] == 1:
                frame = cv2.circle(frame, c5,50, color[cp[5]], 3 )
            else:
                frame = cv2.drawMarker(frame, c5, color[cp[5]] ,markerType=cv2.MARKER_TILTED_CROSS, markerSize=90, thickness=3, line_type=cv2.LINE_AA )
        if m4==0:
            frame, m4, clr = findContour(frame, roi4, hist, m4, clr)
            if m4==1:
                cp[4] = change()
                b[1][0] = cp[4]
        if (m4==1):
            if cp[4] == 1:
                frame = cv2.circle(frame, c4,50, color[cp[4]], 3 )
            else:
                frame = cv2.drawMarker(frame, c4, color[cp[4]] ,markerType=cv2.MARKER_TILTED_CROSS, markerSize=90, thickness=3, line_type=cv2.LINE_AA )
        if m3==0:
            frame, m3, clr = findContour(frame, roi3, hist, m3, clr)
            if m3==1:
                cp[3] = change()
                b[0][2] = cp[3]
        if (m3==1):
            if cp[3] == 1:
                frame = cv2.circle(frame, c3,50, color[cp[3]], 3 )
            else:
                frame = cv2.drawMarker(frame, c3, color[cp[3]] ,markerType=cv2.MARKER_TILTED_CROSS, markerSize=90, thickness=3, line_type=cv2.LINE_AA )
        if m2==0:
            frame, m2, clr = findContour(frame, roi2, hist, m2, clr)
            if m2 ==1:
                cp[2] = change()
                b[0][1] = cp[2]
        if (m2==1):
            if cp[2] == 1:
                frame = cv2.circle(frame, c2,50, color[cp[2]], 3 )    
            else:
                frame = cv2.drawMarker(frame, c2, color[cp[2]] ,markerType=cv2.MARKER_TILTED_CROSS, markerSize=90, thickness=3, line_type=cv2.LINE_AA )
        if m1==0:
            frame, m1, clr = findContour(frame, roi1, hist, m1, clr)
            if m1==1:
                cp[1] = change()
                b[0][0] = cp[1]
        if (m1==1):
            if cp[1] == 1:
                frame = cv2.circle(frame, c1,50, color[cp[1]], 3 )
            else:
                frame = cv2.drawMarker(frame, c1, color[cp[1]] ,markerType=cv2.MARKER_TILTED_CROSS, markerSize=90, thickness=3, line_type=cv2.LINE_AA )
    
        start = (2*int(w/3),0)
        end = (2*int(w/3), h)
        thickness = 5
        frame = cv2.line(frame, start, end,colour, thickness)
        start = (0,int(h/3))
        end = (w, int(h/3))
        # colour = (0,255,0)
        thickness = 5
        frame = cv2.line(frame, start, end,colour, thickness)
        start = (0,2*int(h/3))
        end = (w, 2*int(h/3))
        # colour = (0,255,0)
        thickness = 5
        frame = cv2.line(frame, start, end,colour, thickness)

        cv2.imshow("Tic-Tac-Toe", frame)
        if cv2.waitKey(10) == ord('q'):
            print("Closing Program")
            break
        rx = check()
        if rx==1:
            break
        # if(k%256 == 27):
        #     print("INFO: Closing Program ...")
        #     break
    cam.release()
    cv2.destroyAllWindows()
    return cam

root = tk.Tk()
root.configure(bg='#A3E4D7')
root.title("Tic-Tac-Toe")
root.geometry("400x200")
topframe = tk.Frame(root)
topframe.pack(side= tk.TOP)
bottomframe = tk.Frame(root)
bottomframe.pack(side= tk.BOTTOM)
background_image=tk.PhotoImage(...)
#background_label = tk.Label(bottomframe, image=background_image)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)
rootHeading = tk.Label(root, text="Welcome to VR X-O-X-O")
rootHeading.pack()
hist = []
lab2 = tk.Label(root, text="Failed")
lab2.pack()
objScanHeading = tk.Label(topframe, text="Press Scan button to scan the object")
objScanHeading.pack()
scanBtn = tk.Button(topframe, text="Scan", command = get_hand_hist)
scanBtn.pack()
gameHeading = tk.Label(bottomframe, text="Press Start to start the game.")
gameHeading.pack()
startBtn = tk.Button(bottomframe, text="START", command = game)
startBtn.pack()
root.mainloop()

global cam

cam.release()
cv2.destroyAllWindows()