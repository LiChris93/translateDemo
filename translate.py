import requests
import random
from hashlib import md5
from urllib import parse
import json

appID = "appID"  # appID,请设置成自己的
apiKey = "apikey"  # apikey,请设置成自己的


def translate(query, to, source="auto", action=0):
    """_summary_

    Args:
        query (String): 要翻译的内容
        to (String): 目标语言(zh,en,jp,fra.....)(具体请参考readme)
        source (str, optional): 来源语言. Defaults to "auto".(具体请参考readme)
        action (int, optional): 是否用术语库干预翻译结果(是为1,否为0,需使用高级版及以上的api). Defaults to 0.

    Returns:
        String: 翻译结果或错误详情
    """
    if (
        not isinstance(query, str)
        or not isinstance(to, str)
        or not isinstance(source, str)
    ):  # 参数错误
        return "error,illegal argument"

    salt = random.randint(0, 100000)  # 随机salt值
    sign = md5((appID + query + str(salt) + apiKey).encode()).hexdigest()  # MD5签名
    data = requests.get(
        f"https://fanyi-api.baidu.com/api/trans/vip/translate?q={parse.quote(query)}&from={source}&to={to}&appid={appID}&salt={salt}&sign={sign}&action={action}"
    ).text  # 请求api
    decoded_data = json.loads(data)  # json->list

    if "error_code" in decoded_data.keys():  # 返回结果里有错误,返回错误详细信息
        return f"error,code={decoded_data['error_code']},msg=\"{decoded_data['error_msg']}\""

    result = ""
    for i in decoded_data["trans_result"]:  # 逐行记录翻译结果
        result += i["dst"]
        result += "\n"
    return result  # 返回结果


def main():
    try:
        print(translate(input("要翻译的内容:"), input("目标语言:")))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
