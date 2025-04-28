
# libraries Import
from functools import partial
from tkinter import *
from tkinter import ttk  # 需要額外引入 Treeview
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

##########################################################################################################################
###                                                                                                                    ###
###                                             負責其他區塊的請注意看到這裡                                             ###
###                                                                                                                    ###
##########################################################################################################################

# 提供程式運作的當前狀態
sqlStatusString = ""

# 輸入/輸出 串接函式 ======================================================================================================
def input_io_call(dict):
    # 顯示查詢文字並強制刷新
    output_text = f"資料庫查詢中，請稍候......"        
    Output_label.configure(text=output_text, text_color="#FFAA00")
    window.update()

    sqlStatusString = f"沒有可進行預測的資料"
    print(sqlStatusString)
    return -1


# GUI輸出顯示函式
def output_show(gui_output_float):
    global user_input_list

    # 形式正確的回傳值
    if(gui_output_float > 0):
        if (user_input_list["calculate_area"] == None or user_input_list["calculate_area"] == 0):
            # 輸入值無面積時，返回 萬元/坪(or 平方米)
            if(user_input_list["calculate_unit"] == 2):     # 單位:坪
                show_number = gui_output_float
                output_text = f"預期價格: {show_number:.2f}萬元/坪"
            elif(user_input_list["calculate_unit"] == 1):   # 單位:平方米 
                # 1坪 = 3.30579 平方公尺
                show_number = gui_output_float / 3.30579
                output_text = f"預期價格: {show_number:.2f}萬元/平方米"
            else:
                print("[GUI]錯誤! 未定義的單位")
        else:
            # 輸入值有面積時，返回 總價-萬元
            if(user_input_list["calculate_unit"] == 2):     # 單位:坪
                show_number = gui_output_float * user_input_list["calculate_area"]
                output_text = f"預期總價格: {show_number:.2f}萬元"
            elif(user_input_list["calculate_unit"] == 1):   # 單位:平方米 
                # 1坪 = 3.30579 平方公尺
                show_number = (gui_output_float * user_input_list["calculate_area"]) / 3.30579
                output_text = f"預期總價格: {show_number:.2f}萬元"
            else:
                print(f"[GUI]錯誤! 未定義的單位:{user_input_list["calculate_unit"]}")  
                output_text = f"錯誤! 未定義的單位:{user_input_list["calculate_unit"]}"
        Output_label.configure(text=output_text, text_color="#5555FF")
    
    # 錯誤代碼
    elif(gui_output_float == -1):
        output_text = f"[ERROR -1]沒有可進行預測的資料"        
        Output_label.configure(text=output_text, text_color="#CC0000")

    else:
        output_text = f"[ERROR ??]未知的錯誤代碼:{gui_output_float}"        
        Output_label.configure(text=output_text, text_color="#CC0000")



# I/O 、 處理函式 及 變數部分 =============================================================================================
# [I/O]輸入資料表
user_input_list = {
    "city":"",                  # str :     縣市,                                       必填：是 (預設:第一筆的key)
    "town":"",                  # str :     鄉鎮市區,                                   必填：是 (預設:第一筆的key)
    "ptype":[],                 # list :    1房地、2建物、3土地、4車位、5房地+車位,       必填：是 (預設:[1])
    "p_build": None,            # str :     門牌地址 :                                  必填：否 (預設:)
    "p_startY": None,           # int :     交易期間（年起）101-113,                     必填：是 (預設:101)
    "p_startM": None,           # int :     交易期間（月起）1-12,                        必填：是 (預設:1)
    "p_endY": None,             # int :     交易期間（年迄）101-113,                     必填：是 (預設:113)
    "p_endM": None,             # int :     交易期間（月迄）1-12,                        必填：是 (預設:12)
    "pmoney_unit": None,        # int :     單位（1 => 萬元 , 2 => 元)                   必填：是 (預設:1)
    "minp": None,               # int :     最小值(單價),                                必填：否 (預設:)
    "maxp": None,               # int :     最大值（單價）,                              必填：否 (預設:)
    "unit": None,               # int :     面積單位（1 => M^2 ，2 => 坪）,              必填：是 (預設:2)
    "mins": None,               # int :     最小值（坪數）,                              必填：否 (預設:)
    "maxs": None,               # int :     最大值（坪數）,                              必填：否 (預設:)
    "avg_var": None,            # int :     屋齡,                                       必填：否 (預設:)

    # 計算部分 (我們自訂的)
    "calculate_Y": None,        # int :     目標期間（年）,                          必填：是 (預設:)
    "calculate_M": None,        # int :     目標期間（月）,                          必填：是 (預設:)
    "calculate_unit": None,     # int :     面積單位（1 => M^2 ，2 => 坪）,          必填：是 (預設:2)
    "calculate_area": None      # int :     面積,                                    必填：是 (預設:)
}


