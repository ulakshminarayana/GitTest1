import cv2
import numpy as np
import socket
import struct
from io import BytesIO
from kivy.app import App
from kivy.uix.button import Button

class MainApp(App):
    def build(self):
        # Capture frame
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.1.160', 8080))

        while cap.isOpened():
            _, frame = cap.read()

            memfile = BytesIO()
            np.save(memfile, frame)
            memfile.seek(0)
            data = memfile.read()

            # Send form byte array: frame size + frame content
            client_socket.sendall(struct.pack("L", len(data)) + data)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        return Button(text="Hello World")


MainApp().run()