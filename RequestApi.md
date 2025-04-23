# 氣象數公開平台API使用說明
swagger api 請見 https://opendata.cwa.gov.tw/dist/opendata-swagger.html#/
### 套件依賴
需要安裝 requests
```
pip install requests
```

### 函數回傳格式
| 屬性名稱 |  型別 | 說明 |
|--|--|--|
| status |  boolean | 呼叫API是否成功 |
| code   |  int     | HTTP 代碼      |
| message|  string  | 訊息           |
| data   |  string  | API返回結果JSON|

### 縣市氣象資訊，同時提供3天或一週
使用說明
```python
import RequestApi as api

# 取得嘉義市三天預報
result = api.getWeatherByCity("嘉義市", 3)
if result['status']:
    print(result['data'])
else:
    print(result['message'])
# 取得嘉義市一週預報
result = api.getWeatherByCity("嘉義市", 7)
if result['status']:
    print(result['data'])
else:
    print(result['message'])
```
可以透過RequestAPI中的cityApi屬性取得
```python
import RequestApi as api

api = api.RequestApi()
# 取得縣市與API端點路徑 key為縣市 value為API路徑List第一個位置為3天，第二個位置為7天
print(api.cityApi)
# 只取得縣市
print(api.cityApi.keys())
# result
# dict_keys(['宜蘭縣', '桃園市', '新竹縣', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '屏東縣', '臺東縣', '花蓮縣', '澎湖縣', '基隆市', '新竹市', '嘉義市', '臺北市', '高雄市', '新北市', '臺中市', '臺南市', '連江縣', '金門縣'])
```

### 地震資訊
使用說明
```python
import RequestApi as api

api = api.RequestApi()
#小區域有感地震
result = api.getEarthquake(0)
if result['status']:
    print(result['data'])
else:
    print(result['message'])
#顯著有感地震
result = api.getEarthquake(1)
if result['status']:
    print(result['data'])
else:
    print(result['message'])
```