# 屋齡
age_dict = {
    None: "不拘",
    1 : "5年以下",
    2 : "5~10年",
    3 : "10~20年",
    4 : "20~30年",
    5 : "30~40年",
    6 : "40年以上",
}



##########################################################################################################################
###                                                                                                                    ###
###                                             負責其他區塊的只需要看到這裡                                             ###
###                                                                                                                    ###
##########################################################################################################################



# 通用回調函數，根據選取值查詢對應字典，並匯入 user_input_list
def get_selected_key(selected_value, lookup_dict, code):
    global user_input_list
    for key, value in lookup_dict.items():
        if value == selected_value:
            user_input_list[code] = key
            print(f"[GUI]user_input_list.{code}: {user_input_list[code]}")
            return user_input_list[code]
            

# 通用回調函數 2，直接將回傳值匯入 user_input_list
def return_selected_key(return_value, code):
    global user_input_list

    # 如果為 CheckBox，則回傳列表並附加到指定的 code 鍵中
    if code == "ptype":
        if code not in user_input_list:
            user_input_list[code] = []  # 初始化為列表
        
        # 避免重複添加
        if return_value not in user_input_list[code]:
            user_input_list[code].append(return_value)
        else:
            # 若已存在於列表中，表示取消選擇，則移除該值
            user_input_list[code].remove(return_value)

    # 如果為 RadioButton，則回傳單一正整數，更新指定 code 的值
    else:
        user_input_list[code] = return_value

    print(f"[GUI]user_input_list[{code}]: {user_input_list[code]}")


# 通用輸入，直接將回傳值匯入 user_input_list
def entry_update(entry_value, code):
    global user_input_list

    user_input_list[code] = entry_value
    print(f"[GUI]user_input_list[{code}]: {user_input_list[code]}")
    return True


# 整數的通用輸入，直接將回傳值匯入 user_input_list
def validate_and_update(entry_value, code):
    global user_input_list
    if entry_value.isdigit() and int(entry_value) > 0:
        # 更新正整數值至 user_input_list[code]
        user_input_list[code] = int(entry_value)
        print(f"[GUI]user_input_list[{code}]: {user_input_list[code]}")
        return True
    elif entry_value == "":
        # 允許清空輸入
        user_input_list[code] = None
        return True
    else:
        # 非正整數則阻止顯示
        return False



# 生成結果按鈕(一階判斷)
def on_output_button():
    print("\n[GUI]開始檢查輸入資料表:")
    can_output = True
    wrong_time_range = False
    warning_text = "警告: "
    

    # 輸出警告文字或調用計算函數
    if(can_output == True):
        print("[GUI]輸入正確，調用計算函數")
        gui_output_float = input_io_call(user_input_list)
        output_show(gui_output_float)

    # 僅有起訖時間範圍錯誤
    elif (warning_text == "警告: " and wrong_time_range == True):
        warning_text = "警告: 起訖時間範圍錯誤"
        Output_label.configure(text=warning_text, text_color="#CC0000")
    
    # 輸入有缺漏
    else:
        # 找到最後一個 "、" 並替換為 " 為必填項目!"
        warning_text = warning_text[::-1].replace("、", "!目項填必為 ", 1)[::-1]
        if (wrong_time_range == True):
            warning_text += "\n警告: 起訖時間範圍錯誤"
        Output_label.configure(text=warning_text, text_color="#CC0000")
    



# 視窗控制 及 物件列表 =======================================================================================================

#window = Tk()                   # 初始化 tkinter 視窗
window = customtkinter.CTk()    # 初始化 customtkinter 視窗
window.title("房價預測器")
window.geometry("600x450")

# 設置外觀模式 (可選 "System", "Dark", "Light")
customtkinter.set_appearance_mode("System")  # 跟隨系統設置的深色/淺色模式

appearance_mode = 0

# 創建可滾動框架
scrollable_frame = customtkinter.CTkScrollableFrame(
    master=window, 
    width=600, 
    height=720,
    bg_color="transparent",
    fg_color="transparent",
    )
scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

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

# 頂部框架
top_frame = customtkinter.CTkFrame(
    master=scrollable_frame, 
    height=30, 
    fg_color="transparent"
    )
top_frame.pack(side="top", fill="x", pady=0)

