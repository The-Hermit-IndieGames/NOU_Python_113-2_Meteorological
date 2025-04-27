from RequestApi import RequestApi
from datetime import datetime

app = RequestApi()


def classify_period_by_end_time(start_time: str, end_time: str) -> tuple[str, str]:
    """
    根據end_time判斷白天或晚上，回傳日期與時段
    """

    start_date = datetime.fromisoformat(start_time)
    end_date = datetime.fromisoformat(end_time)
    date = start_date.strftime("%Y-%m-%d")

    if end_date.hour == 18:
        period = "白天"
    elif end_date.hour == 6:
        period = "晚上"
    else:
        period = "其他"

    return date, period


def extract_element_value(element_value,  allowed_element_type):
    """
    根據每種資料類型(ElementName) 提取7日資料，轉為統一格式
    參數：
    - element_value：含有單一氣象元素資料的字典（包含 ElementName、Time 區段）
    - allowed_element_type：允許的 ElementName 清單，用來過濾需要的氣象項目

    回傳範例：
    extracted = [
            {
                "date": 2025-05-18,
                "period": 白天,
                "value":  {'Temperature': '21' }
            }
        ]
    """
    element_type = element_value.get("ElementName")

    if element_type not in allowed_element_type:
        return []

    extracted = []

    for time_block in element_value.get("Time", []):
        start_time = time_block.get("StartTime")
        end_time = time_block.get("EndTime")

        date, period = classify_period_by_end_time(start_time, end_time)
        for value in time_block.get("ElementValue", []):
            values = {}
            for value_type, actual_value in value.items():
                values[value_type] = actual_value
            extracted.append(
                {
                    "date": date,
                    "period": period,
                    "values": values
                }
            )
    return extracted


def parse_weather_elements(WeatherElement, allowed_element_type):
    """
    處理整個 WeatherElement 列表，整理出所有需要的項目
    參數：
    - WeatherElement: List，每個元素是 dict，包含氣象元素資訊（ElementName, Time 等）
    - allowed_element_type：允許的 ElementName 清單，用來過濾需要的氣象項目 
    """
    results = []
    for element in WeatherElement:
        element_type = element.get("ElementName")
        element_values = extract_element_value(element, allowed_element_type)
        if element_values:
            results.append(
                {
                    "elementType": element_type,
                    "elementValue": element_values
                }
            )
    return results


def get_weather_by_loction(city: str, district: str, target_elements: list = ['天氣預報綜合描述']):
    """
    獲取行政區天氣資訊
    參數：
    - city(str)：市區
    - district(str)：行政區
    - target_elements(list): ["最高溫度", "天氣預報綜合描述", "平均相對濕度", "天氣現象", "紫外線指數", "最高體感溫度", "降雨機率", "風向", "平均溫度"... ]

    回傳格式範例：{
        "city": "臺北市",
        "district": "大安區",
        "weather": [
            {
                "elementType":'紫外線指數',
                "elementValue":[
                    {
                        'date': '2025-04-26',
                        'period': '白天', 
                        'value': { 'UVIndex': '7', 'UVExposureLevel': '高量級'}
                    },
                    ...   
                ]
            },
            ...
        ]
    }
    """
    response = app.getWeatherByCity(city, 7)

    if not response.get("status"):
        return

    data = response.get("data")

    locations = data["records"]["Locations"]
    if not locations:
        return []

    location_list = locations[0].get("Location", [])
    for loc in location_list:
        location_name = loc.get("LocationName")
        if location_name != district:
            continue
        weather_element = loc.get("WeatherElement", [])
        weather_data = parse_weather_elements(weather_element, target_elements)

        return {
            "city": locations[0].get("LocationsName", []),
            "district": location_name,
            "weather": weather_data
        }

    print("找不到指定行政區")
    return []


# if __name__ == "__main__":
#     result = get_weather_by_loction("臺北市", "大安區", ["平均溫度"])
#     print(result)
