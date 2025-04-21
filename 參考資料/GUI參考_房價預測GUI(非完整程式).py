
# libraries Import
from functools import partial
from tkinter import *
import customtkinter
from lib.MySQL import MySQL
from Select import Select
from lib.Tools import Tools
from predictive_model import predictive_model

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

    # 調閱資料庫
    tools = Tools()
    sqlParams = tools.changeToSelectDict(dict)
    queryBuilder =  Select().createQuery(sqlParams)
    with MySQL() as db:
        sqlStatusString = "資料庫查詢中．．．"
        print(sqlStatusString)
        result = db.query(queryBuilder[0], queryBuilder[1])
        count = len(result)
        sqlStatusString = f"查詢到{count}筆交易紀錄．．．"
        print(sqlStatusString)
        if count > 0:
            data = tools.getKeyByDict(result)
            userInput = {
                "calculate_Y": dict['calculate_Y'],
                "calculate_M": dict['calculate_M'],
            }
            sqlStatusString = f"進行預測"
            print(sqlStatusString)
            amount = predictive_model(userInput, data)
            sqlStatusString = f"預測完成輸出結果"
            print(sqlStatusString)
            return round(amount, 2)
        else:
            sqlStatusString = f"沒有可進行預測的資料"
            print(sqlStatusString)
            return -1
    print(dict)
    
    # 一律回傳 萬元/每單位面積。 須注意單位為何 "calculate_unit" （1 => M^2 ，2 => 坪）
    # 一坪等於3.3058平方公尺


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


# 資料型態-鍵值表 (選單名稱與輸出值) =======================================================================================
# 縣市
city_dict = {
    None: "縣市　",
    "C":"基隆市",
    "A":"臺北市",
    "F":"新北市",
    "H":"桃園市",
    "O":"新竹市",
    "J":"新竹縣",
    "K":"苗栗縣",
    "B":"臺中市",
    "M":"南投縣",
    "N":"彰化縣",
    "P":"雲林縣",
    "I":"嘉義市",
    "Q":"嘉義縣",
    "D":"臺南市",
    "E":"高雄市",
    "T":"屏東縣",
    "G":"宜蘭縣",
    "U":"花蓮縣",
    "V":"臺東縣",
    "X":"澎湖縣",
    "W":"金門縣",
    "Z":"連江縣"
}


