from ultralytics import YOLO
import streamlit as st
import cv2
import settings


def load_model(model_path):
    return YOLO(model_path)


def play_webcam(conf, model):
    cap = cv2.VideoCapture(settings.WEBCAM_PATH)
    st_frame = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model.predict(frame, conf=conf)
        annotated = results[0].plot()
        st_frame.image(annotated, channels="BGR", use_column_width=True)

    cap.release()
