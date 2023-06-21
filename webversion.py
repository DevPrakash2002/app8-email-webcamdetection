import streamlit as st
import cv2
from datetime import datetime
import emaiiling as em

st.title("Motion Detection")

button_tap1 = st.button("Start Camera")
button_tap2 = st.button("Stop Camera")

first_frame = None
status_list = []
if button_tap1:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        status = 0
        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        now = datetime.now()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        if first_frame is None:
            first_frame = gray_frame_gau

        delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

        thresh_frame = cv2.threshold(delta_frame, 80, 255, cv2.THRESH_BINARY)[1]
        dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

        contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 10000:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            if rectangle.any():
                status = 1

        status_list.append(status)
        status_list = status_list[-2:]

        if status_list[0] == 1 and status_list[1] == 0:
            em.send_email()

        cv2.putText(img=frame, text=now.strftime('%A'), org=(30, 80),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(124, 142, 56),
                    thickness=2, lineType=cv2.LINE_AA)
        cv2.putText(img=frame, text=now.strftime('%H:%M:%S'), org=(30, 140),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(124, 142, 56),
                    thickness=2, lineType=cv2.LINE_AA)

        streamlit_image.image(frame)
        if button_tap2:
            break
    camera.release()


