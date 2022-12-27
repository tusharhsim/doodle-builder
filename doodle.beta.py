import cv2
import time
import math
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

width = 1280#cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = 720#cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

from tkinter import *
tk = Tk()
#tk.attributes('-alpha',0.2)
tk.wm_attributes("-transparentcolor", "white")
canvas = Canvas(tk, width = width, height = height)
canvas.configure(bg='white')
tk.title("arhsim")
canvas.pack()
radius = 26
color = 'black'
colour = (0,0,0)

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    try:
      for hand_landmarks in results.multi_hand_landmarks:
        INDEX_FINGER_TIP = [int(hand_landmarks.landmark[8].x * width), int(hand_landmarks.landmark[8].y * height)]
        THUMB_MCP = [int(hand_landmarks.landmark[2].x * width), int(hand_landmarks.landmark[2].y * height)]
        THUMB_TIP = [int(hand_landmarks.landmark[4].x * width), int(hand_landmarks.landmark[4].y * height)]
        INDEX_FINGER_MCP = [int(hand_landmarks.landmark[5].x * width), int(hand_landmarks.landmark[5].y * height)]
        MIDDLE_FINGER_TIP = [int(hand_landmarks.landmark[12].x * width), int(hand_landmarks.landmark[12].y * height)]

        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        try:
          s_point = (lx, ly)
        except:
          lx, ly = INDEX_FINGER_TIP[0], INDEX_FINGER_TIP[1]
        e_point = (INDEX_FINGER_TIP[0], INDEX_FINGER_TIP[1])

        l_click_angle = abs(math.degrees(math.atan2(INDEX_FINGER_TIP[1]-THUMB_MCP[1], INDEX_FINGER_TIP[0]-THUMB_MCP[0]) - math.atan2(THUMB_TIP[1]-THUMB_MCP[1], THUMB_TIP[0]-THUMB_MCP[0])))
        r_click_angle = abs(math.degrees(math.atan2(INDEX_FINGER_TIP[1]-INDEX_FINGER_MCP[1], INDEX_FINGER_TIP[0]-INDEX_FINGER_MCP[0]) - math.atan2(MIDDLE_FINGER_TIP[1]-INDEX_FINGER_MCP[1], MIDDLE_FINGER_TIP[0]-INDEX_FINGER_MCP[0])))

        if l_click_angle < 30 and r_click_angle > 30:
          canvas.create_line(lx, ly, INDEX_FINGER_TIP[0], INDEX_FINGER_TIP[1], fill = color, width=6)
        elif r_click_angle < 30:
          canvas.create_oval(INDEX_FINGER_TIP[0]-radius, INDEX_FINGER_TIP[1]-radius, INDEX_FINGER_TIP[0]+radius, INDEX_FINGER_TIP[1]+radius, fill='white', outline="white")

        cv2.circle(image, e_point, radius, (0,255,255), 2)
        cv2.rectangle(image, (0, 0), (320, 24), (0,0,0), -1)
        cv2.rectangle(image, (320, 0), (640, 24), (0,0,255), -1)
        cv2.rectangle(image, (640, 0), (960, 24), (0,255,0), -1)
        cv2.rectangle(image, (960, 0), (1280, 24), (255,0,0), -1)
        cv2.putText(image, color, (24,48), cv2.FONT_HERSHEY_SIMPLEX, 1, colour,2)
        cv2.imshow('arhsim', image)
        tk.update()
        lx, ly = INDEX_FINGER_TIP[0], INDEX_FINGER_TIP[1]

    except:
      cv2.imshow('arhsim', image)
      tk.update()
      continue

    if INDEX_FINGER_TIP[1] < 24:
      if INDEX_FINGER_TIP[0] in range(0,320):
        color = 'black'
        colour = (0,0,0)
      if INDEX_FINGER_TIP[0] in range(320,640):
        color = 'red'
        colour = (0,0,255)
      if INDEX_FINGER_TIP[0] in range(640,960):
        color = 'green'
        colour = (0,255,0)
      if INDEX_FINGER_TIP[0] in range(960,1280):
        color = 'blue'
        colour = (255,0,0)

    if l_click_angle > 120:
      print('gesture exit')
      break

    if cv2.waitKey(5) & 0xFF == 27:
      break

  cap.release()
  tk.destroy()
  cv2.destroyAllWindows()
