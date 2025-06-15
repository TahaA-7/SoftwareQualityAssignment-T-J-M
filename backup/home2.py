import msvcrt

import platform, os

class interface_for_python:
    def home_screen():
        pass

    def on_key():
        print("Press a key (1 or 2):")

        while True:
            key = msvcrt.getch().decode('utf-8')

            if key == '1':
                print('You pressed 1')
            elif key == '2':
                print('You pressed 2')
            elif key == 'q':
                break
            else:
                print(f'You pressed something else: {key}')


if __name__ == '__main__':
    if platform.system() == 'Windows':
        obj = interface_for_python()
        interface_for_python.home_screen()
