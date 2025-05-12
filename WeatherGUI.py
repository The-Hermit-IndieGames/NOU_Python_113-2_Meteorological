import customtkinter as ctk
from tkinter import messagebox
import json
from RequestApi import RequestApi
from app import get_weather_by_loction
from datetime import datetime
from datetime import date as DateToday
from PIL import Image
import os
import sys

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("氣象預報系統")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        # 初始化天氣圖示
        self.weather_icons = self.load_weather_icons()
        
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
            text="",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 15))
        
        # 替換成下拉選單
        earthquake_types = ["小區域有感地震", "顯著有感地震"]
        self.earthquake_type_var = ctk.StringVar()
        self.earthquake_type_combo = ctk.CTkComboBox(
            control_frame,
            values=earthquake_types,
            variable=self.earthquake_type_var,
            width=200,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        self.earthquake_type_combo.pack(pady=5)
        self.earthquake_type_combo.set(earthquake_types[0])
        
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
        
        # 查詢結果
        ctk.CTkLabel(
            result_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # 改為結果表格框架
        self.earthquake_table_frame = ctk.CTkFrame(result_frame)
        self.earthquake_table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
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

    def resource_path(self, relative_path):
        """取得執行路徑，不論是原始執行或經 PyInstaller 打包"""
        try:
                    base_path = sys._MEIPASS  # PyInstaller onefile 暫存路徑
        except AttributeError:
            base_path = os.path.abspath(".")
            # 僅開發時檢查圖示資料夾
            folder = os.path.join(base_path, "weather_icons")
            if not os.path.exists(folder):
                os.makedirs(folder)
                print("已建立資料夾 weather_icons，請放入對應圖示（PNG）後再執行。")

        return os.path.join(base_path, relative_path)
        
    def load_weather_icons(self):
        """載入天氣圖示（PNG）"""
        icons = {}
        icon_size = (40, 40)
        icon_path = "weather_icons"

        # 確保圖示資料夾存在
        # if not os.path.exists(icon_path):
        #     os.makedirs(icon_path)
        #     print(f"請在 {icon_path} 資料夾中放入天氣圖示（PNG 格式）")
        #     return icons

        # 定義天氣狀況和對應的圖示檔案名稱
        weather_icon_mapping = {
            "多雲": "多雲.png",
            "陰": "陰.png",
            "陰天": "陰天.png",
            "陰時多雲": "陰時多雲.png",
            "多雲時陰": "多雲時陰.png",
            "雨": "雨.png",
            "陣雨": "陣雨.png",
            "短暫雨": "短暫雨.png",
            "多雲短暫雨": "多雲短暫雨.png",
            "午後短暫雨": "午後短暫雨.png",
            "多雲午後短暫雨": "多雲午後短暫雨.png",
            "晴": "晴.png",
            "晴時多雲": "晴時多雲.png",
            "晴時陰": "晴時陰.png",
            "晴時多雲時陰": "晴時多雲時陰.png",
            "晴時多雲時陰短暫雨": "晴時多雲時陰短暫雨.png",
            "晴時多雲時陰陣雨": "晴時多雲時陰陣雨.png",
            "晴時多雲時陰陣雨短暫雨": "晴時多雲時陰陣雨短暫雨.png",
            "陰短暫陣雨或雷雨": "陰短暫陣雨或雷雨.png",
        }

        # 載入圖示
        # for weather, icon_file in weather_icon_mapping.items():
        #     icon_path_full = os.path.join(icon_path, icon_file)
        #     if os.path.exists(icon_path_full):
        #         try:
        #             image = Image.open(icon_path_full)
        #             image = image.resize(icon_size, Image.Resampling.LANCZOS)
        #             icons[weather] = ctk.CTkImage(light_image=image, dark_image=image, size=icon_size)
        #             print(f"成功載入圖示: {icon_file}")
        #         except Exception as e:
        #             print(f"無法載入圖示 {icon_file}: {str(e)}")
        #     else:
        #         print(f"找不到圖示檔案: {icon_path_full}")

        # return icons
    
        for weather, icon_file in weather_icon_mapping.items():
        # 使用 resource_path 抓取正確路徑
            icon_path_full = self.resource_path(os.path.join(icon_path, icon_file))

            if os.path.exists(icon_path_full):
                try:
                    image = Image.open(icon_path_full)
                    image = image.resize(icon_size, Image.Resampling.LANCZOS)
                    icons[weather] = ctk.CTkImage(light_image=image, dark_image=image, size=icon_size)
                    print(f"成功載入圖示: {icon_file}")
                except Exception as e:
                    print(f"無法載入圖示 {icon_file}: {str(e)}")
            else:
                print(f"找不到圖示檔案: {icon_path_full}")

        return icons

    def get_weather_icon(self, weather_text):
        """根據天氣描述取得對應的圖示"""
        for key in self.weather_icons.keys():
            if key in weather_text:
                return self.weather_icons[key]
        return None

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

                    # 創建垂直排列的框架
                    weather_content_frame = ctk.CTkFrame(
                        weather_frame,
                        fg_color="transparent"
                    )
                    weather_content_frame.place(relx=0.5, rely=0.5, anchor="center")
                    
                    # 顯示天氣圖示
                    weather_icon = self.get_weather_icon(weather_text)
                    if weather_icon:
                        icon_label = ctk.CTkLabel(
                            weather_content_frame,
                            text="",
                            image=weather_icon
                        )
                        icon_label.pack(pady=(0, 5))
                    
                    # 顯示天氣文字
                    if len(weather_text) > 10:
                        weather_text = '\n'.join([weather_text[i:i+10] for i in range(0, len(weather_text), 10)])
                    
                    weather_label = ctk.CTkLabel(
                        weather_content_frame,
                        text=weather_text,
                        font=ctk.CTkFont(size=12),
                        fg_color="transparent",
                        justify="center",
                        wraplength=60,
                        text_color="black"
                    )
                    weather_label.pack()

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
        
    def create_intensity_icon(self, parent, intensity_level):
        
        # 定義震度等級對應的顏色和文字樣式
        intensity_styles = {
            "0級": {"bg": "#CCCCCC", "fg": "black", "font_size": 16},      
            "1級": {"bg": "#CCCCCC", "fg": "black", "font_size": 16},      
            "2級": {"bg": "#B266FF", "fg": "black", "font_size": 16},      
            "3級": {"bg": "#9999FF", "fg": "black", "font_size": 16},      
            "4級": {"bg": "#3333CC", "fg": "white", "font_size": 16},      
            "5弱": {"bg": "#CCFFCC", "fg": "white", "font_size": 16},    
            "5強": {"bg": "#66CC66", "fg": "white", "font_size": 16},    
            "6弱": {"bg": "#FFFF99", "fg": "black", "font_size": 16},    
            "6強": {"bg": "#FFAA66", "fg": "white", "font_size": 16},    
            "7級": {"bg": "#FF6666", "fg": "white", "font_size": 16},      
        }

    
        # 獲取震度樣式
        style = intensity_styles.get(intensity_level, {"bg": "#CCCCCC", "fg": "black", "font_size": 16})
    
        # 創建圖示
        icon_frame = ctk.CTkFrame(parent, fg_color="transparent")
        icon_frame.pack(expand=True, fill="both")
    
        spacer_top = ctk.CTkFrame(icon_frame, fg_color="transparent", height=0)
        spacer_top.pack(expand=True)

        # 創建圓形圖示
        icon_size = 50
        intensity_icon = ctk.CTkFrame(
            icon_frame,
            width=icon_size,
            height=icon_size,
            corner_radius=icon_size//2,  
            fg_color=style["bg"],            
        )
        intensity_icon.pack(anchor="center")
        intensity_icon.pack_propagate(False)  

        icon_label = ctk.CTkLabel(
            intensity_icon,
            text=intensity_level,
            font=ctk.CTkFont(size=style["font_size"], weight="bold"),
            text_color=style["fg"]
        )
        icon_label.place(relx=0.5, rely=0.5, anchor="center")  
        
        spacer_bottom = ctk.CTkFrame(icon_frame, fg_color="transparent", height=0)
        spacer_bottom.pack(expand=True)

        return icon_frame
    
    def format_earthquake_data(self, data):
        # 清除現有表格
        for widget in self.earthquake_table_frame.winfo_children():
            widget.destroy()

        if not data or not data.get('records', {}).get('Earthquake'):
            label = ctk.CTkLabel(self.earthquake_table_frame, text="目前查無地震資料")
            label.pack()
            return

        # 創建主表格框架
        main_table_frame = ctk.CTkFrame(self.earthquake_table_frame, fg_color="transparent")
        main_table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.earthquake_main_table = main_table_frame

        # 標題
        headers = ["發生時間", "震央位置", "規模", "深度", "最大震度", "地區", "描述"]

        # 預設列寬度權重 (描述欄位給予更多空間)
        col_weights = [1, 1, 1, 1, 1, 1, 3]

        # 設定列寬權重
        for i, weight in enumerate(col_weights):
            main_table_frame.grid_columnconfigure(i, weight=weight)

        # 繪製標題列
        for col, text in enumerate(headers):
            header_cell = ctk.CTkFrame(main_table_frame, corner_radius=6, fg_color="#2B5773")
            header_cell.grid(row=0, column=col, padx=2, pady=2, sticky="news")

            label = ctk.CTkLabel(
                header_cell,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white",
                justify="center"
            )
            label.pack(fill="both", expand=True, padx=5, pady=5)

        # 填入地震數據
        eq_list = data.get('records', {}).get('Earthquake', [])

        row_heights = [40]  
        for _ in range(len(eq_list)):
            row_heights.append(60)  

        # 設定行高
        for i, height in enumerate(row_heights):
            main_table_frame.grid_rowconfigure(i, minsize=height)

        # 計算換行寬度
        base_width = self.earthquake_table_frame.winfo_width()
        if base_width <= 1:  
            base_width = 800

        total_weight = sum(col_weights)
        col_wraplengths = [int((weight / total_weight) * base_width * 0.85) for weight in col_weights]

        # 處理每行資料
        for row_idx, eq in enumerate(eq_list, 1):
            info = eq.get('EarthquakeInfo', {})
            intensity = eq.get('Intensity', {})
            shaking_areas = intensity.get('ShakingArea', [])

            # 取最大震度
            max_area = None
            max_intensity = ""
            for area in shaking_areas:
                ai = area.get('AreaIntensity', '')
                if ai and (not max_intensity or ai > max_intensity):
                    max_intensity = ai
                    max_area = area

            # 提取所需數據
            origin_time = info.get('OriginTime', '-')
            location = info.get('Epicenter', {}).get('Location', '-')
            magnitude_value = info.get('EarthquakeMagnitude', {}).get('MagnitudeValue')
            magnitude = str(magnitude_value) if magnitude_value is not None else '-'

            focal_depth = info.get('FocalDepth')
            depth = f"{focal_depth} 公里" if focal_depth is not None else '-'

            if max_area:
                area_intensity = max_area.get('AreaIntensity', '-')
                county_name = max_area.get('CountyName', '-')
            else:
                area_intensity = '-'
                county_name = '-'

            report_content = eq.get('ReportContent', '-')

            values = [
                origin_time,
                location,
                magnitude,
                depth,
                area_intensity,
                county_name,
                report_content
            ]
        
            cell_bg_color = "#F5F5F5" if row_idx % 2 == 0 else "#FFFFFF"

            # 儲存標籤對象以便後續更新
            self.earthquake_labels = getattr(self, 'earthquake_labels', {})
            if row_idx not in self.earthquake_labels:
                self.earthquake_labels[row_idx] = {}
        
            for col_idx, value in enumerate(values):
                text_value = str(value) if value is not None else '-'
    
                cell_frame = ctk.CTkFrame(main_table_frame, corner_radius=6, fg_color=cell_bg_color)
                cell_frame.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky="news")
    
                if col_idx == 4:  # 最大震度欄位
                    self.create_intensity_icon(cell_frame, text_value)
                else:                    
                    label = ctk.CTkLabel(
                        cell_frame,
                        text=text_value,
                        font=ctk.CTkFont(size=12),
                        justify="left" if col_idx == 6 else "center",  
                        text_color="black",
                        wraplength=col_wraplengths[col_idx],  
                    )
                    label.pack(fill="both", expand=True, padx=5, pady=5)
                    self.earthquake_labels[row_idx][col_idx] = label
    
        # 定義更新換行寬度的函數
        def update_wraplengths(event=None):
            current_width = self.earthquake_table_frame.winfo_width()
            if current_width <= 1:
                return
        
            new_wraplengths = [int((weight / total_weight) * current_width * 0.85) for weight in col_weights]
        
            # 更新所有標籤的換行寬度
            for row in self.earthquake_labels:
                for col, label in self.earthquake_labels[row].items():
                    label.configure(wraplength=new_wraplengths[col])
    
        # 綁定更新函數到類別
        self.update_earthquake_wraplengths = update_wraplengths
    
        # 綁定視窗大小變化事件
        self.earthquake_table_frame.bind("<Configure>", self.update_earthquake_wraplengths)
    
        # 初始更新一次
        main_table_frame.update_idletasks()
        self.update_earthquake_wraplengths()

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
                
                result = {'city': city, 'district': district, 'weather': weather_data}
                self.format_weather_data(result)
            except Exception as e:
                print(f"\nError processing data: {str(e)}")
                messagebox.showerror("錯誤", f"處理資料時發生錯誤: {str(e)}")
        else:
            messagebox.showerror("錯誤", "無法獲取天氣資料")
            
    def get_earthquake(self):
        # 根據下拉選單獲取地震類型值
        earthquake_type_text = self.earthquake_type_var.get()
        mode_type = 0 if earthquake_type_text == "小區域有感地震" else 1
        
        try:
            result = self.api.getEarthquake(mode_type)
            if result['status']:
                self.format_earthquake_data(result['data'])
            else:
                messagebox.showerror("錯誤", result['message'])
        except TypeError as e:
            print(f"TypeError 發生: {str(e)}")
            messagebox.showerror("錯誤", f"處理資料時發生錯誤: {str(e)}")
        except Exception as e:
            print(f"錯誤發生: {str(e)}")
            messagebox.showerror("錯誤", f"發生未預期的錯誤: {str(e)}")

    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)
        self.root.update_idletasks()
        self.root.update()

