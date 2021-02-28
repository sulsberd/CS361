    json_string=response.json()

    symbols = ['国家', '省份', '城市', '区域', '运营商']
    print("****************************************")
    counter = 0
    for symbol in symbols:
        print(symbol + ' ' + str.format(json_string[counter]))
        counter += 1
    print("数据来源<www.ipip.net免费查询接口>")
    print("****************************************")