# NOU_Python_113-2_Meteorological
 NOU Python 113-2 期末專題:氣象預報

Mermaid 3
 ```mermaid
flowchart TD
    %% 起點
    A((開始：開啟 GUI))

    %% GUI 模組
    subgraph 資料呈現 WeatherGUI.py
        A --> B[載入主畫面]
        B --> C[切換至 WeatherTab]
        B --> D[切換至 EarthquakeTab]
        B --> Z{外觀模式切換}
        Z --> B
        
        %% 天氣流程
        C --> E{選擇城市}
        E --> F[更新行政區]
        F --> G{選擇行政區}
        G --> H[執行 get_weather_by_loction]

        %% 地震流程
        D --> I{選擇地震類型}
        I --> J[執行 getEarthquake]
    end

    %% 資料處理模組
    subgraph 資料處理 app.py
        H --> K[處理輸入：城市、區域、元素]
        K --> L[呼叫 getWeatherByCity]
        M[篩選與整理氣象資料]
    end

    %% 資料蒐集模組
    subgraph 資料蒐集 RequestApi.py
        L --> N[存取氣象資料開放平臺 API]
        J --> O[依 mode_type 取得地震資料]
        N --> M
    end

    %% 顯示階段與結尾
    subgraph 資料呈現 WeatherGUI.py
    M --> P[顯示天氣結果]
        Q[載入圖示自 weather_icons] --> P

        O --> R[顯示地震結果]

        P --> S((呈現於主畫面))
        R --> S
    end

```
Mermaid 2
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
