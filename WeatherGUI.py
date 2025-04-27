import tkinter as tk
from tkinter import ttk, messagebox
import json
from RequestApi import RequestApi

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("氣象預報系統")
        self.root.geometry("800x600")
        
        # 初始化 API
        self.api = RequestApi()
        
        # 創建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 創建標籤頁
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 天氣預報頁面
        self.weather_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.weather_frame, text="天氣預報")
        
        # 地震資訊頁面
        self.earthquake_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.earthquake_frame, text="地震資訊")
        
        self.setup_weather_page()
        self.setup_earthquake_page()
        
    def setup_weather_page(self):
        # 城市選擇
        ttk.Label(self.weather_frame, text="選擇城市:").grid(row=0, column=0, padx=5, pady=5)
        self.city_var = tk.StringVar()
        self.city_combo = ttk.Combobox(self.weather_frame, textvariable=self.city_var)
        self.city_combo['values'] = list(self.api.cityApi.keys())
        self.city_combo.grid(row=0, column=1, padx=5, pady=5)
        self.city_combo.current(0)
        
        # 天數選擇
        ttk.Label(self.weather_frame, text="預報天數:").grid(row=1, column=0, padx=5, pady=5)
        self.days_var = tk.StringVar(value="3")
        ttk.Radiobutton(self.weather_frame, text="3天", variable=self.days_var, value="3").grid(row=1, column=1, padx=5, pady=5)
        ttk.Radiobutton(self.weather_frame, text="7天", variable=self.days_var, value="7").grid(row=1, column=2, padx=5, pady=5)
        
        # 查詢按鈕
        ttk.Button(self.weather_frame, text="查詢天氣", command=self.get_weather).grid(row=2, column=0, columnspan=3, pady=10)
        
        # 結果顯示區域
        self.weather_result = tk.Text(self.weather_frame, height=20, width=80)
        self.weather_result.grid(row=3, column=0, columnspan=3, pady=10)
        
    def setup_earthquake_page(self):
        # 地震類型選擇
        ttk.Label(self.earthquake_frame, text="地震類型:").grid(row=0, column=0, padx=5, pady=5)
        self.earthquake_type = tk.StringVar(value="0")
        ttk.Radiobutton(self.earthquake_frame, text="小區域有感地震", variable=self.earthquake_type, value="0").grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(self.earthquake_frame, text="顯著有感地震", variable=self.earthquake_type, value="1").grid(row=0, column=2, padx=5, pady=5)
        
        # 查詢按鈕
        ttk.Button(self.earthquake_frame, text="查詢地震", command=self.get_earthquake).grid(row=1, column=0, columnspan=3, pady=10)
        
        # 結果顯示區域
        self.earthquake_result = tk.Text(self.earthquake_frame, height=20, width=80)
        self.earthquake_result.grid(row=2, column=0, columnspan=3, pady=10)
        
    def get_weather(self):
        city = self.city_var.get()
        days = int(self.days_var.get())
        
        result = self.api.getWeatherByCity(city, days)
        if result['status']:
            # 格式化顯示天氣資料
            weather_data = result['data']
            self.weather_result.delete(1.0, tk.END)
            self.weather_result.insert(tk.END, json.dumps(weather_data, indent=2, ensure_ascii=False))
        else:
            messagebox.showerror("錯誤", result['message'])
            
    def get_earthquake(self):
        mode_type = int(self.earthquake_type.get())
        
        result = self.api.getEarthquake(mode_type)
        if result['status']:
            # 格式化顯示地震資料
            earthquake_data = result['data']
            self.earthquake_result.delete(1.0, tk.END)
            self.earthquake_result.insert(tk.END, json.dumps(earthquake_data, indent=2, ensure_ascii=False))
        else:
            messagebox.showerror("錯誤", result['message'])

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop() 