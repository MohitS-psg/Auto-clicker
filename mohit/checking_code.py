from pynput import mouse, keyboard
import threading
import csv
import time
from datetime import datetime
import pyautogui

class AutoClicker:
    def __init__(self):
        self.position = (0, 0)
        self.clicks = 0
        self.threshold = 1
        self.tracking = False

    def get_position(self):
        input("Move your mouse to the desired position and press Enter...")
        from pyautogui import position
        self.position = position()
        print(f"[INFO] Position captured: {self.position}")

    def set_click_settings(self, clicks, threshold):
        self.clicks = clicks
        self.threshold = threshold
        print(f"[INFO] Clicks to perform: {clicks} in {threshold} seconds.")

    def start_clicking(self):
        from pyautogui import click
        if self.clicks <= 0:
            print("[WARNING] Number of clicks is zero or negative.")
            return
        interval = self.threshold / self.clicks
        print(f"[INFO] Starting clicks at {self.position} every {interval:.2f} seconds...")
        for i in range(self.clicks):
            click(self.position)
            print(f"Click {i+1}/{self.clicks}")
            time.sleep(interval)
        print("[INFO] Clicking completed.")

    def track_user_actions(self, toggle_key='t', stop_key='s', csv_file="mouse_actions.csv"):
        """
        Tracks mouse activity and saves to a CSV file.
        Toggle start/stop with 'toggle_key', and exit with 'stop_key'.
        """

        def log_to_csv(event_type, x, y, button='', extra_info=''):
            with open(csv_file, mode='a', newline='') as f:
                writer = csv.writer(f)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                writer.writerow([timestamp, event_type, x, y, button, extra_info])

        # Initialize CSV file with header
        with open(csv_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "event_type", "x", "y", "button", "extra_info"])

        def on_move(x, y):
            if self.tracking:
                log_to_csv('move', x, y)
                print(f"[MOVE] {(x, y)}")

        def on_click(x, y, button, pressed):
            if self.tracking:
                event_type = 'click_down' if pressed else 'click_up'
                log_to_csv(event_type, x, y, button=str(button))
                print(f"[{event_type.upper()}] {(x, y)} with {button}")

        def on_scroll(x, y, dx, dy):
            if self.tracking:
                log_to_csv('scroll', x, y, extra_info=f"{dx},{dy}")
                print(f"[SCROLL] at {(x, y)} by ({dx},{dy})")

        def on_press(key):
            try:
                if hasattr(key, 'char') and key.char == toggle_key:
                    self.tracking = not self.tracking
                    print(f"[TOGGLE] Tracking {'started' if self.tracking else 'paused'}")
                elif hasattr(key, 'char') and key.char == stop_key:
                    print("[STOP] Stopping tracker.")
                    return False  # Stops keyboard listener
            except:
                pass

        print(f"[INFO] Press '{toggle_key}' to start/pause tracking, '{stop_key}' to stop.")
        
        # Start listeners
        mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
        keyboard_listener = keyboard.Listener(on_press=on_press)

        mouse_listener.start()
        keyboard_listener.start()
        keyboard_listener.join()
        mouse_listener.stop()

        print(f"[INFO] Tracking complete. Log saved to: {csv_file}")

if __name__ == "__main__":
    clicker = AutoClicker()
    clicker.track_user_actions(toggle_key='t', stop_key='s', csv_file='tracked_log.csv')
