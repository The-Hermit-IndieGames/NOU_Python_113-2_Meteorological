import customtkinter as ctk
from tkinter import messagebox
import json
from RequestApi import RequestApi
from app import get_weather_by_loction

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("氣象預報系統")
        self.root.geometry("1200x960") 
        
        # 設置主題
        self.theme_var = ctk.StringVar(value="blue")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme(self.theme_var.get())
        
        # 初始化 API
        self.api = RequestApi()
        
        # 主框架
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 標題
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="氣象預報系統",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))
        
        # 右上角外觀模式下拉選單
        self.appearance_mode = ctk.CTkOptionMenu(
            self.root,
            values=["system", "light", "dark"],
            command=self.change_appearance_mode,
            font=ctk.CTkFont(size=14),
            width=100,
            anchor="center",
            dynamic_resizing=False
        )
        self.appearance_mode.place(relx=0.97, rely=0.03, anchor="ne")
        self.appearance_mode.set(ctk.get_appearance_mode())
        
        # 標籤頁
        self.tabview = ctk.CTkTabview(self.main_frame, fg_color="transparent")
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 天氣預報頁
        self.weather_frame = self.tabview.add("天氣預報")
        
        # 地震資訊頁
        self.earthquake_frame = self.tabview.add("地震資訊")
        
        self.setup_weather_page()
        self.setup_earthquake_page()
        
    def setup_weather_page(self):
        # 內容主框架
        content_frame = ctk.CTkFrame(self.weather_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # 左側控制面板
        control_frame = ctk.CTkFrame(content_frame, fg_color="transparent", width=260)
        control_frame.pack(side="left", fill="y", padx=(0, 0), pady=0)
        
        # 城市選擇
        ctk.CTkLabel(
            control_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 15))
        
        city_names = list(self.api.cityApi.keys())
        self.city_var = ctk.StringVar()
        self.city_combo = ctk.CTkComboBox(
            control_frame,
            values=city_names,
            variable=self.city_var,
            width=200,
            height=35,
            font=ctk.CTkFont(size=13),
            command=self.update_districts
        )
        self.city_combo.pack(pady=5)
        self.city_combo.set(city_names[0])
        
        # 行政區選擇
        ctk.CTkLabel(
            control_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        
        self.district_var = ctk.StringVar()
        self.district_combo = ctk.CTkComboBox(
            control_frame,
            variable=self.district_var,
            width=200,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        self.district_combo.pack(pady=5)
        
        # 查詢按鈕
        self.query_button = ctk.CTkButton(
            control_frame,
            text="查詢",
            command=self.get_weather,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.query_button.pack(pady=20)
        
        # 右側結果顯示區域
        result_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        result_frame.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=0)
        
        # 查詢結果
        ctk.CTkLabel(
            result_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # 結果表格框架 - 使用滾動框架以確保所有內容都可查看
        self.weather_table_container = ctk.CTkFrame(result_frame, fg_color="transparent")
        self.weather_table_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 創建滾動框架來放置天氣表格
        self.weather_table_frame = ctk.CTkScrollableFrame(self.weather_table_container, width=800, height=600)
        self.weather_table_frame.pack(fill="both", expand=True)
        
        # 初始化行政區
        self.update_districts()
        
    def setup_earthquake_page(self):
        # 內容主框架
        content_frame = ctk.CTkFrame(self.earthquake_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # 左側控制面板
        control_frame = ctk.CTkFrame(content_frame, fg_color="transparent", width=260)
        control_frame.pack(side="left", fill="y", padx=(0, 0), pady=0)
        
        # 地震類型選擇
        ctk.CTkLabel(
            control_frame,
            text="地震類型:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        
        self.earthquake_type_var = ctk.StringVar(value="0")
        self.earthquake_type_combo = ctk.CTkComboBox(
            control_frame,
            values=["小區域有感地震", "顯著有感地震"],
            variable=self.earthquake_type_var,
            width=200,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        self.earthquake_type_combo.pack(pady=5)
        self.earthquake_type_combo.set("小區域有感地震")
        
        # 查詢按鈕
        self.query_button = ctk.CTkButton(
            control_frame,
            text="查詢",
            command=self.get_earthquake,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.query_button.pack(pady=20)
        
        # 右側結果顯示區域 - 使用框架來讓內容可以滾動
        result_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        result_container.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=0)
        
        # 結果標題
        ctk.CTkLabel(
            result_container,
            text="地震資訊查詢結果",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 5))
        
        # 結果顯示區域 - 使用框架來容納滾動視圖
        self.earthquake_result = ctk.CTkFrame(result_container, fg_color="transparent")
        self.earthquake_result.pack(fill="both", expand=True, padx=10, pady=10)
        
    def update_districts(self, event=None):
        city = self.city_var.get()
        result = self.api.getWeatherByCity(city, 7)
        if result['status']:
            data = result['data']
            locations = data["records"]["Locations"]
            if locations:
                districts = [loc["LocationName"] for loc in locations[0].get("Location", [])]
                self.district_combo.configure(values=districts)
                if districts:
                    self.district_combo.set(districts[0])
        
    def format_weather_data(self, data):
        for widget in self.weather_table_frame.winfo_children():
            widget.destroy()

        if not data:
            label = ctk.CTkLabel(self.weather_table_frame, text="無法獲取天氣資料")
            label.pack()
            return

        # 表格標題
        headers = ["時間", "溫度", "體感溫度", "相對溼度", "天氣狀況", "降雨機率", "蒲福風級", "風向"]
        header_widths = [100, 80, 80, 80, 120, 80, 80, 80]  # 自定義各列寬度
        
        header_frame = ctk.CTkFrame(self.weather_table_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=2, pady=5)
        
        for col, (header, width) in enumerate(zip(headers, header_widths)):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color="#2B5773", 
                text_color="white", 
                corner_radius=6,
                width=width,
                height=30
            )
            label.grid(row=0, column=col, padx=2, pady=2, sticky="nsew")
            header_frame.grid_columnconfigure(col, weight=0)  # 固定寬度

        # 填入天氣資料
        for row_idx, weather in enumerate(data['weather'], start=1):
            # 從時間字串中提取日期和時段
            time_parts = weather['time'].split(' ')
            if len(time_parts) == 2:
                date = time_parts[0]
                period = time_parts[1]
                # 只顯示月日
                date = date[5:]  # 去掉年份和第一個橫槓
                display_time = f"{date}\n{period}"
            else:
                display_time = weather['time']

            values = [
                display_time,
                weather['temperature'],
                weather['feels_like'],
                weather['humidity'],
                weather['weather'],
                weather['rain_chance'],
                weather['wind_scale'],
                weather['wind_direction']
            ]
            
            # 創建每行的框架
            row_frame = ctk.CTkFrame(self.weather_table_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=2, pady=2)

            for col_idx, (value, width) in enumerate(zip(values, header_widths)):
                wrap_width = width - 10
                
                label = ctk.CTkLabel(
                    row_frame,
                    text=value,
                    font=ctk.CTkFont(size=13),
                    wraplength=wrap_width,
                    corner_radius=6,
                    width=width,
                    height=40,
                    anchor="center"
                )
                label.grid(row=0, column=col_idx, padx=2, pady=2, sticky="nsew")
                row_frame.grid_columnconfigure(col_idx, weight=0)  # 固定寬度
                
            # 添加分隔線
            separator = ctk.CTkFrame(self.weather_table_frame, height=1, fg_color="#CCCCCC")
            separator.pack(fill="x", padx=5, pady=3)
          
    def get_weather(self):
        city = self.city_var.get()
        district = self.district_var.get()
        
        if not district:
            messagebox.showerror("錯誤", "請選擇行政區")
            return
            
        # 請求所有需要的氣象資料
        target_elements = [
            "平均溫度",
            "體感溫度",
            "相對濕度",
            "天氣現象",
            "降雨機率",
            "風向",
            "蒲福風級"
        ]
        
        result = get_weather_by_loction(city, district, target_elements)
        
        if result and isinstance(result, dict):
            weather_data = []
            try:
                # 建立時間點列表（未來7天，每天白天和晚上）
                dates = []
                for weather_element in result.get('weather', []):
                    for value in weather_element.get('elementValue', []):
                        date_period = (value.get('date', ''), value.get('period', ''))
                        if date_period not in dates:
                            dates.append(date_period)
                
                # 排序日期和時段
                dates.sort(key=lambda x: (x[0], x[1] != '白天'))  # 白天在前，晚上在後
                
                # 為每個時間點建立資料結構
                for date, period in dates:
                    weather_data.append({
                        'time': f"{date} {period}",
                        'temperature': '-',
                        'feels_like': '-',
                        'humidity': '-',
                        'weather': '-',
                        'rain_chance': '-',
                        'wind_scale': '-',
                        'wind_direction': '-'
                    })
                
                # 填入氣象資料
                for weather_element in result.get('weather', []):
                    element_type = weather_element.get('elementType')
                    for value in weather_element.get('elementValue', []):
                        date = value.get('date', '')
                        period = value.get('period', '')
                        values = value.get('values', {})
                        print(f"values: {values}")
                        
                        # 找到對應的時間點資料
                        target_data = next((x for x in weather_data if x['time'] == f"{date} {period}"), None)
                        if target_data:
                            if element_type == "平均溫度" and "Temperature" in values:
                                target_data['temperature'] = f"{values['Temperature']}°C" if values['Temperature'] != '-' else '-'
                            elif element_type == "體感溫度" and "FeelsLike" in values:
                                target_data['feels_like'] = f"{values['FeelsLike']}°C" if values['FeelsLike'] != '-' else '-'
                            elif element_type == "相對濕度" and "Humidity" in values:
                                target_data['humidity'] = f"{values['Humidity']}%" if values['Humidity'] != '-' else '-'
                            elif element_type == "天氣現象" and "Weather" in values:
                                target_data['weather'] = values['Weather']
                            elif element_type == "降雨機率" and "RainChance" in values:
                                target_data['rain_chance'] = f"{values['RainChance']}%" if values['RainChance'] != '-' else '-'
                            elif element_type == "風向" and "WindDirection" in values:
                                target_data['wind_direction'] = values['WindDirection']
                            elif element_type == "蒲福風級" and "WindScale" in values:
                                target_data['wind_scale'] = f"{values['WindScale']}級" if values['WindScale'] != '-' else '-'
                
                result = {'city': city, 'district': district, 'weather': weather_data}
                self.format_weather_data(result)
            except Exception as e:
                print(f"\nError processing data: {str(e)}")
                messagebox.showerror("錯誤", f"處理資料時發生錯誤: {str(e)}")
        else:
            messagebox.showerror("錯誤", "無法獲取天氣資料")
            
    def get_earthquake(self):
        # 根據下拉式選單值獲取地震類型
        earthquake_type_text = self.earthquake_type_combo.get()
        # 將選項文字轉換為對應的數值
        mode_type = 0 if earthquake_type_text == "小區域有感地震" else 1
        
        result = self.api.getEarthquake(mode_type)
        
        # 清空先前顯示
        for widget in self.earthquake_result.winfo_children():
            widget.destroy()
            
        if not result['status']:
            ctk.CTkLabel(self.earthquake_result, text=f"錯誤: {result['message']}").pack()
            return
            
        data = result['data']
        records = data.get('records', {})
        eq_list = records.get('Earthquake', [])
        
        if not eq_list:
            ctk.CTkLabel(self.earthquake_result, text="目前查無地震資料。").pack()
            return

        # 創建可滾動的框架
        scroll_frame = ctk.CTkScrollableFrame(self.earthquake_result, width=850, height=500)
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # 標題列
        headers = ["地震時間", "震央位置", "規模", "深度", "最大震度", "簡要描述"]
        header_widths = [120, 120, 60, 60, 100, 350]  # 自定義各列寬度
        
        header_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=2, pady=5)
        
        for col, (header, width) in enumerate(zip(headers, header_widths)):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color="#2B5773",
                text_color="white",
                corner_radius=6,
                width=width
            )
            label.grid(row=0, column=col, padx=2, pady=2, sticky="nsew")
            header_frame.grid_columnconfigure(col, weight=0)  # 不自動調整寬度

        # 地震資料列
        for row_idx, eq in enumerate(eq_list, start=1):
            info = eq.get('EarthquakeInfo', {})
            intensity = eq.get('Intensity', {})
            shaking_areas = intensity.get('ShakingArea', [])
            
            # 找出最大震度地區
            max_intensity = "-"
            max_area = "-"
            if shaking_areas:
                # 嘗試找出最大震度地區
                try:
                    max_area_obj = max(shaking_areas, key=lambda a: int(a.get('AreaIntensity', '0') or '0'))
                    max_intensity = max_area_obj.get('AreaIntensity', '-')
                    max_area = max_area_obj.get('CountyName', '-')
                except (ValueError, TypeError):
                    # 如果無法比較震度，使用第一個地區
                    max_area_obj = shaking_areas[0] if shaking_areas else {}
                    max_intensity = max_area_obj.get('AreaIntensity', '-')
                    max_area = max_area_obj.get('CountyName', '-')

            # 準備顯示資料
            epicenter = info.get('Epicenter', {}).get('Location', '-')
            magnitude = info.get('EarthquakeMagnitude', {}).get('MagnitudeValue', '-')
            depth = f"{info.get('FocalDepth', '-')} 公里"
            origin_time = info.get('OriginTime', '-')
            report = eq.get('ReportContent', '-')
            
            # 創建每行的框架
            row_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=2, pady=2)
            
            # 顯示資料
            values = [origin_time, epicenter, magnitude, depth, f"{max_area} {max_intensity}", report]
            
            for col_idx, (val, width) in enumerate(zip(values, header_widths)):
                # 為報告內容提供更大的換行寬度
                wrap_width = 330 if col_idx == 5 else width - 10
                
                label = ctk.CTkLabel(
                    row_frame,
                    text=str(val),
                    font=ctk.CTkFont(size=13),
                    wraplength=wrap_width,
                    corner_radius=4,
                    width=width,
                    height=50 if col_idx == 5 else 30,  # 給報告內容更多垂直空間
                    anchor="w",  # 文字靠左對齊
                    justify="left"  # 多行文字左對齊
                )
                label.grid(row=0, column=col_idx, padx=2, pady=2, sticky="nsew")
                row_frame.grid_columnconfigure(col_idx, weight=0)  # 不自動調整寬度
            
            # 添加分隔線
            separator = ctk.CTkFrame(scroll_frame, height=1, fg_color="#CCCCCC")
            separator.pack(fill="x", padx=5, pady=3)

    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)
        self.root.update_idletasks()
        self.root.update()

if __name__ == "__main__":
    root = ctk.CTk()
    app = WeatherApp(root)
    root.mainloop()