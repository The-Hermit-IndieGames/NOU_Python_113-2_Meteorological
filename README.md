# NOU_Python_113-2_Meteorological
### NOU Python 113-2 期末專題:氣象預報
---
### 流程圖:
 ```mermaid
flowchart LR
    %% 起點
    A((開始：開啟 GUI))

    %% GUI 模組 - 垂直呈現
    subgraph WeatherGUI.py[資料呈現 WeatherGUI.py]
        direction TB
        A --> B[載入主畫面]
        B --> C[切換至<br>WeatherTab]
        B --> D[切換至<br>EarthquakeTab]
        B --> Z{外觀模式切換}
        Z --> B

        %% 天氣操作流程
        C --> E{選擇城市}
        E --> F[更新行政區]
        F --> G{選擇行政區}
        G --> H[執行<br>get_weather_by_loction]

        %% 地震操作流程
        D --> I{選擇地震類型}
        I --> J[執行<br>getEarthquake]
    end

    %% app.py 模組 - 水平排列
    subgraph app.py[資料處理 app.py]
        direction LR
        H --> L[呼叫<br>getWeatherByCity]
        L --> M[篩選與整理氣象資料]
    end

    %% API 模組 - 垂直排列
    subgraph RequestApi.py[資料蒐集 RequestApi.py]
        direction TB
        L --> N[存取氣象資料開放平臺 API]
        N --> M
        J --> O[依 mode_type<br>取得地震資料]
    end

    %% 顯示結果與結尾 - 水平
    subgraph 顯示與結束
        direction LR
        M --> P[顯示天氣結果]
        Q[從 weather_icons<br>載入圖示] --> P
        O --> R[顯示地震結果]
        P --> S((回主畫面))
        R --> S
        S --> T((結束))
    end

```
---