import time
import pyautogui
from PIL import Image
from pynput.mouse import Controller, Button
import threading
from pynput import keyboard
from SensorText import *
from LittleFunc import * 

class MinecraftGui:

    def __init__(self):
        self.running = False
        self.stab_running = False  # отдельный флаг для стабилизации
        self.cycle_thread = None
        self.stab_thread = None
        self.sensor_angle = SensorText([352, 252, 521 - 351, 265 - 251], "screenshot_angle.png")
        self.current_angle = ["", ""]

    def on_press(self, key):
        try:
            print(f'Key {key.char} pressed')
        except AttributeError:
            print(f'Special key {key} pressed')

            if key == keyboard.Key.home:
                if not self.stab_running:
                    self.start_stab_cycle()
                else:
                    print("Stab cycle already running")
                
            if key == keyboard.Key.end:
                self.stop_stab_cycle()

    def start_stab_cycle(self):
        if not self.stab_running:
            self.stab_running = True
            self.stab_thread = threading.Thread(target=self.StabLoop)
            self.stab_thread.daemon = True
            self.stab_thread.start()
            print("Stab cycle STARTED")

    def stop_stab_cycle(self):
        if self.stab_running:
            self.stab_running = False
            if self.stab_thread and self.stab_thread.is_alive():
                self.stab_thread.join(timeout=1.0)
            print("Stab cycle STOPPED")

    def cycle_worker(self):
        while self.running:
            self.current_angle = self.sensor_angle.get_coord()
            threading.Event().wait(0.05)

    def StabLoop(self):
        if self.current_angle[0] == '':
            return
        
        first_angle = (round(float(self.current_angle[0]) / 90) * 90) % 360
        print(f"Stabilizing to angle: {first_angle}")

        while self.stab_running:  # используем отдельный флаг
            if self.current_angle[0] == '':
                break
                
            try:
                AngleX = float(self.current_angle[0])
                val = 5
                if AngleX > first_angle:
                    turn(-val, 0)
                elif AngleX < first_angle:
                    turn(val, 0)
                time.sleep(0.05)
            except (ValueError, IndexError):
                break

    def activate(self):
        self.running = True
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        # Запускаем поток для мониторинга угла
        self.cycle_thread = threading.Thread(target=self.cycle_worker)
        self.cycle_thread.daemon = True
        self.cycle_thread.start()

        listener.join()

    def deactivate(self):
        self.running = False
        self.stop_stab_cycle()
        if self.cycle_thread and self.cycle_thread.is_alive():
            self.cycle_thread.join(timeout=1.0)

def turn(vectx, vecty):
    pyautogui.move(vectx, vecty)  # используем move вместо moveTo для относительного перемещения
    
MG = MinecraftGui()
MG.activate()