# 行政區
town_dict = {
    None:[{"code": None,"title": "鄉鎮市區"}],
    "C":[
        {
            "code": "C02",
            "title": "七堵區"
        },
        {
            "code": "C05",
            "title": "中山區"
        },
        {
            "code": "C01",
            "title": "中正區"
        },
        {
            "code": "C04",
            "title": "仁愛區"
        },
        {
            "code": "C06",
            "title": "安樂區"
        },
        {
            "code": "C07",
            "title": "信義區"
        },
        {
            "code": "C03",
            "title": "暖暖區"
        }
    ],          
    "A":[
        {
            "code": "A15",
            "title": "士林區"
        },
        {
            "code": "A09",
            "title": "大同區"
        },
        {
            "code": "A02",
            "title": "大安區"
        },
        {
            "code": "A10",
            "title": "中山區"
        },
        {
            "code": "A03",
            "title": "中正區"
        },
        {
            "code": "A14",
            "title": "內湖區"
        },
        {
            "code": "A11",
            "title": "文山區"
        },
        {
            "code": "A16",
            "title": "北投區"
        },
        {
            "code": "A01",
            "title": "松山區"
        },
        {
            "code": "A17",
            "title": "信義區"
        },
        {
            "code": "A13",
            "title": "南港區"
        },
        {
            "code": "A05",
            "title": "萬華區"
        }
    ],
    "F":[
        {
            "code": "F32",
            "title": "八里區"
        },
        {
            "code": "F30",
            "title": "三芝區"
        },
        {
            "code": "F05",
            "title": "三重區"
        },
        {
            "code": "F15",
            "title": "三峽區"
        },
        {
            "code": "F19",
            "title": "土城區"
        },
        {
            "code": "F18",
            "title": "中和區"
        },
        {
            "code": "F03",
            "title": "五股區"
        },
        {
            "code": "F22",
            "title": "平溪區"
        },
        {
            "code": "F33",
            "title": "永和區"
        },
        {
            "code": "F31",
            "title": "石門區"
        },
        {
            "code": "F08",
            "title": "石碇區"
        },
        {
            "code": "F28",
            "title": "汐止區"
        },
        {
            "code": "F10",
            "title": "坪林區"
        },
        {
            "code": "F02",
            "title": "林口區"
        },
        {
            "code": "F14",
            "title": "板橋區"
        },
        {
            "code": "F25",
            "title": "金山區"
        },
        {
            "code": "F06",
            "title": "泰山區"
        },
        {
            "code": "F11",
            "title": "烏來區"
        },
        {
            "code": "F24",
            "title": "貢寮區"
        },
        {
            "code": "F27",
            "title": "淡水區"
        },
        {
            "code": "F09",
            "title": "深坑區"
        },
        {
            "code": "F07",
            "title": "新店區"
        },
        {
            "code": "F01",
            "title": "新莊區"
        },
        {
            "code": "F21",
            "title": "瑞芳區"
        },
        {
            "code": "F26",
            "title": "萬里區"
        },
        {
            "code": "F17",
            "title": "樹林區"
        },
        {
            "code": "F23",
            "title": "雙溪區"
        },
        {
            "code": "F04",
            "title": "蘆洲區"
        },
        {
            "code": "F16",
            "title": "鶯歌區"
        }
    ],
    "H":[
        {
            "code": "H08",
            "title": "八德區"
        },
        {
            "code": "H06",
            "title": "大園區"
        },
        {
            "code": "H02",
            "title": "大溪區"
        },
        {
            "code": "H03",
            "title": "中壢區"
        },
        {
            "code": "H10",
            "title": "平鎮區"
        },
        {
            "code": "H01",
            "title": "桃園區"
        },
        {
            "code": "H13",
            "title": "復興區"
        },
        {
            "code": "H11",
            "title": "新屋區"
        },
        {
            "code": "H04",
            "title": "楊梅區"
        },
        {
            "code": "H09",
            "title": "龍潭區"
        },
        {
            "code": "H07",
            "title": "龜山區"
        },
        {
            "code": "H05",
            "title": "蘆竹區"
        },
        {
            "code": "H12",
            "title": "觀音區"
        }
    ],
    "O":[
        {
            "code": "O01",
            "title": "新竹市"
        }
    ],
    "J":[
        {
            "code": "J15",
            "title": "五峰鄉"
        },
        {
            "code": "J12",
            "title": "北埔鄉"
        },
        {
            "code": "J14",
            "title": "尖石鄉"
        },
        {
            "code": "J05",
            "title": "竹北市"
        },
        {
            "code": "J02",
            "title": "竹東鎮"
        },
        {
            "code": "J13",
            "title": "峨眉鄉"
        },
        {
            "code": "J06",
            "title": "湖口鄉"
        },
        {
            "code": "J04",
            "title": "新埔鎮"
        },
        {
            "code": "J09",
            "title": "新豐鄉"
        },
        {
            "code": "J08",
            "title": "橫山鄉"
        },
        {
            "code": "J03",
            "title": "關西鎮"
        },
        {
            "code": "J11",
            "title": "寶山鄉"
        },
        {
            "code": "J10",
            "title": "芎林鄉"
        }
    ],
    "K":[
        {
            "code": "K06",
            "title": "三義鄉"
        },
        {
            "code": "K13",
            "title": "三灣鄉"
        },
        {
            "code": "K15",
            "title": "大湖鄉"
        },
        {
            "code": "K04",
            "title": "公館鄉"
        },
        {
            "code": "K09",
            "title": "竹南鎮"
        },
        {
            "code": "K07",
            "title": "西湖鄉"
        },
        {
            "code": "K16",
            "title": "卓蘭鎮"
        },
        {
            "code": "K14",
            "title": "南庄鄉"
        },
        {
            "code": "K12",
            "title": "後龍鎮"
        },
        {
            "code": "K01",
            "title": "苗栗市"
        },
        {
            "code": "K02",
            "title": "苑裡鎮"
        },
        {
            "code": "K18",
            "title": "泰安鄉"
        },
        {
            "code": "K03",
            "title": "通霄鎮"
        },
        {
            "code": "K11",
            "title": "造橋鄉"
        },
        {
            "code": "K17",
            "title": "獅潭鄉"
        },
        {
            "code": "K05",
            "title": "銅鑼鄉"
        },
        {
            "code": "K10",
            "title": "頭份市"
        },
        {
            "code": "K08",
            "title": "頭屋鄉"
        }
    ],
    "B":[
        {
            "code": "B11",
            "title": "大甲區"
        },
        {
            "code": "B22",
            "title": "大安區"
        },
        {
            "code": "B24",
            "title": "大肚區"
        },
        {
            "code": "B28",
            "title": "大里區"
        },
        {
            "code": "B18",
            "title": "大雅區"
        },
        {
            "code": "B01",
            "title": "中區"
        },
        {
            "code": "B27",
            "title": "太平區"
        },
        {
            "code": "B08",
            "title": "北屯區"
        },
        {
            "code": "B05",
            "title": "北區"
        },
        {
            "code": "B21",
            "title": "外埔區"
        },
        {
            "code": "B20",
            "title": "石岡區"
        },
        {
            "code": "B15",
            "title": "后里區"
        },
        {
            "code": "B06",
            "title": "西屯區"
        },
        {
            "code": "B04",
            "title": "西區"
        },
        {
            "code": "B13",
            "title": "沙鹿區"
        },
        {
            "code": "B29",
            "title": "和平區"
        },
        {
            "code": "B02",
            "title": "東區"
        },
        {
            "code": "B10",
            "title": "東勢區"
        },
        {
            "code": "B07",
            "title": "南屯區"
        },
        {
            "code": "B03",
            "title": "南區"
        },
        {
            "code": "B23",
            "title": "烏日區"
        },
        {
            "code": "B16",
            "title": "神岡區"
        },
        {
            "code": "B14",
            "title": "梧棲區"
        },
        {
            "code": "B12",
            "title": "清水區"
        },
        {
            "code": "B19",
            "title": "新社區"
        },
        {
            "code": "B17",
            "title": "潭子區"
        },
        {
            "code": "B25",
            "title": "龍井區"
        },
        {
            "code": "B09",
            "title": "豐原區"
        },
        {
            "code": "B26",
            "title": "霧峰區"
        }
    ],
    "M":[
        {
            "code": "M08",
            "title": "中寮鄉"
        },
        {
            "code": "M13",
            "title": "仁愛鄉"
        },
        {
            "code": "M11",
            "title": "水里鄉"
        },
        {
            "code": "M06",
            "title": "名間鄉"
        },
        {
            "code": "M04",
            "title": "竹山鎮"
        },
        {
            "code": "M12",
            "title": "信義鄉"
        },
        {
            "code": "M01",
            "title": "南投市"
        },
        {
            "code": "M02",
            "title": "埔里鎮"
        },
        {
            "code": "M03",
            "title": "草屯鎮"
        },
        {
            "code": "M10",
            "title": "國姓鄉"
        },
        {
            "code": "M09",
            "title": "魚池鄉"
        },
        {
            "code": "M07",
            "title": "鹿谷鄉"
        },
        {
            "code": "M05",
            "title": "集集鎮"
        }
    ],
    "N":[
        {
            "code": "N20",
            "title": "二水鄉"
        },
        {
            "code": "N08",
            "title": "二林鎮"
        },
        {
            "code": "N15",
            "title": "大村鄉"
        },
        {
            "code": "N24",
            "title": "大城鄉"
        },
        {
            "code": "N04",
            "title": "北斗鎮"
        },
        {
            "code": "N18",
            "title": "永靖鄉"
        },
        {
            "code": "N07",
            "title": "田中鎮"
        },
        {
            "code": "N21",
            "title": "田尾鄉"
        },
        {
            "code": "N25",
            "title": "竹塘鄉"
        },
        {
            "code": "N10",
            "title": "伸港鄉"
        },
        {
            "code": "N12",
            "title": "秀水鄉"
        },
        {
            "code": "N03",
            "title": "和美鎮"
        },
        {
            "code": "N19",
            "title": "社頭鄉"
        },
        {
            "code": "N23",
            "title": "芳苑鄉"
        },
        {
            "code": "N13",
            "title": "花壇鄉"
        },
        {
            "code": "N14",
            "title": "芬園鄉"
        },
        {
            "code": "N05",
            "title": "員林市"
        },
        {
            "code": "N17",
            "title": "埔心鄉"
        },
        {
            "code": "N16",
            "title": "埔鹽鄉"
        },
        {
            "code": "N22",
            "title": "埤頭鄉"
        },
        {
            "code": "N02",
            "title": "鹿港鎮"
        },
        {
            "code": "N26",
            "title": "溪州鄉"
        },
        {
            "code": "N06",
            "title": "溪湖鎮"
        },
        {
            "code": "N01",
            "title": "彰化市"
        },
        {
            "code": "N11",
            "title": "福興鄉"
        },
        {
            "code": "N09",
            "title": "線西鄉"
        }
    ],
    "P":[
        {
            "code": "P11",
            "title": "二崙鄉"
        },
        {
            "code": "P19",
            "title": "口湖鄉"
        },
        {
            "code": "P05",
            "title": "土庫鎮"
        },
        {
            "code": "P08",
            "title": "大埤鄉"
        },
        {
            "code": "P17",
            "title": "元長鄉"
        },
        {
            "code": "P01",
            "title": "斗六市"
        },
        {
            "code": "P02",
            "title": "斗南鎮"
        },
        {
            "code": "P20",
            "title": "水林鄉"
        },
        {
            "code": "P06",
            "title": "北港鎮"
        },
        {
            "code": "P07",
            "title": "古坑鄉"
        },
        {
            "code": "P16",
            "title": "台西鄉"
        },
        {
            "code": "P18",
            "title": "四湖鄉"
        },
        {
            "code": "P04",
            "title": "西螺鎮"
        },
        {
            "code": "P14",
            "title": "東勢鄉"
        },
        {
            "code": "P10",
            "title": "林內鄉"
        },
        {
            "code": "P03",
            "title": "虎尾鎮"
        },
        {
            "code": "P12",
            "title": "崙背鄉"
        },
        {
            "code": "P13",
            "title": "麥寮鄉"
        },
        {
            "code": "P15",
            "title": "褒忠鄉"
        },
        {
            "code": "P09",
            "title": "莿桐鄉"
        }
    ],
    "I":[
        {
            "code": "I01",
            "title": "嘉義市"
        }
    ],
    "Q":[
        {
            "code": "Q04",
            "title": "大林鎮"
        },
        {
            "code": "Q18",
            "title": "大埔鄉"
        },
        {
            "code": "Q14",
            "title": "中埔鄉"
        },
        {
            "code": "Q08",
            "title": "六腳鄉"
        },
        {
            "code": "Q12",
            "title": "太保市"
        },
        {
            "code": "Q13",
            "title": "水上鄉"
        },
        {
            "code": "Q03",
            "title": "布袋鎮"
        },
        {
            "code": "Q05",
            "title": "民雄鄉"
        },
        {
            "code": "Q02",
            "title": "朴子市"
        },
        {
            "code": "Q15",
            "title": "竹崎鄉"
        },
        {
            "code": "Q09",
            "title": "東石鄉"
        },
        {
            "code": "Q20",
            "title": "阿里山鄉"
        },
        {
            "code": "Q16",
            "title": "梅山鄉"
        },
        {
            "code": "Q11",
            "title": "鹿草鄉"
        },
        {
            "code": "Q17",
            "title": "番路鄉"
        },
        {
            "code": "Q07",
            "title": "新港鄉"
        },
        {
            "code": "Q06",
            "title": "溪口鄉"
        },
        {
            "code": "Q10",
            "title": "義竹鄉"
        }
    ],
    "D":[
        {
            "code": "D22",
            "title": "七股區"
        },
        {
            "code": "D16",
            "title": "下營區"
        },
        {
            "code": "D19",
            "title": "大內區"
        },
        {
            "code": "D30",
            "title": "山上區"
        },
        {
            "code": "D08",
            "title": "中西區"
        },
        {
            "code": "D32",
            "title": "仁德區"
        },
        {
            "code": "D17",
            "title": "六甲區"
        },
        {
            "code": "D24",
            "title": "北門區"
        },
        {
            "code": "D04",
            "title": "北區"
        },
        {
            "code": "D31",
            "title": "左鎮區"
        },
        {
            "code": "D39",
            "title": "永康區"
        },
        {
            "code": "D36",
            "title": "玉井區"
        },
        {
            "code": "D12",
            "title": "白河區"
        },
        {
            "code": "D07",
            "title": "安平區"
        },
        {
            "code": "D29",
            "title": "安定區"
        },
        {
            "code": "D06",
            "title": "安南區"
        },
        {
            "code": "D21",
            "title": "西港區"
        },
        {
            "code": "D20",
            "title": "佳里區"
        },
        {
            "code": "D18",
            "title": "官田區"
        },
        {
            "code": "D14",
            "title": "東山區"
        },
        {
            "code": "D01",
            "title": "東區"
        },
        {
            "code": "D38",
            "title": "南化區"
        },
        {
            "code": "D02",
            "title": "南區"
        },
        {
            "code": "D13",
            "title": "後壁區"
        },
        {
            "code": "D11",
            "title": "柳營區"
        },
        {
            "code": "D23",
            "title": "將軍區"
        },
        {
            "code": "D15",
            "title": "麻豆區"
        },
        {
            "code": "D27",
            "title": "善化區"
        },
        {
            "code": "D26",
            "title": "新化區"
        },
        {
            "code": "D28",
            "title": "新市區"
        },
        {
            "code": "D09",
            "title": "新營區"
        },
        {
            "code": "D37",
            "title": "楠西區"
        },
        {
            "code": "D25",
            "title": "學甲區"
        },
        {
            "code": "D35",
            "title": "龍崎區"
        },
        {
            "code": "D33",
            "title": "歸仁區"
        },
        {
            "code": "D34",
            "title": "關廟區"
        },
        {
            "code": "D10",
            "title": "鹽水區"
        }
    ],
    "E":[
        {
            "code": "E05",
            "title": "三民區"
        },
        {
            "code": "E16",
            "title": "大社區"
        },
        {
            "code": "E14",
            "title": "大寮區"
        },
        {
            "code": "E15",
            "title": "大樹區"
        },
        {
            "code": "E11",
            "title": "小港區"
        },
        {
            "code": "E17",
            "title": "仁武區"
        },
        {
            "code": "E35",
            "title": "內門區"
        },
        {
            "code": "E32",
            "title": "六龜區"
        },
        {
            "code": "E03",
            "title": "左營區"
        },
        {
            "code": "E27",
            "title": "永安區"
        },
        {
            "code": "E22",
            "title": "田寮區"
        },
        {
            "code": "E33",
            "title": "甲仙區"
        },
        {
            "code": "E34",
            "title": "杉林區"
        },
        {
            "code": "E38",
            "title": "那瑪夏區"
        },
        {
            "code": "E19",
            "title": "岡山區"
        },
        {
            "code": "E13",
            "title": "林園區"
        },
        {
            "code": "E23",
            "title": "阿蓮區"
        },
        {
            "code": "E07",
            "title": "前金區"
        },
        {
            "code": "E09",
            "title": "前鎮區"
        },
        {
            "code": "E31",
            "title": "美濃區"
        },
        {
            "code": "E26",
            "title": "茄萣區"
        },
        {
            "code": "E36",
            "title": "茂林區"
        },
        {
            "code": "E08",
            "title": "苓雅區"
        },
        {
            "code": "E37",
            "title": "桃源區"
        },
        {
            "code": "E29",
            "title": "梓官區"
        },
        {
            "code": "E18",
            "title": "鳥松區"
        },
        {
            "code": "E25",
            "title": "湖內區"
        },
        {
            "code": "E06",
            "title": "新興區"
        },
        {
            "code": "E04",
            "title": "楠梓區"
        },
        {
            "code": "E24",
            "title": "路竹區"
        },
        {
            "code": "E02",
            "title": "鼓山區"
        },
        {
            "code": "E30",
            "title": "旗山區"
        },
        {
            "code": "E10",
            "title": "旗津區"
        },
        {
            "code": "E12",
            "title": "鳳山區"
        },
        {
            "code": "E20",
            "title": "橋頭區"
        },
        {
            "code": "E21",
            "title": "燕巢區"
        },
        {
            "code": "E28",
            "title": "彌陀區"
        },
        {
            "code": "E01",
            "title": "鹽埕區"
        }
    ],
    "T":[
        {
            "code": "T08",
            "title": "九如鄉"
        },
        {
            "code": "T26",
            "title": "三地門鄉"
        },
        {
            "code": "T13",
            "title": "內埔鄉"
        },
        {
            "code": "T14",
            "title": "竹田鄉"
        },
        {
            "code": "T33",
            "title": "牡丹鄉"
        },
        {
            "code": "T23",
            "title": "車城鄉"
        },
        {
            "code": "T09",
            "title": "里港鄉"
        },
        {
            "code": "T21",
            "title": "佳冬鄉"
        },
        {
            "code": "T30",
            "title": "來義鄉"
        },
        {
            "code": "T25",
            "title": "枋山鄉"
        },
        {
            "code": "T16",
            "title": "枋寮鄉"
        },
        {
            "code": "T03",
            "title": "東港鎮"
        },
        {
            "code": "T19",
            "title": "林邊鄉"
        },
        {
            "code": "T06",
            "title": "長治鄉"
        },
        {
            "code": "T20",
            "title": "南州鄉"
        },
        {
            "code": "T01",
            "title": "屏東市"
        },
        {
            "code": "T04",
            "title": "恆春鎮"
        },
        {
            "code": "T31",
            "title": "春日鄉"
        },
        {
            "code": "T18",
            "title": "崁頂鄉"
        },
        {
            "code": "T29",
            "title": "泰武鄉"
        },
        {
            "code": "T22",
            "title": "琉球鄉"
        },
        {
            "code": "T11",
            "title": "高樹鄉"
        },
        {
            "code": "T15",
            "title": "新埤鄉"
        },
        {
            "code": "T17",
            "title": "新園鄉"
        },
        {
            "code": "T32",
            "title": "獅子鄉"
        },
        {
            "code": "T05",
            "title": "萬丹鄉"
        },
        {
            "code": "T12",
            "title": "萬巒鄉"
        },
        {
            "code": "T24",
            "title": "滿州鄉"
        },
        {
            "code": "T28",
            "title": "瑪家鄉"
        },
        {
            "code": "T02",
            "title": "潮州鎮"
        },
        {
            "code": "T27",
            "title": "霧臺鄉"
        },
        {
            "code": "T07",
            "title": "麟洛鄉"
        },
        {
            "code": "T10",
            "title": "鹽埔鄉"
        }
    ],
    "G":[
        {
            "code": "G10",
            "title": "三星鄉"
        },
        {
            "code": "G11",
            "title": "大同鄉"
        },
        {
            "code": "G07",
            "title": "五結鄉"
        },
        {
            "code": "G08",
            "title": "冬山鄉"
        },
        {
            "code": "G04",
            "title": "壯圍鄉"
        },
        {
            "code": "G01",
            "title": "宜蘭市"
        },
        {
            "code": "G12",
            "title": "南澳鄉"
        },
        {
            "code": "G05",
            "title": "員山鄉"
        },
        {
            "code": "G02",
            "title": "頭城鎮"
        },
        {
            "code": "G03",
            "title": "礁溪鄉"
        },
        {
            "code": "G06",
            "title": "羅東鎮"
        },
        {
            "code": "G09",
            "title": "蘇澳鎮"
        }
    ],
    "U":[
        {
            "code": "U03",
            "title": "玉里鎮"
        },
        {
            "code": "U02",
            "title": "光復鄉"
        },
        {
            "code": "U05",
            "title": "吉安鄉"
        },
        {
            "code": "U11",
            "title": "秀林鄉"
        },
        {
            "code": "U13",
            "title": "卓溪鄉"
        },
        {
            "code": "U01",
            "title": "花蓮市"
        },
        {
            "code": "U10",
            "title": "富里鄉"
        },
        {
            "code": "U04",
            "title": "新城鄉"
        },
        {
            "code": "U09",
            "title": "瑞穗鄉"
        },
        {
            "code": "U12",
            "title": "萬榮鄉"
        },
        {
            "code": "U06",
            "title": "壽豐鄉"
        },
        {
            "code": "U07",
            "title": "鳳林鎮"
        },
        {
            "code": "U08",
            "title": "豐濱鄉"
        }
    ],
    "V":[
        {
            "code": "V05",
            "title": "大武鄉"
        },
        {
            "code": "V06",
            "title": "太麻里鄉"
        },
        {
            "code": "V01",
            "title": "台東市"
        },
        {
            "code": "V02",
            "title": "成功鎮"
        },
        {
            "code": "V10",
            "title": "池上鄉"
        },
        {
            "code": "V04",
            "title": "卑南鄉"
        },
        {
            "code": "V12",
            "title": "延平鄉"
        },
        {
            "code": "V07",
            "title": "東河鄉"
        },
        {
            "code": "V15",
            "title": "金峰鄉"
        },
        {
            "code": "V08",
            "title": "長濱鄉"
        },
        {
            "code": "V13",
            "title": "海端鄉"
        },
        {
            "code": "V09",
            "title": "鹿野鄉"
        },
        {
            "code": "V14",
            "title": "達仁鄉"
        },
        {
            "code": "V11",
            "title": "綠島鄉"
        },
        {
            "code": "V03",
            "title": "關山鎮"
        },
        {
            "code": "V16",
            "title": "蘭嶼鄉"
        }
    ],
    "X":[
        {
            "code": "X06",
            "title": "七美鄉"
        },
        {
            "code": "X03",
            "title": "白沙鄉"
        },
        {
            "code": "X04",
            "title": "西嶼鄉"
        },
        {
            "code": "X01",
            "title": "馬公市"
        },
        {
            "code": "X05",
            "title": "望安鄉"
        },
        {
            "code": "X02",
            "title": "湖西鄉"
        }
    ],
    "W":[
        {
            "code": "W02",
            "title": "金沙鎮"
        },
        {
            "code": "W03",
            "title": "金城鎮"
        },
        {
            "code": "W01",
            "title": "金湖鎮"
        },
        {
            "code": "W04",
            "title": "金寧鄉"
        },
        {
            "code": "W05",
            "title": "烈嶼鄉"
        },
        {
            "code": "W06",
            "title": "烏坵鄉"
        }
    ],
    "Z":[
        {
            "code": "Z02",
            "title": "北竿鄉"
        },
        {
            "code": "Z04",
            "title": "東引鄉"
        },
        {
            "code": "Z01",
            "title": "南竿鄉"
        },
        {
            "code": "Z03",
            "title": "莒光鄉"
        }
    ]
}


