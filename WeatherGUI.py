import customtkinter as ctk
from tkinter import messagebox
import json
from RequestApi import RequestApi
from app import get_weather_by_loction

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
        
        # 天氣元素選擇
        ctk.CTkLabel(
            control_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        
        self.elements_var = ctk.StringVar(value="天氣預報綜合描述")
        self.elements_combo = ctk.CTkComboBox(
            control_frame,
            values=[
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
            ],
            variable=self.elements_var,
            width=200,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        self.elements_combo.pack(pady=5)
        
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
        
        # 查詢結果顯示區域
        self.weather_result = ctk.CTkTextbox(
            result_frame,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        self.weather_result.pack(fill="both", expand=True, padx=10, pady=10)
        
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
        element = self.elements_var.get()
        
        if not district:
            messagebox.showerror("錯誤", "請選擇行政區")
            return
            
        result = get_weather_by_loction(city, district, [element])
        if result:
            formatted_data = self.format_weather_data(result)
            self.weather_result.delete(1.0, ctk.END)
            self.weather_result.insert(ctk.END, formatted_data)
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