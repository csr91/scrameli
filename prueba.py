import pyautogui
import time
import random

def scroll_up():
    screen_height = pyautogui.size()[1]
    scroll_amount = -screen_height
    pyautogui.scroll(scroll_amount, x=pyautogui.position()[0], y=pyautogui.position()[1])

def scroll_down():
    screen_height = pyautogui.size()[1]
    scroll_amount = screen_height
    pyautogui.scroll(scroll_amount, x=pyautogui.position()[0], y=pyautogui.position()[1])

def main():
    pyautogui.hotkey('alt', 'tab')
    time.sleep(1.5)

    # Realizar dos scrolls aleatorios (uno hacia arriba y otro hacia abajo)
    scroll_down()
    scroll_up()
    scroll_down()
    scroll_up()

if __name__ == "__main__":
    main()
