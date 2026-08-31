# 世界国家猜猜猜 - 游戏设计文档

## 一、游戏概述

玩家需要猜出系统预设的国家，通过经纬度、人口、面积、GDP等信息逐步缩小范围。

## 二、数据表设计

### countries 表

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| id | INTEGER | 主键 | 1 |
| name | TEXT | 国家名称 | 中国 |
| capital | TEXT | 首都 | 北京 |
| capital_chars | INTEGER | 首都字数 | 2 |
| country_chars | INTEGER | 国家字数 | 2 |
| longitude | REAL | 首都经度 | 116.4 |
| latitude | REAL | 首都纬度 | 39.9 |
| population | REAL | 人口（亿） | 14.1 |
| area | REAL | 国土面积（万平方公里） | 960 |
| gdp_rank | INTEGER | GDP排名 | 2 |
| continent | TEXT | 所在大洲 | 亚洲 |

### 数据示例

```sql
CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    capital TEXT NOT NULL,
    capital_chars INTEGER NOT NULL,
    country_chars INTEGER NOT NULL,
    longitude REAL NOT NULL,
    latitude REAL NOT NULL,
    population REAL NOT NULL,
    area REAL NOT NULL,
    gdp_rank INTEGER NOT NULL,
    continent TEXT NOT NULL
);
```

## 三、游戏提示规则

### 1. 初始提示

进入游戏后，系统会提示：
- 国家名称：X个字
- 首都名称：X个字

### 2. 猜测后的提示

当玩家猜测一个国家后，系统会返回以下信息：

| 提示项 | 显示方式 | 示例 |
|--------|----------|------|
| 经度 | 偏东/偏西/接近 | "偏东15°" 或 "偏西3°" 或 "经度接近" |
| 纬度 | 偏北/偏南/接近 | "偏北8°" 或 "偏南2°" 或 "纬度接近" |
| 首都距离 | 计算直线距离 | "首都相距约2500公里" |
| 人口 | 更多/更少/接近 | "人口更多" 或 "人口更少" 或 "人口接近" |
| 面积 | 更大/更小/接近 | "面积更大" 或 "面积更小" 或 "面积接近" |
| GDP排名 | 更高/更低/接近 | "GDP排名更高" 或 "GDP排名更低" 或 "GDP排名接近" |
| 大洲 | 相同/不同 | "同大洲" 或 "不同大洲" |

### 3. 距离计算公式

使用Haversine公式计算两个经纬度之间的距离：

```python
import math

def calculate_distance(lon1, lat1, lon2, lat2):
    """
    计算两个经纬度之间的距离（公里）
    """
    R = 6371  # 地球半径（公里）
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance = R * c
    return round(distance)
```

### 4. 阈值设定

| 提示项 | "接近"阈值 | 说明 |
|--------|-----------|------|
| 经度 | ±5° | 差值在5度以内显示"接近" |
| 纬度 | ±5° | 差值在5度以内显示"接近" |
| 首都距离 | 500公里 | 距离在500公里以内显示"很近" |
| 人口 | ±20% | 差值在20%以内显示"接近" |
| 面积 | ±20% | 差值在20%以内显示"接近" |
| GDP排名 | ±5名 | 差值在5名以内显示"接近" |

## 四、游戏界面设计

### 初始界面

```
┌─────────────────────────────────────────┐
│           世界国家猜猜猜                 │
│                                         │
│  提示：国家名称 2个字，首都名称 2个字     │
│                                         │
│  ┌─────────────────────┐  ┌──────────┐ │
│  │ 请输入国家名称       │  │   猜测   │ │
│  └─────────────────────┘  └──────────┘ │
│                                         │
│  ─────────────────────────────────────  │
│  猜测记录：                             │
│  ─────────────────────────────────────  │
└─────────────────────────────────────────┘
```

### 猜测后界面

