import threading
import subprocess
import cv2
import imutils
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Update the following variables with your email account details
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'manojkumarkalyanapu777@gmail.com'
EMAIL_PASSWORD = 'rltwypaqrwaldwgl'
RECIPIENT_EMAIL = 'manojkumarkalyanapu@gmail.com'

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0


def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("ALARM")
        cv2.imwrite("alarm_photo.jpg", frame)
        subprocess.run(["aplay", "/usr/share/sounds/alsa/Front_Center.wav"])
        send_email_with_photo("alarm_photo.jpg")
    alarm = False


def send_email_with_photo(photo_path):
    # Create a multipart message and set the headers
    message = MIMEMultipart()
    message['From'] = 'manojkumarkalyanapu777@gmail.com'
    message['To'] = 'manojkumarkalyanapu@gmail.com'
    message['Subject'] = 'Alarm Photo'

    # Attach the photo to the email
    with open(photo_path, 'rb') as photo_file:
        image = MIMEImage(photo_file.read())
    message.attach(image)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('manojkumarkalyanapu777@gmail.com', 'rltwypaqrwaldwgl')
        server.sendmail('manojkumarkalyanapu777@gmail.com', 'manojkumarkalyanapu@gmail.com', message.as_string())


while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshold.sum() > 1:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1
        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)

    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
