import pyautogui

screenSize = pyautogui.size()


def main():
    sleep_time = 30
    x = 0
    # in a infinite loop, keep going to "Start" menu and open Windows 
    # and again close it. then, wait for a sleep time.
    while True: 
        pyautogui.moveTo(5, screenSize.width, duration=1)
        pyautogui.click()
        pyautogui.sleep(1)
        pyautogui.click()
        x += sleep_time
        print(f"Sleep for {x} seconds")
        pyautogui.sleep(sleep_time)


main()
