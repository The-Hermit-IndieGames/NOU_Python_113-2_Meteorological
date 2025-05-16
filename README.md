# NOU_Python_113-2_Meteorological
### NOU Python 113-2 期末專題:氣象預報
---
### 流程圖:
 ```mermaid
flowchart LR
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
        Q[從 weather_icons 載入圖示] --> P
        O --> R[顯示地震結果]
        P --> S((呈現於主畫面))
        R --> S
        S --> B
    end

```
---