# 外觀模式按鈕
appearance_btn = customtkinter.CTkButton(
    master=top_frame,
    height=25,
    width=60, 
    text="系統預設",
    font=("Microsoft JhengHei", 14, "bold"),
    command=update_appearance_mode
    )
appearance_btn.pack(side="right", anchor="n", pady=0)


radio_var_price = IntVar()
radio_var_areaA = IntVar()
radio_var_areaB = IntVar()


 ########################################  版面配置區  ########################################

# 大標 1
Title_1 = customtkinter.CTkLabel(
    master=top_frame,
    text="欲統計分析之交易資料條件範圍",
    font=("Microsoft JhengHei", 20, "bold"),
    anchor="w",  # 左對齊
    height=20,
    width=300,
    corner_radius=0,
    bg_color="transparent",
    fg_color="transparent",
)
Title_1.pack(pady=0, anchor="w")

# 註解 1
Title_1_info = customtkinter.CTkLabel(
    master=top_frame,
    text="填寫說明: 輸入之條件建議盡量與目標購置之房屋條件相近，以增加預測可參考性",
    font=("Microsoft JhengHei", 14),
    anchor="w",
    text_color="#646464",
    height=10,
    width=300,
    corner_radius=0,
    bg_color="transparent",
    fg_color="transparent",
)
Title_1_info.pack(pady=0, anchor="w")

# 底色框 1 ======================================================================= 位置
background_frame_1 = customtkinter.CTkFrame(
    master=scrollable_frame,
    height=80,
    width=560,
    # 使用自適應色彩
    # bg_color="transparent",    
    # fg_color="#c8c8c8",
    # text_color="#000000",
)
background_frame_1.pack(pady=5, anchor="w")

# Class_1_checkbox 房屋=1
Class_1_checkbox_1 = customtkinter.CTkCheckBox(
    master=background_frame_1,
    text="房地",
    font=("Microsoft JhengHei", 14),
    corner_radius=4,
    border_width=2,
    height=30,
    width=50,
    command=partial(return_selected_key, return_value=1, code="ptype"),
)
Class_1_checkbox_1.place(x=230, y=10)

# Class_1_checkbox 土地=2
Class_1_checkbox_2 = customtkinter.CTkCheckBox(
    master=background_frame_1,
    text="土地",
    font=("Microsoft JhengHei", 14),
    corner_radius=4,
    border_width=2,
    height=30,
    width=50,
    command=partial(return_selected_key, return_value=2, code="ptype"),
)
Class_1_checkbox_2.place(x=230, y=40)

# Class_1_checkbox 建物=3
Class_1_checkbox_3 = customtkinter.CTkCheckBox(
    master=background_frame_1,
    text="建物",
    font=("Microsoft JhengHei", 14),
    corner_radius=4,
    border_width=2,
    height=30,
    width=50,
    command=partial(return_selected_key, return_value=3, code="ptype"),
)
Class_1_checkbox_3.place(x=295, y=10)

# Class_1_checkbox 車位=4
Class_1_checkbox_4 = customtkinter.CTkCheckBox(
    master=background_frame_1,
    text="車位",
    font=("Microsoft JhengHei", 14),
    corner_radius=4,
    border_width=2,
    height=30,
    width=50,
    command=partial(return_selected_key, return_value=4, code="ptype"),
)
Class_1_checkbox_4.place(x=295, y=40)

# Class_1_entry 門牌/社區名稱
validate_command_code0 = (window.register(partial(entry_update, code="p_build")), '%P')

Class_1_entry = customtkinter.CTkEntry(
    master=background_frame_1,
    placeholder_text="門牌/社區名稱",
    font=("Microsoft JhengHei", 14),
    height=50,
    width=120,
    border_width=2,
    corner_radius=6,
    validate="key", 
    validatecommand=validate_command_code0
)
Class_1_entry.place(x=430, y=15)

# 底色框 3 ======================================================================= 單價
background_frame_3 = customtkinter.CTkFrame(
    master=scrollable_frame,
    height=60,
    width=360,
)
background_frame_3.pack(pady=5, anchor="w")

# Class_3_title 單價
Class_3_title = customtkinter.CTkLabel(
    master=background_frame_3,
    text="單價:",
    font=("Microsoft JhengHei", 16, "bold"),
    height=40,
    width=60,
    corner_radius=0,
    )
Class_3_title.place(x=5, y=10)

# Class_3_radioButton 萬元=1
Class_3_radioButton_1 = customtkinter.CTkRadioButton(
    master=background_frame_3,
    variable=radio_var_price,
    value=10000,
    text="萬元",
    font=("Microsoft JhengHei", 14),
    height=20,
    width=40,
    command=partial(return_selected_key, return_value=1, code="pmoney_unit"),
    )
