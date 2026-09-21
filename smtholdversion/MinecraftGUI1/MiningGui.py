
import time
import pyautogui
import threading
from PIL import Image
from pynput.mouse import Controller, Button
from pynput import keyboard
from SensorCords import *



class MiningGui:
    ROTATE_90_ANGLE = -600 
    COORD_BUTTON_EXIT = (957, 506)
    # Путь картинки сердца
    HEART_SCREEN_PATH = "debug/screenshot_heart.png"

    def __init__(self):
        self.mouse = Controller()  
        self.sensor_coord = SensorCoord([52, 198, 342, 14], "screenshot_coord.png")

        # Позиция игрока
        self.current_position = [0, 0, 0]
        self.running = True


    def save_screenshot(self, rect : tuple):
        pyautogui.screenshot(region=rect).save(MiningGui.HEART_SCREEN_PATH)


    def press(self, keys_keyboard : list = [], keys_mouse : list = [], delay: float = 0.01):
        for key in keys_keyboard:
            pyautogui.keyDown(key)

        for key in keys_mouse:
            self.mouse.press(key)

        time.sleep(delay)

        for key in keys_keyboard:
            pyautogui.keyUp(key)
            
        for key in keys_mouse:
            self.mouse.release(key)


    def on_press(self, key):
        try:
            print(f'Key {key.char} pressed')

        except AttributeError:
            print(f'Special key {key} pressed')

            if key == keyboard.Key.home:
                self.composter()
            if key == keyboard.Key.end:
                self.ender_farm()
            if key == keyboard.Key.insert:
                self.put_torch()
            if key == keyboard.Key.page_down:
                self.check_health()
            if key == keyboard.Key.page_up:
                self.mining()
            if key == keyboard.Key.delete:
                self.destroing()


    def on_release(self, key):
        if key == "nope":
            return False
        

    def turn(self, vectx, vecty):
        x, y = pyautogui.position()
        pyautogui.moveTo(x+vectx, y+vecty)


    def leave_to_menu(self):
        self.press(["esc"])
        pyautogui.moveTo(MiningGui.COORD_BUTTON_EXIT)
        pyautogui.click()


    def put_torch(self):
        self.press(["9"])
        self.turn(0, 600)
        self.press([], [Button.right])
        time.sleep(0.1)
        self.turn(0, -400)
        self.press(["4"])
    

    def check_health(self):
        self.save_screenshot((922, 952, 18, 18))
        color_heart = (255, 19, 19)
        color_space = (40, 40, 40) # удар (255, 161, 161)
        img = Image.open(MiningGui.HEART_SCREEN_PATH)
        color = img.getpixel((12, 6))

        if color == color_space:
            self.leave_to_menu()

    def cycle_worker(self):
        # Функция для второго потока с циклом

        while True:
            # Проверка хп
            # self.check_health()

            coord = self.sensor_coord.get_coord()
            if coord and "" not in coord: 
                self.current_position = [float(i) for i in coord]
                    
            # Добавьте небольшую задержку, чтобы не перегружать CPU
            threading.Event().wait(0.05)  # Задержка 50 мс

    
    def mining(self):
        counter_line = 0

        on_left = False
        distance = 15
        direction_way = 1
        step_torch = 6

        vector_trans = 0
        vector_line = 2

        while self.running:

            # Поставили факел
            if counter_line % step_torch == 0: 
                self.put_torch()

            target_pos = int(self.current_position[vector_line] + distance * (on_left * 2 - 1))
            
            if on_left:
                target_pos -= 1

            center_pos = int(self.current_position[vector_line] + (distance // 2) * (on_left * 2 - 1))

            torched = False
            while (on_left and self.current_position[vector_line] < target_pos) or \
                (not on_left and self.current_position[vector_line] > target_pos):
                
                # Поставили факел
                if int(self.current_position[vector_line]) == center_pos and (not torched) and (counter_line + 3) % step_torch == 0:
                    torched = True
                    pyautogui.keyUp("w")
                    self.mouse.release(Button.left)
                    self.put_torch()

                pyautogui.keyDown("w")
                self.mouse.press(Button.left)

                # time.sleep(0.08)

                # pyautogui.keyUp("w")
                # self.mouse.release(Button.left)


            pyautogui.keyUp("w")
            pyautogui.keyUp("space")
            self.mouse.release(Button.left)

            # Поставили факелw
            if counter_line % step_torch == 0: 
                self.put_torch()

            # Повернулись
            self.turn(direction_way * MiningGui.ROTATE_90_ANGLE * (on_left * 2 - 1), 0)

            target_pos = int(self.current_position[vector_trans] + direction_way)

            if direction_way == 1:
                target_pos -= 1
            
            while self.current_position[vector_trans] < target_pos:
                pyautogui.keyDown("w")
                self.mouse.press(Button.left)

                time.sleep(0.1)

                pyautogui.keyUp("w")
                self.mouse.release(Button.left)


            pyautogui.keyUp("w")
            self.mouse.release(Button.left)

            # Повернулись
            self.turn(direction_way * MiningGui.ROTATE_90_ANGLE * (on_left * 2 - 1), 0)

            on_left = not on_left
            counter_line += 1



    def activate(self):
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

        # Создание и запуск второго потока для цикла
        cycle_thread = threading.Thread(target=self.cycle_worker)
        cycle_thread.daemon = True  # Поток демона завершится с основным потоком
        cycle_thread.start()

        listener.join()


    def composter(self):
        while self.running:
            # self.press(['shift'], [], 0.001)
            self.mouse.press(Button.right)
        self.mouse.release(Button.right)

    def ender_farm(self):
        pyautogui.keyUp("shift")
        while self.running:
            pyautogui.keyDown("shift")
            self.press([], [Button.left], 0.2)
            time.sleep(0.6)
    
    def destroing(self):
        self.mouse.press(Button.left)


    def rotating(self):
        while True:
            self.turn(-32000, 0)
            pyautogui.keyDown("shift")
            pyautogui.keyUp("shift")
    
    def moving(self):
        while True:
            self.press(keys_keyboard=["w"], delay=0.1)
            self.press(keys_keyboard=["s"], delay=0.1)

    def hyperloop(self):
        pyautogui.keyUp("shift")
        while True:
            pyautogui.keyDown("shift")
            pyautogui.keyDown("s")
            self.mouse.press(Button.right)


    def print_mouse_pos(self):
        x, y = pyautogui.position()
        # print(x, y)


mg = MiningGui()
mg.activate()