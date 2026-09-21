import pyautogui
from pynput import keyboard
from pynput.mouse import Controller, Button
import threading
import time
import sounddevice as sd
from SensorText import SensorText


pyautogui.FAILSAFE = False

def turn(vectx, vecty):
    x, y = pyautogui.position()
    # pyautogui.moveRel(-100, 0, duration=0.1)
    pyautogui.moveTo(vectx, vecty)


class MineGui:

    def __init__(self):
        self.mouse = Controller()  

        self.running = True
        self.paused = True

        self.couter : int = 0

        self.current_position : list[int] = [0, 0, 0]
        self.sensor_position = SensorText([1512, 202, 402, 14], "screenshot_coords.png")

        self.counter_line = 0
        self.flag_left : bool = True # когда игрок доходит до конца линии, нужно повернуться, чтобы начать ломать новую линию
        self.ANGLE : int = -600
        self.DISTANTE : int = 15

    def run(self):
        threading.Thread(target=self.worker, daemon=True).start()
        threading.Thread(target=self.worker2, daemon=True).start()

        print("F8 — пауза/продолжить")
        print("F9 — остановить")

        with keyboard.Listener(on_press=self._on_press) as listener:
            listener.join()
    
    def worker(self):
        while self.running:
            if not self.paused:
                # self._auto_boor()
                self._mob_farm()
                # self._auto_mining()

            time.sleep(0.03)

    def worker2(self):
        while self.running:
            self._getting_pos()

            time.sleep(0.03)


    def _on_press(self, key):
        if key == keyboard.Key.f8:
            self.paused = not self.paused
            self._reset_actions()
            print("Пауза" if self.paused else "Работа")

        elif key == keyboard.Key.f9:
            self.running = False
            self._reset_actions()
            print("Остановка")
            return False

    def _reset_actions(self):
        pyautogui.keyUp("w")
        self.mouse.release(Button.left)


    def _getting_pos(self):
        coord = self.sensor_position.get_text()
        if coord and "" not in coord: 
            self.current_position = [float(i) for i in coord]

    def _mob_farm(self):
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        time.sleep(0.7)
        turn(-300, 0.1)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        time.sleep(0.7)
        turn(-300, 0.1)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        time.sleep(0.7)
        turn(300, 0.1)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        time.sleep(0.7)
        turn(300, 0.1)

    def _auto_boor(self):
        self.couter += 1
        self.mouse.press(Button.right)
        self.mouse.release(Button.right)
        print(self.couter)
        time.sleep(5)

    def _auto_mining(self):

        # Нужная позиция, куда копать
        target_pos = int(self.current_position[2] + self.DISTANTE * (self.flag_left * 2 - 1))

        if self.flag_left:
            target_pos -= 1

        while (self.flag_left and self.current_position[2] < target_pos) or \
            (not self.flag_left and self.current_position[2] > target_pos):

                if self.paused or not self.running:
                    self._reset_actions()
                    return
                
                pyautogui.keyDown("w")
                self.mouse.press(Button.left)

        self._reset_actions()

        turn(self.ANGLE * (self.flag_left * 2 - 1), 0)

        time.sleep(1)
        target_pos = self.current_position[0] + 0.3

        while self.current_position[0] < target_pos:
            
            if self.paused or not self.running:
                self._reset_actions()
                return
            
            pyautogui.keyDown("w")
            self.mouse.press(Button.left)

        self._reset_actions()

        turn(self.ANGLE * (self.flag_left * 2 - 1), 0)

        self.flag_left = not self.flag_left
        self.counter_line += 1

        time.sleep(0.05)
        

if __name__ == "__main__":
    mg = MineGui()
    mg.run()