Class_3_radioButton_1.place(x=70, y=5)

# Class_3_radioButton 元=2
Class_3_radioButton_2 = customtkinter.CTkRadioButton(
    master=background_frame_3,
    variable=radio_var_price,
    value=1,
    text="元",
    font=("Microsoft JhengHei", 14),
    height=20,
    width=40,
    command=partial(return_selected_key, return_value=2, code="pmoney_unit"),
    )
Class_3_radioButton_2.place(x=70, y=35)

# Class_3_entry 最小
validate_command_code1 = (window.register(partial(validate_and_update, code="minp")), '%P')

Class_3_entry_1 = customtkinter.CTkEntry(
    master=background_frame_3,
    placeholder_text="最小",
    font=("Microsoft JhengHei", 14),
    height=30,
    width=80,
    border_width=2,
    corner_radius=6,
    validate="key", 
    validatecommand=validate_command_code1
    )
Class_3_entry_1.place(x=150, y=15)

# Class_3_label
Class_3_label = customtkinter.CTkLabel(
    master=background_frame_3,
    text="~",
    font=("Microsoft JhengHei", 18),
    height=30,
    width=25,
    corner_radius=0,
    )
Class_3_label.place(x=240, y=15)

# Class_3_entry 最大
validate_command_code2 = (window.register(partial(validate_and_update, code="maxp")), '%P')

Class_3_entry_2 = customtkinter.CTkEntry(
    master=background_frame_3,
    placeholder_text="最大",
    font=("Microsoft JhengHei", 14),
    height=30,
    width=80,
    border_width=2,
    corner_radius=6,
    validate="key", 
    validatecommand=validate_command_code2
    )
Class_3_entry_2.place(x=270, y=15)

# 底色框 5 ======================================================================= 屋齡
background_frame_5 = customtkinter.CTkFrame(
    master=scrollable_frame,
    height=60,
    width=190,
)
background_frame_5.pack(pady=5, anchor="w")

# Class_5_title
Class_5_title = customtkinter.CTkLabel(
    master=background_frame_5,
    text="屋齡:",
    font=("Microsoft JhengHei", 16, "bold"),
    height=40,
    width=60,
    corner_radius=0,
    )
Class_5_title.place(x=0, y=10)

# 屋齡-選單
Class_5_optionMenu = customtkinter.CTkOptionMenu(
    master=background_frame_5,
    values=list(age_dict.values()),
    command=partial(get_selected_key, lookup_dict=age_dict, code="avg_var"),
    font=("Microsoft JhengHei", 14),
    hover=True,
    height=40,
    width=80,
    corner_radius=6,
    )
Class_5_optionMenu.place(x=55, y=10)

"""
 ########################################  資料輸出區  ########################################
"""

# 生成資料按鈕
Output_button = customtkinter.CTkButton(
    master=scrollable_frame,
    text="生成資料",
    font=("Microsoft JhengHei", 18, "bold"),
    hover=True,
    height=50,
    width=140,
    border_width=2,
    corner_radius=6,
    command=on_output_button,
    )
Output_button.pack(pady=10, anchor="center")

# 輸出區
Output_label = customtkinter.CTkLabel(
    master=scrollable_frame,
    text="輸出區",
    font=("Microsoft JhengHei", 16, "bold"),
    text_color="#0033ff",
    height=70,
    width=580,
    corner_radius=0,
    bg_color="transparent",
    fg_color="transparent",
    )
Output_label.pack(pady=20, anchor="center")

# 表格、作圖 ======================================================================= 位置

# 建立 Treeview 表格
tree = ttk.Treeview(scrollable_frame, columns=("Name", "Age", "City"), show="headings")
tree.heading("Name", text="姓名")
tree.heading("Age", text="年齡")
tree.heading("City", text="城市")

# 插入一些資料
tree.insert("", "end", values=("小明", 25, "台北"))
tree.insert("", "end", values=("小華", 30, "新北"))
tree.insert("", "end", values=("小美", 28, "台中"))

tree.pack(fill="both", expand=True, padx=10, pady=10)


# 建立 matplotlib 圖表
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4, 5], [2, 3, 5, 7, 11], marker='o')
ax.set_title("簡單折線圖")
ax.set_xlabel("X 軸")
ax.set_ylabel("Y 軸")

# 將 matplotlib 圖表嵌入到 customtkinter
canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


#run the main loop
window.mainloop()