if __name__ == "__main__":
    root = ctk.CTk()
    app = WeatherApp(root)
    root.mainloop()


    
    # 匯出命令(無控制台)
    # pyinstaller --onefile --add-data "weather_icons;weather_icons" --name "氣象預報系統 Windows/iOS v0.1.0" --noconsole <your_script.py>
    
    # 匯出命令(有控制台)
    # pyinstaller --onefile --add-data "weather_icons;weather_icons" --name "氣象預報系統 Windows/iOS v0.1.0 debug" <your_script.py>

    # <your_script.py> 填入完整路徑
    # --name "氣象預報系統 Windows/iOS v0.1.0" 用於設置匯出後檔名，建議: "房價預測器 OS系統 版本號"

    # 開始匯出後會出現 build 資料夾並產生傳遞檔案，可在匯出後刪除
    # [檔名].spec 檔案是 PyInstaller 產生執行檔時的配置文件，可在匯出後刪除
    # 匯出完成後檔案(.exe或.app)將保存在 dist 資料夾，是我們的最終成品

    # 通過  --add-data "weather_icons;weather_icons" 將圖片資料夾打包

    # iOS 版  by ???
    # pyinstaller --onefile --add-data "weather_icons;weather_icons" --name "氣象預報系統 iOS v0.1.0 debug" "完整路徑"
    # pyinstaller --onefile --add-data "weather_icons;weather_icons" --name "氣象預報系統 iOS v0.1.0" --noconsole "完整路徑"
    