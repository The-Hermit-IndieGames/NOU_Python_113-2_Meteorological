import requests

class RequestApi:
    """
    提供HTTP request 呼叫API的快速類別
    """

    # 要呼叫的API URL位置
    url = 'https://opendata.cwa.gov.tw'

    # API版本
    version = 'v1'

    # API路由
    path = f'api/{version}/rest/datastore'

    # token
    apiAuth ={'Authorization': 'CWA-5B306D7D-A5ED-4639-8532-D1C274899F48'}

    # 定義請求標頭
    headers = {
        'User-Agent': 'python work',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    '''
    城市對應的API代碼陣列中第一個位置是3天預報，第二個位置是1週預報
    '''
    cityApi = {
        '宜蘭縣': ['F-D0047-001', 'F-D0047-003'],
        '桃園市': ['F-D0047-005', 'F-D0047-007'],
        '新竹縣': ['F-D0047-009', 'F-D0047-011'],
        '苗栗縣': ['F-D0047-013', 'F-D0047-015'],
        '彰化縣': ['F-D0047-017', 'F-D0047-019'],
        '南投縣': ['F-D0047-021', 'F-D0047-023'],
        '雲林縣': ['F-D0047-025', 'F-D0047-027'],
        '嘉義縣': ['F-D0047-029', 'F-D0047-031'],
        '屏東縣': ['F-D0047-033', 'F-D0047-035'],
        '臺東縣': ['F-D0047-037', 'F-D0047-039'],
        '花蓮縣': ['F-D0047-041', 'F-D0047-043'],
        '澎湖縣': ['F-D0047-045', 'F-D0047-047'],
        '基隆市': ['F-D0047-049', 'F-D0047-051'],
        '新竹市': ['F-D0047-053', 'F-D0047-055'],
        '嘉義市': ['F-D0047-057', 'F-D0047-059'],
        '臺北市': ['F-D0047-061', 'F-D0047-063'],
        '高雄市': ['F-D0047-065', 'F-D0047-067'],
        '新北市': ['F-D0047-069', 'F-D0047-071'],
        '臺中市': ['F-D0047-073', 'F-D0047-075'],
        '臺南市': ['F-D0047-077', 'F-D0047-079'],
        '連江縣': ['F-D0047-081', 'F-D0047-083'],
        '金門縣': ['F-D0047-085', 'F-D0047-087']
    }
    '''
    地震API
    '''
    earthquakeApi = [
        'E-A0016-001', # 小區域有感地震
        'E-A0015-001', # 顯著有感地震
    ]

    # 要呼叫的API端點
    apis = [
        'O-A0003-001', # 現在天氣觀測
        'F-C0032-001', # 臺灣各縣市天氣預報資料及國際都市天氣預報
        'A-B0062-001', # 日出日落
        'E-A0014-001', # 海嘯
    ]

    def setHeader(self, params = {}):
        """
        配置request http header要傳遞的內容
        """
        self.headers = {**self.headers, **params}
        return None

    def get(self, api, params = {}):
        """
        TODO 使用get方法呼叫API
        Args:
            self
            api (string): 要呼叫的API端點
            params (dict): {參數名稱1：參數值1， 參數名稱2：參數值2....}

        Returns:
            json

        Example:
            import Api from Api
            api = Api()
            api.get("{url}", {name: "Hi"})
        """
        uri = f"{self.url}/{self.path}/{api}"
        return self.send('get', uri, params)

    def send(self, method, api, params):
        """
        proxy 代理方法，對應方法發調用request對應的方法
        """
        response = {"status": False, "code":0, "message":None, "data": None}
        try:
            if(method.upper() == 'GET'):
                _r = requests.get(api, headers=self.headers, params={**params, **self.apiAuth})
            elif(method.upper() == 'POST'):
                _r = requests.post(api, headers=self.headers, data=params, params=self.apiAuth)
            else:
                response["message"] = f"錯誤的方法{method}"
                return response
                
            response["status"] = _r.status_code == 200
            response["code"] = _r.status_code
            response["message"] = "呼叫成功" if _r.status_code == 200 else "呼叫失敗"
            response["data"] = _r.json()
            return response

        except requests.exceptions.HTTPError as errh:
            response["message"] = f"HTTP錯誤: {errh}"
            return response
        except requests.exceptions.ConnectionError as errc:
            response["message"] = f"連接錯誤: {errc}"
            return response
        except requests.exceptions.Timeout as errt:
            response["message"] = f"超時錯誤: {errt}"
            return response
        except requests.exceptions.RequestException as err:
            response["message"] = f"無法預期的錯誤: {err}"
            return response
    
    def getWeatherByCity(self, city, days = 3):
        """
        取得指定城市的天氣資料
        Args:
            self
            city (string): 要取得的程式名稱（）
            days (int): 要取得的天數（3或7）
        Returns:
            json
        """
        index = 0 if days == 3 else 1
        #取得縣市與API端點
        api = self.cityApi.get(city)
        if api is None:
            return {"status": False, "message": f"無法取得{city}的API端點"}
        #取得API端點
        if index >= len(api):
            return {"status": False, "message": f"無法取得{city}的{days}天預報API端點"}
        api = api[index]
        #取得API資料
        return self.get(api)
    
    
    def getEarthquake(self, modeType = 0):
        """
        取得地震資料
        Args:
            self
            type (int): 0:小區域有感地震 1:顯著有感地震
        """
        #取得API端點
        api = self.earthquakeApi[modeType]
        #取得API資料
        return self.get(api)