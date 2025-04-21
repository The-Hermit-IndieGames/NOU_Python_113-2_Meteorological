import tkinter as tk  # 導入 tkinter 模組，用於製作圖形化界面
from tkinter import messagebox  # 導入 tkinter 中的 messagebox 用於顯示錯誤訊息框
import customtkinter

# 宣告
input_year = 0
year_day_list = []
year_day_list_strings = []

big_mon = [1,3,5,7,8,10,12]
week = "周一     週二    週三     周四    週五     週六    週日  "

show_mon = 1

# 運算部分 =============================================================================================================== 運算部分 #

# 函式-判斷是否為閏年
def is_leap_year(year):
    # 如果年份能被 4 整除，則可能是閏年。
    if (year % 4 == 0):
        # 但是，如果該年份能被 100 整除，則不是閏年。
        if (year % 100 == 0):
            # 除非該年份能被 400 整除，那麼它仍然是閏年。
            if(year % 400 == 0):
                return True
            else:
                return False
        else:
            return True
    else:
        return False


# 閏年-字串版
def is_leap_year_string(year):
    if is_leap_year(year):
        return "是"
    else:
        return "非"


# 周次修正值
def week_add(year):
    # 基於 0001年 1/1 為周一    ex. 0001年 回傳0 --> 1/1 為周一
    return ((year-1) + (year-1)//4 - (year-1)//100 + (year-1)//400) % 7


# 建立年曆 (列表: [ [1,2,3,...] , [*,*,1,2,3,...] , ......] )
def creat_year_day_list(year):
    global big_mon, year_day_list
    year_day_list = []

    max_day = 0
    now_week = week_add(year)

    mon = 1
    # 第一層-月
    while mon <= 12:
        mon_days = []

        # 天數判斷
        if mon == 2 and is_leap_year(year):
            max_day = 29
        elif mon == 2 and is_leap_year(year) == False:
            max_day = 28
        elif mon in big_mon:
            max_day = 31
        else:
            max_day = 30
        
        # 每月初按造星期輸出空白
        mon_star = now_week
        while mon_star >= 1:
            mon_days.append(" ")
            mon_star -= 1
        
        day = 1
        # 第二層-日
        while day <= max_day:
            
            mon_days.append(day)
            now_week += 1
            if now_week >= 7:
                now_week = 0

            day += 1
        

        year_day_list.append(mon_days)
        mon += 1
        
    else:
        print("\ncreat_year_day_list END")


# 按周印出年曆
def print_year_days():
    global year_day_list, year_day_list_strings
    year_day_list_strings = []

    for mon_list in year_day_list:
        month_str = ""

        x = 0
        for day in mon_list:
            month_str += str(day).ljust(8)  # 每個元素佔據ljust()個字元
            x += 1
            if x % 7 == 0:  # 每7個元素換行
                month_str += "\n"
                x = 0

        year_day_list_strings.append(month_str)
    else:
        print("\nprint_year_days END")


""" 
# 偵錯用
creat_year_day_list(2024)
print_year_days()
print(year_day_list_strings[9]) 
"""


# 視窗部分 =============================================================================================================== 視窗部分 #

# 檢查輸入是否為整數
def validate_int(char):
    return char.isdigit() or char == ""

# 提交按鈕的事件處理函數
def submit():
    global input_year, show_mon
    user_input = entry.get()
    if user_input.isdigit():
        input_year = int(user_input)
        print(f"查詢{input_year}年")
        creat_year_day_list(input_year)
        print_year_days()
        show_mon = 1
        window_update()
    else:
        messagebox.showerror("錯誤", "請輸入有效的年分")


# 換頁按鈕 (下一頁) 的事件處理函數
def next_page():
    global show_mon
    show_mon += 1
    if show_mon >= 13:
        show_mon = 12
    print(f"目前顯示{show_mon:3d}月")
    window_update()

# 換頁按鈕 (上一頁) 的事件處理函數
def previous_page():
    global show_mon
    show_mon -= 1
    if show_mon <= 0:
        show_mon = 1
    print(f"目前顯示{show_mon:3d}月")
    window_update()

# 主視窗刷新
def window_update():
    global input_year, show_mon, input_year

    is_leap_year_var.set(f"{input_year}年{is_leap_year_string(input_year)}閏年")
    output_string = (f"{input_year:4d}年{show_mon:3d}月\n\n{week}\n\n{year_day_list_strings[show_mon-1]}")
    update_main_output(output_string)

# 更新 Text 內容的函式
def update_main_output(new_text):
    main_output_text.configure(state="normal")
    main_output_text.delete("1.0", customtkinter.END)
    main_output_text.insert(customtkinter.END, new_text)
    main_output_text.configure(state="disabled",font=("Courier New", 16))



# 創建主視窗
window = customtkinter.CTk()  # 使用 CTk 來初始化 customtkinter 視窗
window.title("萬年曆")
window.geometry("600x600")


# 設置外觀模式 (可選 "System", "Dark", "Light")
customtkinter.set_appearance_mode("System")  # 跟隨系統設置的深色/淺色模式

appearance_mode = 0

# 更新外觀模式
def update_appearance_mode():
    global appearance_mode
    appearance_mode += 1
    if(appearance_mode == 1) :
        customtkinter.set_appearance_mode("Light")
        appearance_btn.configure(text="淺色模式")
    elif(appearance_mode == 2) :
        customtkinter.set_appearance_mode("Dark")
        appearance_btn.configure(text="深色模式")
    else :
        appearance_mode = 0
        customtkinter.set_appearance_mode("System")
        appearance_btn.configure(text="系統預設")


# 外觀模式按鈕
appearance_btn = customtkinter.CTkButton(
    master=window,
    height=30,
    width=60, 
    text="系統預設",
    font=("Microsoft JhengHei", 16, "bold"),
    command=update_appearance_mode
    )
appearance_btn.pack(pady=5)



# 輸入群組
background_frame_1 = customtkinter.CTkFrame(
    master=window,
    height=60,
    width=550,
)
background_frame_1.pack(pady=10)


# 輸入欄-年
entry_label = customtkinter.CTkLabel(
    master=background_frame_1,
    height=30,
    width=160,
    text="請輸入要查詢的西元年份：",
    font=("Microsoft JhengHei", 16, "bold")
    )
entry_label.place(x=10, y=15)


# 輸入欄 vcmd 註冊為檢查函數，驗證每次鍵入的字元是否有效
vcmd = (window.register(validate_int), "%S")
entry = customtkinter.CTkEntry(
    master=background_frame_1,
    height=30,
    width=120,
    validate="key", 
    validatecommand=vcmd)
entry.place(x=210, y=15)


# 提交按鈕
submit_btn = customtkinter.CTkButton(
    master=background_frame_1,
    height=30,
    width=60, 
    text="提交",
    font=("Microsoft JhengHei", 16, "bold"),
    command=submit
    )
submit_btn.place(x=340, y=15)

# 輸出欄-閏年判斷
is_leap_year_var = customtkinter.StringVar()
is_leap_year_entry = customtkinter.CTkEntry(
    master=background_frame_1,
    height=30,
    width=120, 
    font=("Microsoft JhengHei", 16, "bold"),
    textvariable=is_leap_year_var, 
    state="readonly"
    )
is_leap_year_entry.place(x=410, y=15)
is_leap_year_var.set("是否為閏年?")


# 輸出群組
background_main = customtkinter.CTkFrame(
    master=window,
    height=440,
    width=550,
)
background_main.pack(pady=10)


# 輸出欄-單月曆
main_output_text = customtkinter.CTkTextbox(
    master=background_main,
    height=350,
    width=500, 
    state="normal"
    )
main_output_text.place(x=25, y=25)
main_output_text.insert(customtkinter.END, "此處用於輸出月曆")
main_output_text.configure(state="disabled",font=("Courier New", 20))

# 換頁按鈕 (上一頁)
previous_btn = customtkinter.CTkButton(
    master=background_main,
    height=30,
    width=100,  
    text="上一頁", 
    font=("Microsoft JhengHei", 16, "bold"),
    command=previous_page
    )
previous_btn.place(x=25, y=390)

# 換頁按鈕 (下一頁)
next_btn = customtkinter.CTkButton(
    master=background_main,
    height=30,
    width=100,  
    text="下一頁", 
    font=("Microsoft JhengHei", 16, "bold"),
    command=next_page
    )
next_btn.place(x=425, y=390)

# 啟動視窗循環
window.mainloop()


# v1.0 閏年判斷
# v2.0 萬年曆
# v3.0 串列/方法化
# v4.0 使用 tkinter 套件嘗試建立 GUI 介面 (中英文字型對齊不易，故星期欄使用字串進行硬編碼)
# v5.0 在製作期末報告 GUI 時發現 customtkinter 套件，使用 chatGPT 進行套件語法轉換
# v5.1 發現空格縮排錯誤，經查發現是字體字寬不同導致，改用等寬字型-Courier New 輸出月曆