```
┌─────────────────────────────────────────┐
│           世界国家猜猜猜                 │
│                                         │
│  猜测：日本                             │
│  ─────────────────────────────────────  │
│  经度：偏东 15°                         │
│  纬度：偏北 8°                          │
│  首都距离：约 2500 公里                  │
│  人口：更少                             │
│  面积：更小                             │
│  GDP排名：更低（第3名）                  │
│  大洲：同大洲（亚洲）                    │
│  ─────────────────────────────────────  │
│                                         │
│  当前限定范围：                         │
│  • 经度：116° - 135°                    │
│  • 纬度：35° - 45°                      │
│  • 大洲：亚洲                           │
│  • 人口：1亿 - 15亿                     │
│  ─────────────────────────────────────  │
│                                         │
│  猜测记录：                             │
│  #1 日本 - 偏东·偏北·更小·更少          │
└─────────────────────────────────────────┘
```

## 五、国家数据（示例）

| 国家 | 首都 | 经度 | 纬度 | 人口(亿) | 面积(万km²) | GDP排名 | 大洲 |
|------|------|------|------|----------|-------------|---------|------|
| 中国 | 北京 | 116.4 | 39.9 | 14.1 | 960 | 2 | 亚洲 |
| 日本 | 东京 | 139.7 | 35.7 | 1.26 | 37.8 | 3 | 亚洲 |
| 韩国 | 首尔 | 127.0 | 37.6 | 0.52 | 10 | 10 | 亚洲 |
| 印度 | 新德里 | 77.2 | 28.6 | 14.2 | 328 | 5 | 亚洲 |
| 美国 | 华盛顿 | -77.0 | 38.9 | 3.3 | 937 | 1 | 北美洲 |
| 英国 | 伦敦 | -0.1 | 51.5 | 0.67 | 24.4 | 6 | 欧洲 |
| 法国 | 巴黎 | 2.3 | 48.9 | 0.67 | 64 | 7 | 欧洲 |
| 德国 | 柏林 | 13.4 | 52.5 | 0.83 | 35.7 | 4 | 欧洲 |
| 俄罗斯 | 莫斯科 | 37.6 | 55.8 | 1.44 | 1710 | 11 | 欧洲 |
| 巴西 | 巴西利亚 | -47.9 | -15.8 | 2.1 | 851 | 9 | 南美洲 |
| 澳大利亚 | 堪培拉 | 149.1 | -35.3 | 0.26 | 769 | 13 | 大洋洲 |
| 埃及 | 开罗 | 31.2 | 30.0 | 1.0 | 100 | 32 | 非洲 |
| 南非 | 比勒陀利亚 | 28.2 | -25.7 | 0.6 | 122 | 33 | 非洲 |
| 尼日利亚 | 阿布贾 | 7.5 | 9.1 | 2.2 | 92 | 27 | 非洲 |
| 墨西哥 | 墨西哥城 | -99.1 | 19.4 | 1.3 | 196 | 12 | 北美洲 |
| 阿根廷 | 布宜诺斯艾利斯 | -58.4 | -34.6 | 0.45 | 278 | 22 | 南美洲 |
| 沙特阿拉伯 | 利雅得 | 46.7 | 24.7 | 0.35 | 215 | 18 | 亚洲 |
| 土耳其 | 安卡拉 | 32.9 | 39.9 | 0.85 | 78 | 19 | 亚洲 |
| 印尼 | 雅加达 | 106.8 | -6.2 | 2.7 | 190 | 16 | 亚洲 |
| 泰国 | 曼谷 | 100.5 | 13.8 | 0.7 | 51 | 24 | 亚洲 |

## 六、扩展功能

### 1. 难度模式

- **简单模式**：只显示方向（偏东/偏西），不显示具体度数
- **普通模式**：显示方向和具体度数
- **困难模式**：只显示"接近/不接近"，不显示方向

### 2. 提示道具

- **提示1**：显示首都首字母
- **提示2**：显示所在大洲
- **提示3**：显示人口范围

### 3. 成就系统

- **连续猜对**：连续猜对N个国家
- **快速猜对**：在N次内猜对
- **完美猜对**：第1次就猜对

