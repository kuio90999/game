import math
from database import get_connection

def get_all_countries():
    """获取所有国家列表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM countries ORDER BY id')
    countries = cursor.fetchall()
    
    conn.close()
    return [dict(c) for c in countries]

def get_country_by_name(name):
    """根据名字查找国家"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM countries WHERE name = ?', (name,))
    country = cursor.fetchone()
    
    conn.close()
    return country

def get_country_by_id(country_id):
    """根据ID查找国家"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM countries WHERE id = ?', (country_id,))
    country = cursor.fetchone()
    
    conn.close()
    return country

def calculate_distance(lon1, lat1, lon2, lat2):
    """计算两个经纬度之间的距离（公里）"""
    R = 6371  # 地球半径（公里）
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return round(R * c)

def compare_countries(guess, answer):
    """比较两个国家，返回提示"""
    hints = []
    
    # 经度比较
    lon_diff = guess['longitude'] - answer['longitude']
    guess_lon_prefix = "东经" if guess['longitude'] >= 0 else "西经"
    guess_lon_value = abs(guess['longitude'])
    
    if abs(lon_diff) < 5:
        hints.append({"attr": "经度", "value": f"{guess_lon_prefix}{guess_lon_value}°", "status": "接近"})
    elif lon_diff > 0:
        hints.append({"attr": "经度", "value": f"{guess_lon_prefix}{guess_lon_value}°", "status": "比该国更西"})
    else:
        hints.append({"attr": "经度", "value": f"{guess_lon_prefix}{guess_lon_value}°", "status": "比该国更东"})
    
    # 纬度比较
    lat_diff = guess['latitude'] - answer['latitude']
    guess_lat_prefix = "北纬" if guess['latitude'] >= 0 else "南纬"
    guess_lat_value = abs(guess['latitude'])
    
    if abs(lat_diff) < 5:
        hints.append({"attr": "纬度", "value": f"{guess_lat_prefix}{guess_lat_value}°", "status": "接近"})
    elif lat_diff > 0:
        hints.append({"attr": "纬度", "value": f"{guess_lat_prefix}{guess_lat_value}°", "status": "比该国更南"})
    else:
        hints.append({"attr": "纬度", "value": f"{guess_lat_prefix}{guess_lat_value}°", "status": "比该国更北"})
    
    # 首都距离
    distance = calculate_distance(
        guess['longitude'], guess['latitude'],
        answer['longitude'], answer['latitude']
    )
    if distance < 500:
        hints.append({"attr": "首都距离", "value": f"{distance}公里", "status": "<500公里"})
    else:
        hints.append({"attr": "首都距离", "value": f"{distance}公里", "status": ""})
    
    # 人口比较
    pop_ratio = guess['population'] / answer['population']
    if abs(pop_ratio - 1) < 0.2:
        hints.append({"attr": "人口", "value": f"{guess['population']}亿", "status": "接近"})
    elif pop_ratio > 1:
        hints.append({"attr": "人口", "value": f"{guess['population']}亿", "status": "比该国更少"})
    else:
        hints.append({"attr": "人口", "value": f"{guess['population']}亿", "status": "比该国更多"})
    
    # 面积比较
    area_ratio = guess['area'] / answer['area']
    if abs(area_ratio - 1) < 0.2:
        hints.append({"attr": "面积", "value": f"{guess['area']}万km²", "status": "接近"})
    elif area_ratio > 1:
        hints.append({"attr": "面积", "value": f"{guess['area']}万km²", "status": "比该国更小"})
    else:
        hints.append({"attr": "面积", "value": f"{guess['area']}万km²", "status": "比该国更大"})
    
    # GDP排名比较
    gdp_diff = guess['gdp_rank'] - answer['gdp_rank']
    if abs(gdp_diff) < 5:
        hints.append({"attr": "GDP排名", "value": f"第{guess['gdp_rank']}名", "status": "接近"})
    elif gdp_diff > 0:
        hints.append({"attr": "GDP排名", "value": f"第{guess['gdp_rank']}名", "status": "比该国更高"})
    else:
        hints.append({"attr": "GDP排名", "value": f"第{guess['gdp_rank']}名", "status": "比该国更低"})
    
    return hints

def summarize_country_hints(guesses, answer):
    """总结当前已知信息"""
    summary = []
    
    # 经度范围（答案经度的最小值和最大值）
    lon_min = None  # 答案经度的下界
    lon_max = None  # 答案经度的上界
    lon_close = None  # 接近的经度值
    
    # 纬度范围（答案纬度的最小值和最大值）
    lat_min = None  # 答案纬度的下界
    lat_max = None  # 答案纬度的上界
    lat_close = None  # 接近的纬度值
    
    # 人口范围（答案人口的最小值和最大值）
    pop_min = None
    pop_max = None
    pop_close = None
    
    # 面积范围（答案面积的最小值和最大值）
    area_min = None
    area_max = None
    area_close = None
    
    # GDP排名范围（答案GDP排名的最小值和最大值）
    gdp_min = None  # 排名数字越小越好
    gdp_max = None
    gdp_close = None
    
    for guess in guesses:
        # 经度范围推断
        lon_diff = guess['longitude'] - answer['longitude']
        if abs(lon_diff) < 5:
            lon_close = guess['longitude']
        elif lon_diff > 0:
            # 猜测经度 > 答案经度，答案在西边，猜测经度是上界
            if lon_max is None or guess['longitude'] < lon_max:
                lon_max = guess['longitude']
        else:
            # 猜测经度 < 答案经度，答案在东边，猜测经度是下界
            if lon_min is None or guess['longitude'] > lon_min:
                lon_min = guess['longitude']
        
        # 纬度范围推断
        lat_diff = guess['latitude'] - answer['latitude']
        if abs(lat_diff) < 5:
            lat_close = guess['latitude']
        elif lat_diff > 0:
            # 猜测纬度 > 答案纬度，答案在南边，猜测纬度是上界
            if lat_max is None or guess['latitude'] < lat_max:
                lat_max = guess['latitude']
        else:
            # 猜测纬度 < 答案纬度，答案在北边，猜测纬度是下界
            if lat_min is None or guess['latitude'] > lat_min:
                lat_min = guess['latitude']
        
        # 人口范围推断
        pop_ratio = guess['population'] / answer['population']
        if abs(pop_ratio - 1) < 0.2:
            pop_close = guess['population']
        elif pop_ratio > 1:
            # 猜测人口 > 答案人口，猜测人口是上界
            if pop_max is None or guess['population'] < pop_max:
                pop_max = guess['population']
        else:
            # 猜测人口 < 答案人口，猜测人口是下界
            if pop_min is None or guess['population'] > pop_min:
                pop_min = guess['population']
        
        # 面积范围推断
        area_ratio = guess['area'] / answer['area']
        if abs(area_ratio - 1) < 0.2:
            area_close = guess['area']
        elif area_ratio > 1:
            # 猜测面积 > 答案面积，猜测面积是上界
            if area_max is None or guess['area'] < area_max:
                area_max = guess['area']
        else:
            # 猜测面积 < 答案面积，猜测面积是下界
            if area_min is None or guess['area'] > area_min:
                area_min = guess['area']
        
        # GDP排名范围推断
        gdp_diff = guess['gdp_rank'] - answer['gdp_rank']
        if abs(gdp_diff) < 5:
            gdp_close = guess['gdp_rank']
        elif gdp_diff > 0:
            # 猜测排名 > 答案排名（猜测排名更差），猜测排名是上界
            if gdp_max is None or guess['gdp_rank'] < gdp_max:
                gdp_max = guess['gdp_rank']
        else:
            # 猜测排名 < 答案排名（猜测排名更好），猜测排名是下界
            if gdp_min is None or guess['gdp_rank'] > gdp_min:
                gdp_min = guess['gdp_rank']
    
    # 辅助函数：格式化经度
    def format_lon(value):
        prefix = "东经" if value >= 0 else "西经"
        return f"{prefix}{abs(value)}°"
    
    # 辅助函数：格式化纬度
    def format_lat(value):
        prefix = "北纬" if value >= 0 else "南纬"
        return f"{prefix}{abs(value)}°"
    
    # 经度范围
    if lon_close is not None:
        summary.append({"type": "text", "content": f"经度：接近{format_lon(lon_close)}"})
    elif lon_min is not None or lon_max is not None:
        if lon_min is not None and lon_max is not None:
            summary.append({"type": "text", "content": f"经度：{format_lon(lon_min)} - {format_lon(lon_max)}"})
        elif lon_min is not None:
            summary.append({"type": "text", "content": f"经度：{format_lon(lon_min)} -"})
        elif lon_max is not None:
            summary.append({"type": "text", "content": f"经度：- {format_lon(lon_max)}"})
    
    # 纬度范围
    if lat_close is not None:
        summary.append({"type": "text", "content": f"纬度：接近{format_lat(lat_close)}"})
    elif lat_min is not None or lat_max is not None:
        if lat_min is not None and lat_max is not None:
            summary.append({"type": "text", "content": f"纬度：{format_lat(lat_min)} - {format_lat(lat_max)}"})
        elif lat_min is not None:
            summary.append({"type": "text", "content": f"纬度：{format_lat(lat_min)} -"})
        elif lat_max is not None:
            summary.append({"type": "text", "content": f"纬度：- {format_lat(lat_max)}"})
    
    # 人口范围
    if pop_close is not None:
        summary.append({"type": "text", "content": f"人口：接近{pop_close}亿"})
    elif pop_min is not None or pop_max is not None:
        if pop_min is not None and pop_max is not None:
            summary.append({"type": "text", "content": f"人口：{pop_min}亿 - {pop_max}亿"})
        elif pop_min is not None:
            summary.append({"type": "text", "content": f"人口：{pop_min}亿 -"})
        elif pop_max is not None:
            summary.append({"type": "text", "content": f"人口：- {pop_max}亿"})
    
    # 面积范围
    if area_close is not None:
        summary.append({"type": "text", "content": f"面积：接近{area_close}万km²"})
    elif area_min is not None or area_max is not None:
        if area_min is not None and area_max is not None:
            summary.append({"type": "text", "content": f"面积：{area_min}万km² - {area_max}万km²"})
        elif area_min is not None:
            summary.append({"type": "text", "content": f"面积：{area_min}万km² -"})
        elif area_max is not None:
            summary.append({"type": "text", "content": f"面积：- {area_max}万km²"})
    
    # GDP排名范围
    if gdp_close is not None:
        summary.append({"type": "text", "content": f"GDP排名：接近第{gdp_close}名"})
    elif gdp_min is not None or gdp_max is not None:
        if gdp_min is not None and gdp_max is not None:
            summary.append({"type": "text", "content": f"GDP排名：第{gdp_min}名 - 第{gdp_max}名"})
        elif gdp_min is not None:
            summary.append({"type": "text", "content": f"GDP排名：第{gdp_min}名 -"})
        elif gdp_max is not None:
            summary.append({"type": "text", "content": f"GDP排名：- 第{gdp_max}名"})
    
    return summary
