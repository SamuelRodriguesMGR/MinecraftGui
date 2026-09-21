
import time
import pyautogui
from PIL import Image
from pynput.mouse import Controller, Button

import threading
from pynput import keyboard
from SensorText import *
from LittleFunc import * 

import sounddevice as sd
import numpy as np


class MinecraftGui:

    def __init__(self):
        self.mouse = Controller()  
        self.running = False
        self.cycle_thread = None
        # получение угла
        self.sensor_angle = SensorText([352, 252, 521 - 351, 265 - 251], "screenshot_angle.png")
        # получение координат
        self.sensor_coord = SensorText([52, 198, 342, 14], "screenshot_coord.png")
        self.current_angle = ["", ""]
        self.current_coord = ["", "", ""]

        self.last_trigger = 0


    def on_press(self, key):
        try:
            print(f'Key {key.char} pressed')

        except AttributeError:
            print(f'Special key {key} pressed')

            if key == keyboard.Key.home:

                self.zombe()
                
            if key == keyboard.Key.end:
                self.custom_angle()

            if key == keyboard.Key.delete:
                # turn(1 * -600 * (True * 2 - 1), 0)
                self.ender_farm()

            if key == keyboard.Key.insert:
                self.fishing()


    def loop(self):
        # Функция для второго потока с циклом
        with sd.InputStream(callback=self.callback):
            print("Слушаю микрофон...")
            while self.running:
                pass

        # while self.running:
        #     # Проверка хп
        #     # self.check_health() 
        #     self.current_angle = self.sensor_angle.get_text()
        #     coord = self.sensor_coord.get_text()
        #     if coord and "" not in coord: 
        #         self.current_coord = [float(i) for i in coord]

        #     threading.Event().wait(0.05) # небольшую задержку, чтобы не перегружать CPU


    def detect_noise(self, indata): # 536870913
        THRESHOLD = 0.02  # чувствительность (подбирается)
        DURATION = 0.5    # секунды
        volume_norm = np.linalg.norm(indata) / len(indata)
        if volume_norm > THRESHOLD:
            if time.time() - self.last_trigger > 1:
                print("ШУМ ОБНАРУЖЕН!")
                self.fishing()
                self.last_trigger = time.time()
            
    def callback(self, indata, frames, time, status):
        self.detect_noise(indata)

    def fishing(self):
        self.mouse.press(Button.right)
        self.mouse.release(Button.right)
        time.sleep(0.1)
        self.mouse.press(Button.right)
        self.mouse.release(Button.right)


    def zombe(self):
        while self.running:
            pyautogui.keyDown("w")
            time.sleep(4)
            pyautogui.keyUp("w")
            time.sleep(4)

    def bore(self):
        while self.running:
            self.mouse.press(Button.right)
            time.sleep(0.05)
            self.mouse.release(Button.right)
            time.sleep(4)

    def leftm(self):
        while True:
            self.mouse.press(Button.left)
            time.sleep(0.06)
            self.mouse.release(Button.left)

    def hyperloop(self):
        pyautogui.keyUp("shift")
        while True:
            pyautogui.keyDown("shift")
            pyautogui.keyDown("s")
            self.mouse.press(Button.right)
        
    def ender_farm(self):
        while self.running:
            self.mouse.press(Button.left)
            time.sleep(0.2)
            self.mouse.release(Button.left)
            time.sleep(0.6)
    
    def custom_angle(self):
        angle_complated = False
        val = 1

        while not angle_complated:
            if not self.current_angle[0]:
                break
            # Нормализуем угол от -180 до 180, затем округляем до ближайших 90 градусов
            normalized_angle = (float(self.current_angle[0]) + 180) % 360 - 180
            first_angle = round(normalized_angle / 90) * 90

            AngleX = float(self.current_angle[0])

            if AngleX > first_angle + 0.1:
                turn(-val, 0)
            elif AngleX < first_angle - 0.1:
                turn(val, 0)
            else:
                angle_complated = True

            if (first_angle == 180 and AngleX == -180) or (first_angle == -180 and AngleX == 180):
                angle_complated = True

    def mining(self):
        counter_line = 0

        on_left = True
        distance = 15
        step_torch = 6
        angle = -600

        while self.running: 
            if not self.current_coord[0]:
                break
            

            num = int(str(self.current_coord[2]).split(".")[1][0])
            # Сдвиг для начала линии
            if num > 6:
                pyautogui.keyDown("d")
                pyautogui.keyUp("d")
            if num < 4:
                pyautogui.keyDown("a")
                pyautogui.keyUp("a")
            print(num)
            
            self.custom_angle()

            # Нужная позиция, куда копать
            target_pos = int(self.current_coord[0] + distance * (on_left * 2 -1))
            
            if on_left:
                target_pos -= 1

            while (on_left and self.current_coord[0] < target_pos) or \
            (not on_left and self.current_coord[0] > target_pos):
                pyautogui.keyDown("w")
                # self.mouse.press(Button.left)

                # time.sleep(0.07)
                # pyautogui.keyUp("w")
                # self.mouse.release(Button.left)

            pyautogui.keyUp("w")
            self.mouse.release(Button.left)

            turn(angle * (on_left * 2 - 1), 0)
            self.custom_angle()
            
            time.sleep(1)
            target_pos = int(self.current_coord[2] + -1)

            while self.current_coord[2] > target_pos:
                pyautogui.keyDown("w")
                # self.mouse.press(Button.left)

                # time.sleep(0.1)
                # pyautogui.keyUp("w")
                # self.mouse.release(Button.left)

            pyautogui.keyUp("w")
            self.mouse.release(Button.left)

            # Повернулись
            turn(angle * (on_left * 2 - 1), 0)

            on_left = not on_left
            counter_line += 1

            time.sleep(0.05)



    def activate(self):
        self.running = True
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        # Создание и запуск второго потока для цикла
        cycle_thread = threading.Thread(target=self.loop)
        cycle_thread.daemon = True  # Поток демона завершится с основным потоком
        cycle_thread.start()

        listener.join()
        
MG = MinecraftGui()
MG.activate()