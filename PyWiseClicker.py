#连点器，典型情况下最高连点速度不大于20cps

import tkinter as tk
from tkinter import ttk
import pyautogui
from pynput import mouse, keyboard
import configparser
import time
import random
import threading
from PIL import Image, ImageTk
import os 

class PyWiseClicker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyWiseClicker")
        self.geometry("400x400")
        self.resizable(False, False)
        self.is_active = False
        self.clicking = False
        self.stop_event = threading.Event()
        self.config = configparser.ConfigParser()
        self.load_config()
        self.create_widgets()
        self.mouse_listener = None
        self.keyboard_listener = None
        self.start_listeners()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        self.interval_frame = ttk.Frame(self)
        self.interval_frame.pack(pady=5, fill='x', padx=10)
        self.interval_label = ttk.Label(self.interval_frame, text="基础间隔: 0.10s")
        self.interval_label.pack(side='left')
        self.interval_scale = ttk.Scale(
            self.interval_frame,
            from_=0.01,
            to=1.0,
            value=self.base_interval,
            command=lambda v: self.interval_label.config(text=f"基础间隔: {float(v):.2f}s")
        )
        self.interval_scale.pack(side='right', fill='x', expand=True, padx=5)
        self.error_frame = ttk.Frame(self)
        self.error_frame.pack(pady=5, fill='x', padx=10)
        self.error_label = ttk.Label(self.error_frame, text="随机误差: 0.00s")
        self.error_label.pack(side='left')
        self.error_scale = ttk.Scale(
            self.error_frame,
            from_=0.0,
            to=0.5,
            value=self.error_interval,
            command=lambda v: self.error_label.config(text=f"随机误差: {float(v):.2f}s")
        )
        self.error_scale.pack(side='right', fill='x', expand=True, padx=5)
        self.btn_frame = ttk.Frame(self)
        self.btn_frame.pack(pady=15)
        self.activate_btn = ttk.Button(
            self.btn_frame,
            text="▶ 激活",
            width=15,
            command=self.toggle_activation
        )
        self.activate_btn.pack(side='left', padx=5)
        self.status_var = tk.StringVar(value="当前状态：等待激活")
        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.pack(pady=10)
    
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "Reimu.png")
            image = Image.open(image_path)
            self.photo = ImageTk.PhotoImage(image) 
            self.image_label = ttk.Label(self, image=self.photo)
            self.image_label.pack(pady=10)
        except Exception as e:
            print(f"图片加载失败: {str(e)}")
            self.image_label = ttk.Label(self, text="[图片加载失败]")
            self.image_label.pack(pady=10)
            self.footer_label = ttk.Label(self, text="版本v1.0.2 | Author:Sabour1nX ,and Some AI assistances", font=("宋体", 8), foreground="gray")
            self.footer_label.pack(side=tk.BOTTOM, pady=5)

    def load_config(self):
        self.config.read('PyWiseClicker.ini')
        if not self.config.has_section('Settings'):
            self.base_interval = 0.10
            self.error_interval = 0.00
        else:
            self.base_interval = self.config.getfloat('Settings', 'base_interval', fallback=0.10)
            self.error_interval = self.config.getfloat('Settings', 'error_interval', fallback=0.00)

    def save_config(self):
        if not self.config.has_section('Settings'):
            self.config.add_section('Settings')
        self.config.set('Settings', 'base_interval', str(round(self.interval_scale.get(), 2)))
        self.config.set('Settings', 'error_interval', str(round(self.error_scale.get(), 2)))
        
        with open('PyWiseClicker.ini', 'w') as f:
            self.config.write(f)

    def toggle_activation(self):
        self.is_active = not self.is_active
        if self.is_active:
            self.activate_btn.config(text="⏸ 停用")
            self.status_var.set("当前状态：已激活 - 按住侧键/中键开始连点")
            self.save_config()
        else:
            self.activate_btn.config(text="▶ 激活")
            self.status_var.set("当前状态：已停用")
            self.stop_clicking()

    def start_listeners(self):
        self.mouse_listener = mouse.Listener(on_click=self.handle_mouse)
        self.keyboard_listener = keyboard.Listener(on_press=self.handle_keyboard)
        self.mouse_listener.daemon = True
        self.keyboard_listener.daemon = True
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def handle_mouse(self, x, y, button, pressed):
        if not self.is_active:
            return
        target_buttons = [mouse.Button.x1, mouse.Button.x2, mouse.Button.middle]
        
        if button in target_buttons:
            if pressed:
                self.start_clicking()
            else:
                self.stop_clicking()

    def handle_keyboard(self, key):
        try:
            if key == keyboard.Key.f10:
                self.stop_clicking()
                self.status_var.set("操作已被F10强制终止")
        except AttributeError:
            pass

    def start_clicking(self):
        if self.clicking:
            return 
        self.clicking = True
        self.stop_event.clear()
        click_thread = threading.Thread(target=self.click_loop)
        click_thread.daemon = True
        click_thread.start()

    def stop_clicking(self):
        self.clicking = False
        self.stop_event.set()

    def click_loop(self):
        while not self.stop_event.is_set() and self.is_active:
            base = self.interval_scale.get()
            error = self.error_scale.get()
            actual_interval = base + random.uniform(-error, error)
            actual_interval = max(0.01, actual_interval)  # 防止负值
            pyautogui.click(button='left')
            time.sleep(actual_interval)

    def on_close(self):
        self.stop_clicking()
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.destroy()

if __name__ == "__main__":
    pyautogui.PAUSE = 0.01
    app = PyWiseClicker()
    app.mainloop()