## 七、技术实现

### 数据库初始化

```python
def init_countries_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        capital TEXT NOT NULL,
        capital_chars INTEGER NOT NULL,
        country_chars INTEGER NOT NULL,
        longitude REAL NOT NULL,
        latitude REAL NOT NULL,
        population REAL NOT NULL,
        area REAL NOT NULL,
        gdp_rank INTEGER NOT NULL,
        continent TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()
```

### 距离计算

```python
import math

def calculate_distance(lon1, lat1, lon2, lat2):
    """计算两个经纬度之间的距离（公里）"""
    R = 6371
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return round(R * c)
```

### 比较逻辑

```python
def compare_countries(guess, answer):
    """比较两个国家，返回提示"""
    hints = []
    
    # 经度比较
    lon_diff = guess['longitude'] - answer['longitude']
    if abs(lon_diff) < 5:
        hints.append({"attr": "经度", "value": f"{guess['longitude']}°", "status": "接近"})
    elif lon_diff > 0:
        hints.append({"attr": "经度", "value": f"{guess['longitude']}°", "status": f"偏东 {abs(lon_diff):.1f}°"})
    else:
        hints.append({"attr": "经度", "value": f"{guess['longitude']}°", "status": f"偏西 {abs(lon_diff):.1f}°"})
    
    # 纬度比较
    lat_diff = guess['latitude'] - answer['latitude']
    if abs(lat_diff) < 5:
        hints.append({"attr": "纬度", "value": f"{guess['latitude']}°", "status": "接近"})
    elif lat_diff > 0:
        hints.append({"attr": "纬度", "value": f"{guess['latitude']}°", "status": f"偏北 {abs(lat_diff):.1f}°"})
    else:
        hints.append({"attr": "纬度", "value": f"{guess['latitude']}°", "status": f"偏南 {abs(lat_diff):.1f}°"})
    
    # 首都距离
    distance = calculate_distance(
        guess['longitude'], guess['latitude'],
        answer['longitude'], answer['latitude']
    )
    if distance < 500:
        hints.append({"attr": "首都距离", "value": f"{distance}公里", "status": "很近"})
    else:
        hints.append({"attr": "首都距离", "value": f"{distance}公里", "status": ""})
    
    # 人口比较
    pop_ratio = guess['population'] / answer['population']
    if abs(pop_ratio - 1) < 0.2:
        hints.append({"attr": "人口", "value": f"{guess['population']}亿", "status": "接近"})
    elif pop_ratio > 1:
        hints.append({"attr": "人口", "value": f"{guess['population']}亿", "status": "更多"})
    else:
        hints.append({"attr": "人口", "value": f"{guess['population']}亿", "status": "更少"})
    
    # 面积比较
    area_ratio = guess['area'] / answer['area']
    if abs(area_ratio - 1) < 0.2:
        hints.append({"attr": "面积", "value": f"{guess['area']}万km²", "status": "接近"})
    elif area_ratio > 1:
        hints.append({"attr": "面积", "value": f"{guess['area']}万km²", "status": "更大"})
    else:
        hints.append({"attr": "面积", "value": f"{guess['area']}万km²", "status": "更小"})
    
    # GDP排名比较
    gdp_diff = guess['gdp_rank'] - answer['gdp_rank']
    if abs(gdp_diff) < 5:
        hints.append({"attr": "GDP排名", "value": f"第{guess['gdp_rank']}名", "status": "接近"})
    elif gdp_diff > 0:
        hints.append({"attr": "GDP排名", "value": f"第{guess['gdp_rank']}名", "status": "更低"})
    else:
        hints.append({"attr": "GDP排名", "value": f"第{guess['gdp_rank']}名", "status": "更高"})
    
    # 大洲比较
    if guess['continent'] == answer['continent']:
        hints.append({"attr": "大洲", "value": guess['continent'], "status": "相同"})
    else:
        hints.append({"attr": "大洲", "value": guess['continent'], "status": "不同"})
    
    return hints
```
