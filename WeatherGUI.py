import tkinter as tk
from tkinter import ttk, messagebox
import json
from RequestApi import RequestApi
from app import get_weather_by_loction

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
        
        # 行政區選擇
        ttk.Label(self.weather_frame, text="選擇行政區:").grid(row=1, column=0, padx=5, pady=5)
        self.district_var = tk.StringVar()
        self.district_combo = ttk.Combobox(self.weather_frame, textvariable=self.district_var)
        self.district_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # 天氣元素選擇
        ttk.Label(self.weather_frame, text="選擇天氣元素:").grid(row=2, column=0, padx=5, pady=5)
        self.elements_var = tk.StringVar(value="天氣預報綜合描述")
        self.elements_combo = ttk.Combobox(self.weather_frame, textvariable=self.elements_var)
        self.elements_combo['values'] = [
            "天氣預報綜合描述",
            "平均溫度",
            "最高溫度",
            "最低溫度",
            "平均相對濕度",
            "天氣現象",
            "紫外線指數",
            "最高體感溫度",
            "降雨機率",
            "風向"
        ]
        self.elements_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # 查詢按鈕
        ttk.Button(self.weather_frame, text="查詢天氣", command=self.get_weather).grid(row=3, column=0, columnspan=2, pady=10)
        
        # 結果顯示區域
        self.weather_result = tk.Text(self.weather_frame, height=20, width=80)
        self.weather_result.grid(row=4, column=0, columnspan=2, pady=10)
        
        # 綁定城市選擇事件
        self.city_combo.bind('<<ComboboxSelected>>', self.update_districts)
        
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
        
    def update_districts(self, event=None):
        city = self.city_var.get()
        result = self.api.getWeatherByCity(city, 7)
        if result['status']:
            data = result['data']
            locations = data["records"]["Locations"]
            if locations:
                districts = [loc["LocationName"] for loc in locations[0].get("Location", [])]
                self.district_combo['values'] = districts
                if districts:
                    self.district_combo.current(0)
        
    def format_weather_data(self, data):
        if not data:
            return "無法獲取天氣資料"
            
        result = []
        result.append(f"城市: {data['city']}")
        result.append(f"行政區: {data['district']}")
        result.append("\n天氣預報:")
        
        for weather in data['weather']:
            element_type = weather['elementType']
            result.append(f"\n{element_type}:")
            
            for value in weather['elementValue']:
                date = value['date']
                period = value['period']
                values = value['values']
                
                result.append(f"\n日期: {date} ({period})")
                for key, val in values.items():
                    result.append(f"  {key}: {val}")
                    
        return "\n".join(result)
        
    def format_earthquake_data(self, data):
        if not data:
            return "無法獲取地震資料"
            
        result = []
        for earthquake in data['records']['earthquake']:
            result.append(f"地震時間: {earthquake['reportContent']}")
            result.append(f"震央位置: {earthquake['epicenter']['location']}")
            result.append(f"地震規模: {earthquake['magnitude']['magnitudeValue']}")
            result.append(f"地震深度: {earthquake['depth']['value']} 公里")
            result.append(f"最大震度: {earthquake['intensity']['shakingArea'][0]['areaName']} {earthquake['intensity']['shakingArea'][0]['areaIntensity']}")
            result.append("-" * 50)
            
        return "\n".join(result)
        
    def get_weather(self):
        city = self.city_var.get()
        district = self.district_var.get()
        element = self.elements_var.get()
        
        if not district:
            messagebox.showerror("錯誤", "請選擇行政區")
            return
            
        result = get_weather_by_loction(city, district, [element])
        if result:
            formatted_data = self.format_weather_data(result)
            self.weather_result.delete(1.0, tk.END)
            self.weather_result.insert(tk.END, formatted_data)
        else:
            messagebox.showerror("錯誤", "無法獲取天氣資料")
            
    def get_earthquake(self):
        mode_type = int(self.earthquake_type.get())
        
        result = self.api.getEarthquake(mode_type)
        if result['status']:
            formatted_data = self.format_earthquake_data(result['data'])
            self.earthquake_result.delete(1.0, tk.END)
            self.earthquake_result.insert(tk.END, formatted_data)
        else:
            messagebox.showerror("錯誤", result['message'])

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop() 