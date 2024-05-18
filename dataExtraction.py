'''
Author: HDJ
StartDate: 2024-05-15 00:00:00
LastEditTime: 2024-05-18 23:11:13
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\jd-data-exporter\dataExtraction.py
Description: 

				*		写字楼里写字间，写字间里程序员；
				*		程序人员写程序，又拿程序换酒钱。
				*		酒醒只在网上坐，酒醉还来网下眠；
				*		酒醉酒醒日复日，网上网下年复年。
				*		但愿老死电脑间，不愿鞠躬老板前；
				*		奔驰宝马贵者趣，公交自行程序员。
				*		别人笑我忒疯癫，我笑自己命太贱；
				*		不见满街漂亮妹，哪个归得程序员？    
Copyright (c) 2024 by HDJ, All Rights Reserved. 
'''
import re
import json
import parsel



with open('config.json', 'r', encoding='utf-8') as jsf:
    config = json.load(jsf)



def data_extraction(page_html_src):
    """ 
    数据提取 

    Args: 
        page_html_src (str): 一个网页完整的html源代码
    Returns: 
        list: 返回一个数据表，使用二维列表储存
    """
    result = parsel.Selector(html)
    # 找到合适的外层框架
    table = result.xpath('//table[@class="td-void order-tb"]')
    # 根据需求--筛掉合并订单，该类订单无具体商品信息
    tbodys = table.xpath('.//tbody[not(contains(@id, "parent"))]') 
    form = []   # 表数据
    for tbody in tbodys:
        row = []    # 行数据，一行存一个订单全部数据 
        for header in config['headers']:
            try: 
                row.append(func_dict.get(header)(tbody))
            except TypeError:
                row.append('暂无')
        form.append(row)
    return form        
        

def get_order_id(RP_element: parsel.Selector):
    """ 
    Args:
        RP_element (parsel.Selector): relative_parent_element
    """
    # 获取订单编号
    order_id = RP_element.xpath('.//tr/td/span[@class="number"]/a/text()').get('')
    return order_id

def get_product_name(RP_element):
    # 获取商品名称
    product_name = RP_element.xpath('.//tr[@class="tr-bd"]/td/div/div/div/a/text()').get('').strip()
    return product_name

def get_goods_number(RP_element):
    # 商品数量
    goods_number = RP_element.xpath('.//tr/td/div[@class="goods-number"]/text()').get('').strip().strip('x')
    return goods_number

def get_amount(RP_element):
    # 实付款
    amount = RP_element.xpath('.//tr/td/div[@class="amount"]/span[1]/text()').get('')
    return amount

def get_order_time(RP_element):
    # 下单时间
    order_time = RP_element.xpath('.//tr/td/span[@class="dealtime"]/text()').get('')
    return order_time

def get_order_status(RP_element):
    # 获取订单状态
    order_status = RP_element.xpath('.//tr/td/div[@class="status"]/span/text()').get('').strip()
    return order_status

def get_consignee_name(RP_element):
    # 收件人
    consignee_name = RP_element.xpath('.//tr/td/div/div/div/strong/text()').get('')
    # 进行脱敏
    if len(consignee_name) == 2:
        return consignee_name[0] + "*"
    elif len(consignee_name) > 2:
        return consignee_name[0] + "*" * (len(consignee_name) - 2) + consignee_name[-1]
    return consignee_name

def get_consignee_address(RP_element):
    # 收货地址
    consignee_address = RP_element.xpath('.//tr/td/div/div/div/p[1]/text()').get('')
    # 进行脱敏
    return re.sub(r'\d+', '****', consignee_address)

def get_consignee_phone_number(RP_element):
    # 联系方式
    consignee_phone_number =RP_element.xpath('.//tr/td/div/div/div/p[2]/text()').get('')
    # 进行脱敏
    if len(consignee_phone_number) == 11:  # 适用于中国大陆手机号码
        return consignee_phone_number[:3] + "****" + consignee_phone_number[7:]
    return consignee_phone_number

    
func_dict = {
    "order_id": get_order_id,
    "product_name": get_product_name,
    "goods_number": get_goods_number,
    "amount": get_amount,
    "order_time": get_order_time, 
    "order_status": get_order_status,
    "consignee_name": get_consignee_name,
    "consignee_address": get_consignee_address,
    "consignee_phone_number": get_consignee_phone_number
}
    

if __name__ == "__main__":
    with open('p1.html', 'r', encoding='utf-8') as f:
        html = f.read()
    print(data_extraction(html))