# 通用年/月
year_dict = { 
    None:"年",
    101:"101年", 102:"102年", 103:"103年", 104:"104年", 105:"105年", 106:"106年", 107:"107年", 
    108:"108年", 109:"109年", 110:"110年", 111:"111年", 112:"112年", 113:"113年" 
}

mon_dict = { 
    None:"月",
    1:"1月", 2:"2月", 3:"3月", 4:"4月", 5:"5月", 6:"6月", 
    7:"7月", 8:"8月", 9:"9月", 10:"10月", 11:"11月", 12:"12月" 
}


# 目標年 (我只抓10年)
target_year_dict = {
    None:"目標年",
    114:"114年", 115:"115年", 116:"116年", 117:"117年", 118:"118年", 
    119:"119年", 120:"120年", 121:"121年", 122:"122年", 123:"123年"
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

    # 縣市
    if user_input_list["city"] == "" or user_input_list["city"] == None :
        print("[GUI]警告! <city>項目為空! 該項目為必填!")
        can_output = False
        warning_text += "縣市、"

    # 鄉鎮市區
    if user_input_list["town"] == "" or user_input_list["town"] == None :
        print("[GUI]警告! <town>項目為空! 該項目為必填!")
        can_output = False
        warning_text += "鄉鎮市區、"

    # 類型
    if user_input_list["ptype"] == [] :
        print("[GUI]警告! <ptype>項目為空! 指定為預設值<[1]>")
        user_input_list["ptype"] = [1]
        Class_1_checkbox_1.select()

    # 門牌/社區名稱
    if user_input_list["p_build"] == "門牌/社區名稱" :  # 清除預設顯示文字
        user_input_list["p_build"] = None

    # 起始年月~結束年月
    if user_input_list["p_startY"] == None :
        print("[GUI]警告! <p_startY>項目為空! 指定為預設值<101>")
        user_input_list["p_startY"] = 101
        Class_2_optionMenu_year1.set("101年")
        
    if user_input_list["p_startM"] == None :
        print("[GUI]警告! <p_startM>項目為空! 指定為預設值<1>")
        user_input_list["p_startM"] = 1
        Class_2_optionMenu_mon1.set("1月")
        
    if user_input_list["p_endY"] == None :
        print("[GUI]警告! <p_endY>項目為空! 指定為預設值<113>")
        user_input_list["p_endY"] = 113
        Class_2_optionMenu_year2.set("113年")
        
    if user_input_list["p_endM"] == None :
        print("[GUI]警告! <p_endM>項目為空! 指定為預設值<12>")
        user_input_list["p_endM"] = 12
        Class_2_optionMenu_mon2.set("12月")

    # 起訖限制
    if user_input_list["p_startY"] > user_input_list["p_endY"] :
        print("[GUI]警告! <p_startY>大於<p_endY>")
        can_output = False
        wrong_time_range = True
        
    if user_input_list["p_startY"] == user_input_list["p_endY"] and user_input_list["p_startM"] > user_input_list["p_endM"]:
        print("[GUI]警告! <p_startM>大於<p_endM>")
        can_output = False
        wrong_time_range = True

    # 單位
    if user_input_list["pmoney_unit"] == None :
        print("[GUI]警告! <pmoney_unit>項目為空! 指定為預設值<1>")
        user_input_list["pmoney_unit"] = 1
        Class_3_radioButton_1.select()

    # 面積單位
    if user_input_list["unit"] == None :
        print("[GUI]警告! <unit>項目為空! 指定為預設值<2>")
        user_input_list["unit"] = 2
        Class_4_radioButton_2.select()

    # 目標期間（年月）
    if user_input_list["calculate_Y"] == "" or user_input_list["calculate_Y"] == None :
        print("[GUI]警告! <calculate_Y>項目為空! 該項目為必填!")
        can_output = False
        warning_text += "目標期間(年)、"
        
    if user_input_list["calculate_M"] == "" or user_input_list["calculate_M"] == None :
        print("[GUI]警告! <calculate_M>項目為空! 該項目為必填!")
        can_output = False
        warning_text += "目標期間(月)、"

    # 目標面積單位
    if user_input_list["calculate_unit"] == None :
        print("[GUI]警告! <calculate_unit>項目為空! 指定為預設值<2>")
        user_input_list["calculate_unit"] = 2
        Class_7_radioButton_2.select()
    

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
window.geometry("600x720")

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

# 選單-縣市
def update_town_options(selected_city):
    # 使用通用回調函數獲取 code
    city_code=get_selected_key(selected_city, city_dict, code="city")
    print(f"\n[GUI]目前選擇縣市:{selected_city},code = {city_code}")

    # 取得對應城市代碼的資料
    options = town_dict.get(city_code, [])
    
    # 提取 title 為顯示值，code 為回傳值
    display_values = [item["title"] for item in options]
    code_values = [item["code"] for item in options]
    
    # 更新 option_menu 的值
    Class_1_optionMenu_2.configure(values=display_values)
    Class_1_optionMenu_2.set(display_values[0])  # 預設選擇第一個鄉鎮市區
    user_input_list["town"] = code_values[0]
    print(f"[GUI]user_input_list.town(選單預設): {user_input_list["town"]}")
    
    # 設置選項回調函數，根據 title 回傳 code
    def on_option_selected(choice):
        index = display_values.index(choice)  # 取得選擇的索引
        selected_code = code_values[index]  # 根據索引獲取對應的 code
        user_input_list["town"] = selected_code
        print(f"[GUI]user_input_list.town: {user_input_list["town"]}")

    Class_1_optionMenu_2.configure(command=on_option_selected)


Class_1_optionMenu_1 = customtkinter.CTkOptionMenu(
    master=background_frame_1,
    values=list(city_dict.values()),
    command=update_town_options,
    font=("Microsoft JhengHei", 14),
    height=40,
    width=60,
    corner_radius=8,
)
Class_1_optionMenu_1.place(x=10, y=20)

# 選單-鄉鎮市區
Class_1_optionMenu_2 = customtkinter.CTkOptionMenu(
    master=background_frame_1,
    values=["鄉鎮市區"],
    font=("Microsoft JhengHei", 14),
    height=40,
    width=95,
    corner_radius=8,
)
Class_1_optionMenu_2.place(x=110, y=20)

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

# Class_1_checkbox 房地+車位=5
Class_1_checkbox_5 = customtkinter.CTkCheckBox(
    master=background_frame_1,
    text="房地\n +\n車位",
    font=("Microsoft JhengHei", 14),
    corner_radius=4,
    border_width=2,
    height=50,
    width=50,
    command=partial(return_selected_key, return_value=5, code="ptype"),
)
Class_1_checkbox_5.place(x=360, y=15)

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


# 底色框 2 ======================================================================= 時間
background_frame_2 = customtkinter.CTkFrame(
    master=scrollable_frame,
    height=80,
    width=560,
)
background_frame_2.pack(pady=5, anchor="w")

# Class_2_title
Class_2_title = customtkinter.CTkLabel(
    master=background_frame_2,
    text="交易期間:",
    font=("Microsoft JhengHei", 16, "bold"),
    height=40,
    width=80,
    corner_radius=0,
)
Class_2_title.place(x=5, y=15)

# 起始年
Class_2_optionMenu_year1 = customtkinter.CTkOptionMenu(
    master=background_frame_2,
    values=list(year_dict.values()),
    command=partial(get_selected_key, lookup_dict=year_dict, code="p_startY"),
    font=("Microsoft JhengHei", 14),
    hover=True,
    height=40,
    width=100,
    corner_radius=6,
)
Class_2_optionMenu_year1.place(x=90, y=15)

# 起始月
Class_2_optionMenu_mon1 = customtkinter.CTkOptionMenu(
    master=background_frame_2,
    values=list(mon_dict.values()),
    command=partial(get_selected_key, lookup_dict=mon_dict, code="p_startM"),
    font=("Microsoft JhengHei", 14),
    hover=True,
    height=40,
    width=60,
    corner_radius=6,
)
Class_2_optionMenu_mon1.place(x=200, y=15)

# Class_2_label_2
Class_2_label_2 = customtkinter.CTkLabel(
    master=background_frame_2,
    text="至",
    font=("Microsoft JhengHei", 16),
    height=40,
    width=20,
    corner_radius=0,
)
Class_2_label_2.place(x=280, y=15)

# 結束年
Class_2_optionMenu_year2 = customtkinter.CTkOptionMenu(
    master=background_frame_2,
    values=list(year_dict.values()),
    command=partial(get_selected_key, lookup_dict=year_dict, code="p_endY"),
    font=("Microsoft JhengHei", 14),
    hover=True,
    height=40,
    width=100,
    corner_radius=6,
)
Class_2_optionMenu_year2.place(x=310, y=15)

# 結束月
Class_2_optionMenu_mon2 = customtkinter.CTkOptionMenu(
    master=background_frame_2,
    values=list(mon_dict.values()),
    command=partial(get_selected_key, lookup_dict=mon_dict, code="p_endM"),
    font=("Microsoft JhengHei", 14),
    hover=True,
    height=40,
    width=60,
    corner_radius=6,
)
Class_2_optionMenu_mon2.place(x=420, y=15)

# Class_2_label_4
Class_2_label_4 = customtkinter.CTkLabel(
    master=background_frame_2,
    text="止",
    font=("Microsoft JhengHei", 16),
    height=40,
    width=20,
    corner_radius=0,
)
Class_2_label_4.place(x=510, y=15)

# Class_2_title_info
Class_2_title_info = customtkinter.CTkLabel(
    master=background_frame_2,
    text="填寫說明: 建議選擇欲購置時間的前半年至一年左右",
    font=("Microsoft JhengHei", 14),
    anchor="w",
    text_color="#646464",
    height=20,
    width=300,
    corner_radius=0,
)
Class_2_title_info.place(x=10, y=57)

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

# 底色框 4 ======================================================================= 面積
background_frame_4 = customtkinter.CTkFrame(
    master=scrollable_frame,
    height=60,
    width=360,
)
background_frame_4.pack(pady=5, anchor="w")

# Class_4_title 面積
Class_4_title = customtkinter.CTkLabel(
    master=background_frame_4,
    text="面積:",
    font=("Microsoft JhengHei", 16, "bold"),
    height=40,
    width=60,
    corner_radius=0,
    )
Class_4_title.place(x=5, y=10)

# Class_4_radioButton 平方米 M^2 = 1
Class_4_radioButton_1 = customtkinter.CTkRadioButton(
    master=background_frame_4,
    variable=radio_var_areaA,
    value=1,
    text="平方米",
    font=("Microsoft JhengHei", 14),
    height=20,
    width=60,
    command=partial(return_selected_key, return_value=1, code="unit"),
    )
Class_4_radioButton_1.place(x=70, y=5)

# Class_4_radioButton 坪 = 2
Class_4_radioButton_2 = customtkinter.CTkRadioButton(
    master=background_frame_4,
    variable=radio_var_areaA,
    value=2,
    text="坪",
    font=("Microsoft JhengHei", 14),
    height=20,
    width=60,
    command=partial(return_selected_key, return_value=2, code="unit"),
    )
Class_4_radioButton_2.place(x=70, y=35)

# Class_4_entry 最小
validate_command_code3 = (window.register(partial(validate_and_update, code="mins")), '%P')

Class_4_entry_1 = customtkinter.CTkEntry(
    master=background_frame_4,
    placeholder_text="最小",
    font=("Microsoft JhengHei", 14),
    height=30,
    width=80,
    border_width=2,
    corner_radius=6,
    validate="key", 
    validatecommand=validate_command_code3
    )
Class_4_entry_1.place(x=150, y=15)

# Class_4_label
Class_4_label = customtkinter.CTkLabel(
    master=background_frame_4,
    text="~",
    font=("Microsoft JhengHei", 18),
    height=30,
    width=25,
    corner_radius=0,
    )
Class_4_label.place(x=240, y=15)

# Class_4_entry 最大
validate_command_code4 = (window.register(partial(validate_and_update, code="maxs")), '%P')

Class_4_entry_2 = customtkinter.CTkEntry(
    master=background_frame_4,
    placeholder_text="最大",
    font=("Microsoft JhengHei", 14),
    height=30,
    width=80,
    border_width=2,
    corner_radius=6,
    validate="key", 
    validatecommand=validate_command_code4
    )
Class_4_entry_2.place(x=270, y=15)

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


# 大標 2 ======================================================================= 目標
Title_2 = customtkinter.CTkLabel(
    master=scrollable_frame,
    text="目標購置之房屋資訊",
    font=("Microsoft JhengHei", 20, "bold"),
    anchor="w",
    height=20,
    width=300,
    corner_radius=0,
    )
Title_2.pack(pady=10, anchor="w")


# 底色框 6 ======================================================================= 目標時間
background_frame_6 = customtkinter.CTkFrame(
    master=scrollable_frame,
    height=60,
    width=350,
)
background_frame_6.pack(pady=0, anchor="w")

# Class_6_title
Class_6_title = customtkinter.CTkLabel(
    master=background_frame_6,
    text="時間:",
    font=("Microsoft JhengHei", 16, "bold"),
    height=40,
    width=60,
    corner_radius=0,
    )
Class_6_title.place(x=5, y=10)

# 目標時間 年
Class_6_optionMenu_year = customtkinter.CTkOptionMenu(
    master=background_frame_6,
    values=list(target_year_dict.values()),
    command=partial(get_selected_key, lookup_dict=target_year_dict, code="calculate_Y"),
    font=("Microsoft JhengHei", 14),
    hover=True,
    height=40,
    width=80,
    corner_radius=6,
    )
Class_6_optionMenu_year.place(x=80, y=10)

# 目標時間 月
Class_6_optionMenu_mon = customtkinter.CTkOptionMenu(
    master=background_frame_6,
    values=list(mon_dict.values()),
    command=partial(get_selected_key, lookup_dict=mon_dict, code="calculate_M"),
    font=("Microsoft JhengHei", 14),
    hover=True,
    height=40,
    width=80,
    corner_radius=6,
    )
Class_6_optionMenu_mon.place(x=200, y=10)

# 底色框 7 ======================================================================= 目標面積
background_frame_7 = customtkinter.CTkFrame(
    master=scrollable_frame,
    height=60,
    width=350,
)
background_frame_7.pack(pady=10, anchor="w")

# Class_7_title
Class_7_title = customtkinter.CTkLabel(
    master=background_frame_7,
    text="面積:",
    font=("Microsoft JhengHei", 16, "bold"),
    height=40,
    width=60,
    corner_radius=0,
    )
Class_7_title.place(x=5, y=10)

# 選項-M^2 = 1
Class_7_radioButton_1 = customtkinter.CTkRadioButton(
    master=background_frame_7,
    variable=radio_var_areaB,
    value=1,
    text="平方米",
    font=("Microsoft JhengHei", 14),
    height=20,
    width=60,
    command=partial(return_selected_key, return_value=1, code="calculate_unit"),
    )
Class_7_radioButton_1.place(x=80, y=5)

# 選項-坪 = 2
Class_7_radioButton_2 = customtkinter.CTkRadioButton(
    master=background_frame_7,
    variable=radio_var_areaB,
    value=2,
    text="坪",
    font=("Microsoft JhengHei", 14),
    height=20,
    width=60,
    command=partial(return_selected_key, return_value=2, code="calculate_unit"),
    )
Class_7_radioButton_2.place(x=80, y=35)

# 輸入面積
validate_command_code5 = (window.register(partial(validate_and_update, code="calculate_area")), '%P')

Class_7_entry = customtkinter.CTkEntry(
    master=background_frame_7,
    placeholder_text="輸入面積",
    font=("Microsoft JhengHei", 14),
    height=40,
    width=120,
    border_width=2,
    corner_radius=6,
    validate="key", 
    validatecommand=validate_command_code5
    )
Class_7_entry.place(x=180, y=10)

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

#run the main loop
window.mainloop()

