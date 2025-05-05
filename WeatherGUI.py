import customtkinter as ctk
from tkinter import messagebox
import json
from RequestApi import RequestApi
from app import get_weather_by_loction
from datetime import datetime
from datetime import date as DateToday


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("氣象預報系統")
        self.root.geometry("1000x700") 
        
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
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))
        
        # 右上角外觀模式下拉選單
        self.appearance_mode = ctk.CTkOptionMenu(
            self.root,
            values=["system", "light", "dark"],
            command=self.change_appearance_mode,
            font=ctk.CTkFont(size=12),
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
            font=ctk.CTkFont(size=14, weight="bold"),
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
        
        # 結果表格框架
        self.weather_table_frame = ctk.CTkFrame(result_frame)
        self.weather_table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
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
        
        self.earthquake_type = ctk.StringVar(value="0")
        self.earthquake_frame_radio = ctk.CTkFrame(control_frame)
        self.earthquake_frame_radio.pack(pady=5)
        
        ctk.CTkRadioButton(
            self.earthquake_frame_radio,
            text="小區域有感地震",
            variable=self.earthquake_type,
            value="0",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            self.earthquake_frame_radio,
            text="顯著有感地震",
            variable=self.earthquake_type,
            value="1",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=10)
        
        # 查詢按鈕
        self.query_button = ctk.CTkButton(
            control_frame,
            text="查詢",
            command=self.get_earthquake,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.query_button.pack(pady=20)
        
        # 右側結果顯示區域
        result_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        result_frame.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=0)
        
        # 結果標題
        ctk.CTkLabel(
            result_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # 結果顯示區域
        self.earthquake_result = ctk.CTkTextbox(
            result_frame,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
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

        # 定義星期對照表
        weekday_map = {
            0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"
        }

        # 整理數據按日期分組
        daily_data = {}
        for weather in data['weather']:
            date = weather['time'].split(' ')[0]
            period = weather['time'].split(' ')[1]
            if date not in daily_data:
                daily_data[date] = {'白天': None, '晚上': None}
            daily_data[date][period] = weather

        row_labels = ["天氣狀況", "溫度", "降雨機率", "體感溫度", "相對溼度", "紫外線指數"]
        
        # 地區
        location_label = ctk.CTkLabel(
            self.weather_table_frame,
            text=f"{data['city']}{data['district']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2B5773",
            text_color="white",
            corner_radius=6,
            wraplength=60,
        )
        location_label.grid(row=0, column=0, columnspan=1, padx=(5, 2), pady=(5, 2), sticky="nsew")

        for i, label in enumerate(row_labels):
            row_label = ctk.CTkLabel(
                self.weather_table_frame,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#2B5773",
                text_color="white",
                corner_radius=6,
                width=120 
            )
            row_label.grid(row=i+1, column=0, padx=(5, 2), pady=1, sticky="nsew")

        # 填充天氣數據
        col = 1
        for date, periods in daily_data.items():
            # 轉換日期格式和獲取星期
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            weekday = weekday_map[date_obj.weekday()]
            display_date = f"{date_obj.month:02d}/{date_obj.day:02d}\n星期{weekday}"
            
            # 創建日期框架
            date_frame = ctk.CTkFrame(
                self.weather_table_frame,
                fg_color="#2B5773",
                corner_radius=6,
            )
            date_frame.grid(row=0, column=col, columnspan=2, padx=1, pady=(5, 2), sticky="nsew")
            
            # 日期標題
            date_label = ctk.CTkLabel(
              date_frame,
                text=f"{date_obj.month:02d}/{date_obj.day:02d}\n星期{weekday}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white",
            )
            date_label.pack(pady=(5,0))

            period_frame = ctk.CTkFrame(
                date_frame,
                fg_color="transparent"
            )
            period_frame.pack(fill="x", pady=(0,5))
            
            day_label = ctk.CTkLabel(
                period_frame,
                text="白天",
                font=ctk.CTkFont(size=11),
                text_color="white",
                width=50
            )
            day_label.pack(side="left", padx=2)
            
            night_label = ctk.CTkLabel(
                period_frame,
                text="晚上",
                font=ctk.CTkFont(size=11),
                text_color="white",
                width=50
            )
            night_label.pack(side="right", padx=2)

            # 白天和晚上數據
            for period_idx, period_key in enumerate(['白天', '晚上']):
                period_data = periods.get(period_key, {})
                if period_data:
                    # 天氣狀況
                    weather_frame = ctk.CTkFrame(
                        self.weather_table_frame,
                        fg_color="#F5F5F5" if period_idx == 0 else "#FFFFFF",
                        width=100, 
                        height=80
                    )
                    weather_frame.grid(row=1, column=col, padx=1, pady=1, sticky="nsew")
                    weather_frame.grid_propagate(False)
                    
                    weather_text = period_data.get('weather', '-')

                    if len(weather_text) > 10:
                        weather_text = '\n'.join([weather_text[i:i+10] for i in range(0, len(weather_text), 10)])
                    
                    weather_label = ctk.CTkLabel(
                        weather_frame,
                        text=weather_text,
                        font=ctk.CTkFont(size=12),
                        fg_color="transparent",
                        wraplength=60,
                        justify="center",
                        text_color="black"
                    )
                    weather_label.place(relx=0.5, rely=0.5, anchor="center")

                    # 溫度
                    temp_frame = ctk.CTkFrame(
                        self.weather_table_frame,
                        fg_color="#F5F5F5" if period_idx == 0 else "#FFFFFF",
                        width=100,
                        height=40
                    )
                    temp_frame.grid(row=2, column=col, padx=1, pady=1, sticky="nsew")
                    temp_frame.grid_propagate(False)
                    
                    temp_label = ctk.CTkLabel(
                        temp_frame,
                        text=period_data.get('temperature', '-'),
                        font=ctk.CTkFont(size=12),
                        fg_color="transparent",
                        text_color="black"
                    )
                    temp_label.place(relx=0.5, rely=0.5, anchor="center")

                    # 降雨機率
                    rain_frame = ctk.CTkFrame(
                        self.weather_table_frame,
                        fg_color="#F5F5F5" if period_idx == 0 else "#FFFFFF",
                        width=100,
                        height=40
                    )
                    rain_frame.grid(row=3, column=col, padx=1, pady=1, sticky="nsew")
                    rain_frame.grid_propagate(False)
                    
                    rain_label = ctk.CTkLabel(
                        rain_frame,
                        text=period_data.get('rain_chance', '-'),
                        font=ctk.CTkFont(size=12),
                        fg_color="transparent",
                        text_color="black"
                    )
                    rain_label.place(relx=0.5, rely=0.5, anchor="center")

                    # 體感溫度
                    feels_frame = ctk.CTkFrame(
                        self.weather_table_frame,
                        fg_color="#F5F5F5" if period_idx == 0 else "#FFFFFF",
                        width=100,
                        height=60
                    )
                    feels_frame.grid(row=4, column=col, padx=1, pady=1, sticky="nsew")
                    feels_frame.grid_propagate(False)
                    
                    feels_label = ctk.CTkLabel(
                        feels_frame,
                        text=period_data.get('feels_like', '-'),
                        font=ctk.CTkFont(size=12),
                        fg_color="transparent",
                        justify="center",
                        wraplength=60,
                        text_color="black" 
                    )
                    feels_label.place(relx=0.5, rely=0.5, anchor="center")

                    # 相對溼度
                    humidity_frame = ctk.CTkFrame(
                        self.weather_table_frame,
                        fg_color="#F5F5F5" if period_idx == 0 else "#FFFFFF",
                        width=100,
                        height=40
                    )
                    humidity_frame.grid(row=5, column=col, padx=1, pady=1, sticky="nsew")
                    humidity_frame.grid_propagate(False)
                    
                    humidity_label = ctk.CTkLabel(
                        humidity_frame,
                        text=period_data.get('humidity', '-'),
                        font=ctk.CTkFont(size=12),
                        fg_color="transparent",
                        text_color="black"
                    )
                    humidity_label.place(relx=0.5, rely=0.5, anchor="center")

                    # 紫外線指數 - 只在白天的第一個欄位創建，並跨兩列
                    if period_key == '白天':
                        uv_frame = ctk.CTkFrame(
                            self.weather_table_frame,
                            fg_color="#F5F5F5",
                            width=200,  # 兩倍寬度
                            height=40
                        )
                        uv_frame.grid(row=6, column=col, columnspan=2, padx=1, pady=1, sticky="nsew")
                        uv_frame.grid_propagate(False)
                        
                        uv_label = ctk.CTkLabel(
                            uv_frame,
                            text=period_data.get('uv_index', '-'),
                            font=ctk.CTkFont(size=12),
                            fg_color="transparent",
                            text_color="black"
                        )
                        uv_label.place(relx=0.5, rely=0.5, anchor="center")

                col += 1

        # 配置網格權重
        self.weather_table_frame.grid_columnconfigure(0, weight=1)
        for i in range(1, col):
            self.weather_table_frame.grid_columnconfigure(i, weight=1)
        
        # 配置行高
        for i in range(7):  # 0-6行
            self.weather_table_frame.grid_rowconfigure(i, weight=1)
        
    def format_earthquake_data(self, data):
        if not data:
            return "無法獲取地震資料"
        records = data.get('records', {})
        eq_list = records.get('Earthquake')
        if not eq_list or len(eq_list) == 0:
            return "目前查無地震資料。"
        result = []
        for eq in eq_list:
            info = eq.get('EarthquakeInfo', {})
            intensity = eq.get('Intensity', {})
            shaking_areas = intensity.get('ShakingArea', [])
            # 取最大震度
            max_area = None
            max_intensity = ""
            for area in shaking_areas:
                ai = area.get('AreaIntensity', '')
                if not max_intensity or ai > max_intensity:
                    max_intensity = ai
                    max_area = area
            # 條列顯示
            result.append(f"地震時間：{info.get('OriginTime', '-')}")
            result.append(f"震央位置：{info.get('Epicenter', {}).get('Location', '-')}")
            result.append(f"地震規模：{info.get('EarthquakeMagnitude', {}).get('MagnitudeValue', '-')}")
            result.append(f"地震深度：{info.get('FocalDepth', '-')} 公里")
            if max_area:
                result.append(f"最大震度：{max_area.get('CountyName', '-')}，{max_area.get('AreaIntensity', '-')}")
            else:
                result.append("最大震度：-")
            result.append(f"簡要描述：{eq.get('ReportContent', '-')}")
            result.append("-" * 40)
        return "\n".join(result)
        
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
            "蒲福風級",
            "紫外線指數",
            "天氣預報綜合描述"
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
                
                # 檢查今天日期是否缺少白天資料，若是則補進空值
                today_str = DateToday.today().strftime("%Y-%m-%d")
                has_today_day = any(d == today_str and p == "白天" for d, p in dates)
                if not has_today_day:
                    dates.insert(0, (today_str, "白天"))
                
                # 排序日期和時段，白天前晚上後
                dates.sort(key=lambda x: (x[0], x[1] != '白天'))
                
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
                        'wind_direction': '-',
                        'uv_index': '-',
                        'description': '-'
                    })
                
                # 填入氣象資料
                import re
                for weather_element in result.get('weather', []):
                    element_type = weather_element.get('elementType')
                    for value in weather_element.get('elementValue', []):
                        date = value.get('date', '')
                        period = value.get('period', '')
                        values = value.get('values', {})

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
                            elif element_type == "紫外線指數" and "UVIndex" in values:
                                target_data['uv_index'] = values['UVIndex']
                            elif element_type == "天氣預報綜合描述" and "WeatherDescription" in values:
                                description = values['WeatherDescription']
                                target_data['description'] = description
                                # Extract "溫度攝氏22至25度。舒適。" → assign to feels_like
                                temp_match = re.search(r"(溫度攝氏[\d至]+度。[^\n。]*)", description)
                                if temp_match and target_data['feels_like'] == '-':
                                    target_data['feels_like'] = temp_match.group(1)
                                # Extract "相對濕度90%" → assign to humidity
                                humidity_match = re.search(r"相對濕度(\d+)%", description)
                                if humidity_match and target_data['humidity'] == '-':
                                    target_data['humidity'] = f"{humidity_match.group(1)}%"
                                # Extract "降雨機率60%" → assign to rain_chance
                                rain_match = re.search(r"降雨機率(\d+)%", description)
                                if rain_match and target_data['rain_chance'] == '-':
                                    target_data['rain_chance'] = f"{rain_match.group(1)}%"
                                # Extract "風速<= 1級" → assign to wind_scale
                                wind_scale_match = re.search(r"風速.?=?\s?(\d+)級", description)
                                if wind_scale_match and target_data['wind_scale'] == '-':
                                    target_data['wind_scale'] = f"{wind_scale_match.group(1)}級"
                                # Extract "東北風" → assign to wind_direction
                                wind_dir_match = re.search(r"(東北風|西北風|東南風|西南風|北風|南風|東風|西風)", description)
                                if wind_dir_match and target_data['wind_direction'] == '-':
                                    target_data['wind_direction'] = wind_dir_match.group(1)
                
                print("\n=== Processed Weather Data ===")
                print(json.dumps(weather_data, indent=2, ensure_ascii=False))
                
                result = {'city': city, 'district': district, 'weather': weather_data}
                self.format_weather_data(result)
            except Exception as e:
                print(f"\nError processing data: {str(e)}")
                messagebox.showerror("錯誤", f"處理資料時發生錯誤: {str(e)}")
        else:
            messagebox.showerror("錯誤", "無法獲取天氣資料")
            
    def get_earthquake(self):
        mode_type = int(self.earthquake_type.get())
        
        result = self.api.getEarthquake(mode_type)
        if result['status']:
            formatted_data = self.format_earthquake_data(result['data'])
            self.earthquake_result.delete(1.0, ctk.END)
            self.earthquake_result.insert(ctk.END, formatted_data)
        else:
            messagebox.showerror("錯誤", result['message'])

    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)
        self.root.update_idletasks()
        self.root.update()

if __name__ == "__main__":
    root = ctk.CTk()
    app = WeatherApp(root)
    root.mainloop() 