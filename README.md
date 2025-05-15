# NOU_Python_113-2_Meteorological
 NOU Python 113-2 期末專題:氣象預報

 ```mermaid
flowchart TD
    %% 資料呈現模組
    subgraph 資料呈現 WeatherGUI.py
        A[開始：使用者操作介面]
        B[呼叫 get_weather_by_loction：傳入城市、區域、元素]
        C[呼叫 getEarthquake：傳入地震類型模式]
        D[從 weather_icons 資料夾載入對應圖示]
        E[顯示天氣與地震資訊]
        F[結束：資料呈現完成]
    end

    %% 資料處理模組
    subgraph 資料處理 app.py
        G[接收城市與區域等資訊]
        H[呼叫 getWeatherByCity：取得指定城市天氣資料]
        I[處理並篩選所需氣象元素]
        J[回傳資料給 WeatherGUI.py]
    end

    %% 資料蒐集模組
    subgraph 資料蒐集 RequestApi.py
        K[使用 氣象資料開放平臺 API 取得天氣資料]
        M[取得地震資料：依照 mode_type 模式]
    end

    %% 流程連線
    A --> B
    A --> C
    A --> D
    B --> G
    G --> H
    H --> K
    K --> I
    I --> J
    J --> E
    C --> M
    M --> E
    D --> E
    E --> F
```

```mermaid
flowchart TD
    Start([開始])--> MainWindow[GUI介面]
    
    subgraph 主功能模組
        MainWindow --> WeatherTab[天氣預報頁面]
        MainWindow --> EarthquakeTab[地震資訊頁面]
    end
    
    subgraph 天氣預報流程
        WeatherTab --> CitySelect{城市選擇}
        CitySelect -->|選擇城市| DistrictUpdate[更新行政區]
        DistrictUpdate --> DistrictSelect{行政區選擇}
        DistrictSelect -->|確認| WeatherQuery[查詢天氣]
        WeatherQuery --> WeatherDataProcess[資料處理]
        WeatherDataProcess --> WeatherDisplay[天氣資訊顯示]
    end
    
    subgraph 地震資訊流程
        EarthquakeTab --> EarthquakeTypeSelect{地震類型選擇}
        EarthquakeTypeSelect -->|選擇類型| EarthquakeQuery[查詢地震資訊]
        EarthquakeQuery --> EarthquakeDataProcess[資料處理]
        EarthquakeDataProcess --> EarthquakeDisplay[地震資訊顯示]
    end
    
    subgraph 外觀控制
        MainWindow --> AppearanceMode[外觀模式切換]
    end
    
    WeatherDisplay --> MainWindow
    EarthquakeDisplay --> MainWindow
    AppearanceMode --> MainWindow
 ```