import random
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

def get_weather(city):
    try:
        # 故意制造一个可能出错的地方（比如字典取值、变量名错误）
        weather_types2 = ["晴", "多云", "阴", "小雨", "中雨", "雷阵雨"]
        weather = random.choice(weather_types)
        temperature = random.randint(5, 35)
        # 假设下面这行代码可能引发 KeyError（比如从空字典取值）
        # 这里用城市名模拟一个可能不存在的键
        dummy = {"city": city}
        result = dummy["city"]   # 这行不会出错，只是演示
        logging.info(f"{city}天气：{weather}，温度：{temperature}℃")
        return {"city": city, "weather": weather, "temp": temperature}
    except NameError as e:
        logging.error(f"代码错误：变量 {e} 未定义")
    except KeyError as e:
        logging.error(f"数据错误：找不到键 {e}")
    except Exception as e:
        logging.error(f"未知错误：{e}")

if __name__ == "__main__":
    city = input("请输入城市名：")
    get_weather(city)