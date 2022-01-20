import cv2
import numpy as np
import imutils
import time
import datetime
import RPi.GPIO as GPIO
import os
cap = cv2.VideoCapture('video1.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2()
#fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
car_counter = 0
car_counter2 = 0
car_counter3 = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, False)
while True:
    ahora = datetime.datetime.now()
    dia = str(ahora.day)
    mes = str(ahora.month)
    año = str(ahora.year)   
    hora = str(ahora.hour)
    minuto = str(ahora.minute)
    segundo = str(ahora.second)
    ret, frame = cap.read()
    if ret == False: break
    frame = imutils.resize(frame, width=640)
    # Especificamos los puntos extremos del área a analizar
    area_pts = np.array([[25, 220], [frame.shape[1]-495, 220], [frame.shape[1]-495, 255], [25, 255]])
    
    area_pts2 = np.array([[350, 275], [frame.shape[1]-170, 275], [frame.shape[1]-170, 310], [350, 310]])

    area_pts3 = np.array([[180, 96], [frame.shape[1]-340, 96], [frame.shape[1]-340, 61], [180, 61]])

    # Con ayuda de una imagen auxiliar, determinamos el área
    # sobre la cual actuará el detector de movimiento
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    image_area = cv2.bitwise_and(frame, frame, mask=imAux)
     
   
    imAux2 = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux2 = cv2.drawContours(imAux2, [area_pts2], -1, (255), -1)
    image_area2 = cv2.bitwise_and(frame, frame, mask=imAux2)

    imAux3 = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux3 = cv2.drawContours(imAux3, [area_pts3], -1, (255), -1)
    image_area3 = cv2.bitwise_and(frame, frame, mask=imAux3)
    
    # Obtendremos la imagen binaria donde la región en blanco representa
    # la existencia de movimiento
    fgmask = fgbg.apply(image_area)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    fgmask = cv2.dilate(fgmask, None, iterations=5)

    fgmask2 = fgbg.apply(image_area2)
    fgmask2 = cv2.morphologyEx(fgmask2, cv2.MORPH_OPEN, kernel)
    fgmask2 = cv2.morphologyEx(fgmask2, cv2.MORPH_CLOSE, kernel)
    fgmask2 = cv2.dilate(fgmask2, None, iterations=5)

    fgmask3 = fgbg.apply(image_area3)
    fgmask3 = cv2.morphologyEx(fgmask3, cv2.MORPH_OPEN, kernel)
    fgmask3 = cv2.morphologyEx(fgmask3, cv2.MORPH_CLOSE, kernel)
    fgmask3 = cv2.dilate(fgmask3, None, iterations=5)
    # Encontramos los contornos presentes de fgmask, para luego basándonos
    # en su área poder determinar si existe movimiento (autos)
    cnts= cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts2= cv2.findContours(fgmask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts3= cv2.findContours(fgmask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    timee = time.strftime("%H-%M")
    horap = str(timee)
    nombres = horap + ".txt"
    if not os.path.exists(nombres):
        f= open(nombres,"w+")
       # f.close()


            
    for cnt in cnts:
        if cv2.contourArea(cnt) > 1500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,255), 1)
            if 60 < (x + w ) < 80:

                GPIO.output(40, True)
                time.sleep(1)
                GPIO.output(40, False)
               
                car_counter = car_counter + 1
                cv2.line(frame, (70, 220), (70, 255), (0, 255, 0), 3)
                archivo = open(nombres,"a")
                carro = "1"
                archivo.write(carro)
                archivo.write(",")
                archivo.write(",")
                archivo.write(",")
                archivo.write(",")                     
                archivo.write(dia)
                archivo.write(",")
                archivo.write(mes)
                archivo.write(",")
                archivo.write(año)
                archivo.write(",")
                archivo.write(",")
                archivo.write(hora)
                archivo.write(",")        
                archivo.write(minuto)
                archivo.write(",")
                archivo.write(segundo)
                archivo.write(",")
                archivo.write("\n")
                archivo.close()
                
    for cnt2 in cnts2:
        if cv2.contourArea(cnt2) > 1500:
            x, y, w, h = cv2.boundingRect(cnt2)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 1)
            if 385 < (x + w) < 405:
                car_counter2 = car_counter2 + 1
                cv2.line(frame, (395, 275), (395, 310), (0, 255, 250), 3)
                archivo = open(nombres,"a")
                carro2 = "1"
                archivo.write(",")              
                archivo.write(carro2)
                archivo.write(",")
                archivo.write(",")
                archivo.write(",")
                archivo.write(dia)
                archivo.write(",")
                archivo.write(mes)
                archivo.write(",")
                archivo.write(año)
                archivo.write(",")
                archivo.write(",")
                archivo.write(hora)
                archivo.write(",")        
                archivo.write(minuto)
                archivo.write(",")
                archivo.write(segundo)
                archivo.write(",")
                archivo.write("\n")
                archivo.close()

    for cnt3 in cnts3:
        if cv2.contourArea(cnt3) > 1500:
            x, y, w, h = cv2.boundingRect(cnt3)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,255), 1)
            if 215 < (x + w) < 235:
                car_counter3 = car_counter3 + 1
                cv2.line(frame, (225, 61), (225, 96), (0, 255, 150), 3)
                archivo = open(nombres,"a")
                carro3 = "1"
                archivo.write(",")
                archivo.write(",")
                archivo.write(carro3)
                archivo.write(",")
                archivo.write(",")
                archivo.write(dia)
                archivo.write(",")
                archivo.write(mes)
                archivo.write(",")
                archivo.write(año)
                archivo.write(",")
                archivo.write(",")
                archivo.write(hora)
                archivo.write(",")        
                archivo.write(minuto)
                archivo.write(",")
                archivo.write(segundo)
                archivo.write(",")
                archivo.write("\n")
                archivo.close()
            
    # Si el auto ha cruzado entre 440 y 460 abierto, se incrementará
    # en 1 el contador de auto

    # Visualización del conteo de autos
    cv2.drawContours(frame, [area_pts], -1, (255, 0, 255), 2)

    cv2.drawContours(frame, [area_pts2], -1, (255, 200, 255), 2)

    cv2.drawContours(frame, [area_pts3], -1, (200, 200, 255), 2)
    
    cv2.line(frame, (70, 220), (70, 255), (0, 255, 255), 1)
    cv2.rectangle(frame, (frame.shape[1]-490, 215), (frame.shape[1]-425, 260), (0, 255, 0), 2)
    cv2.putText(frame, str(car_counter), (frame.shape[1]-465, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)


    cv2.line(frame, (395, 275), (395,310), (0, 255, 255), 1)
    cv2.rectangle(frame, (frame.shape[1]-165, 270), (frame.shape[1]-100, 320), (0, 0, 255), 2)
    cv2.putText(frame, str(car_counter2), (frame.shape[1]-140, 305),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 2)

    cv2.line(frame, (225, 61), (225,96), (0, 0, 255), 1)
    cv2.rectangle(frame, (frame.shape[1]-335, 111), (frame.shape[1]-270, 66), (0, 250, 255), 2)
    cv2.putText(frame, str(car_counter3), (frame.shape[1]-310, 95),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 2)
    #cv2.imshow('f1', fgmask)
    #cv2.imshow('f2', fgmask2)
    #cv2.imshow('f3', fgmask3)
 
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1) & 0xFF
    if k ==27:
        break
cap.release()
cv2.destroyAllWindows()
