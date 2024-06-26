'''
Author: HDJ
StartDate: 2024-05-15 00:00:00
LastEditTime: 2024-06-17 00:39:19
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\jd-pers-data-exporter\src\dataExporter.py
Description: 

                *       写字楼里写字间，写字间里程序员；
                *       程序人员写程序，又拿程序换酒钱。
                *       酒醒只在网上坐，酒醉还来网下眠；
                *       酒醉酒醒日复日，网上网下年复年。
                *       但愿老死电脑间，不愿鞠躬老板前；
                *       奔驰宝马贵者趣，公交自行程序员。
                *       别人笑我忒疯癫，我笑自己命太贱；
                *       不见满街漂亮妹，哪个归得程序员？    
Copyright (c) 2024 by HDJ, All Rights Reserved. 
'''

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .orderListCapture import JDOrderListCapture
from .orderDetailsCapture import JDOrderDetailsCapture
from .dataPortector import ConfigManager
from .data_type.Form import Form


class JDDataExporter:
    def __init__(self):
        # 日志记录器
        self.logger = logging.getLogger(__name__)
        
        self.__configManager = ConfigManager()
        self.__config = self.__configManager.get_config() # 获取配置文件
        self.__date_range_dict = self.__configManager.get_date_range_dict() # 获取日期范围字典
        self.__chrome_options = webdriver.ChromeOptions()
        self.__chrome_options.add_argument('--start-maximized')  # 最大化浏览器
        self.__chrome_options.add_argument('--disable-infobars')  # 禁用信息栏
        self.__driver = webdriver.Chrome(options=self.__chrome_options)

        self.__need_details = False

    def wait_for_loading(self) -> bool:
        """等待用户登录"""
        try:
            element = WebDriverWait(self.__driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_user"]/div/div[1]/div/p[1]/a')))
            if self.__config.get('user_name') and element.text == self.__config.get('user_name'):
                # 条件满足时，跳出循环
                self.logger.info("登录成功")
                return True
            else:
                self.logger.warning("用户名不匹配，登录失败")
        except TimeoutException:
            self.logger.error("登录超时，请重试！")
        self.__close()
        return False

    def wait_for_element(self, duration, attribute, value, err_text):
        """
        等待页面元素出现，并返回该元素对象。

        Args:
            duration (int): 最长等待时间（秒）。
            attribute (str): 元素属性，如 'id'、'class name'、'xpath' 等。
            value (str): 元素属性值，用于定位元素。
            err_text (str): 错误提示文本。 

        Returns:
            element: 如果元素出现，则返回该元素对象；否则返回 None。
        """
        try:
            # 使用WebDriverWait等待元素出现
            element = WebDriverWait(self.__driver, duration).until(EC.presence_of_element_located((attribute, value)))
            if element:
                return element
        except TimeoutException:
            if err_text:
                self.logger.error(f'超时: {err_text}')
            else:
                self.logger.error("超时未找到组件，请重试！")
        return None

    def get_d_values(self):
        """ 生成目标url的d值的列表 """
        d_values = [self.__date_range_dict.get(quantum) for quantum in self.__config['date_range'] if self.__date_range_dict.get(quantum)]
        d_values = list(set(d_values))
        
        if -1 in d_values:
            d_values = [value for value in self.__date_range_dict.values() if value not in [-1, 1]]
        if not d_values:
            d_values.append(1)  # 默认d值仅有1
            
        d_values.sort()
        return d_values

    def fetch_data(self):
        """ 从网页获取所需数据 """
        orderDetailsCapture = JDOrderDetailsCapture()
        # 判断是否需要进一步获取
        self.__need_details = any(header in orderDetailsCapture.header_owned for header in self.__config['header'])
        form = Form()
        url_login = "https://passport.jd.com/new/login.aspx"
        self.__driver.get(url_login)
        if self.wait_for_loading():
            for d in self.get_d_values():
                page = 1
                while True:
                    target_url = f"https://order.jd.com/center/list.action?d={d}&s=4096&page={page}"
                    self.__driver.get(target_url)
                    self.wait_for_element(3, By.XPATH, '//*[@id="order02"]/div[2]/table', '表单未出现！')  # 等待表单出现
                    # 获取结束标志
                    finish_tip = self.wait_for_element(2, By.XPATH, '//*[@id="order02"]/div[2]/div[2]/div/h5', '结束标志未出现！')
                    if finish_tip:
                        self.logger.info("当前时段数据获取结束！")
                        break
                    # time.sleep(2)
                    orderListCapture = JDOrderListCapture(self.__driver.page_source)
                    level_1_data = orderListCapture.filter_data(orderListCapture.extract_data()) # 订单列表中一页订单的数据
                    new_form = Form() # 用来储存一页订单数据
                
                    if self.__need_details:
                        # 进一步获取数据
                        for order_data in level_1_data:
                            order_url = order_data.get('order_url', '')
                            if order_url:
                                orderDetailsCapture = JDOrderDetailsCapture(order_url, self.__driver)
                                level_2_data = orderDetailsCapture.extract_data() # 一个订单更详细的数据
                                new_order_data = {**order_data, **level_2_data} # 将两次获取到的数据整合到一起
                                new_form.append(new_order_data)
                    else:
                        new_form = level_1_data
                    form += new_form  # 将新的一页数据添加到from
                    self.logger.info(f"------------d{d}-page{page}结束---------------")
                    page += 1
                self.logger.info(f"------------d{d}结束---------------")
        self.__close()
        return form

    def __close(self):
        time.sleep(1)
        self.__driver.quit()

    def run(self, export_mode: str | None = None):
        mode = self.__config.get('export_mode') # 不传参使用配置文件
        if export_mode: 
            mode = export_mode
        form = self.fetch_data()
        try:
            if form:
                if mode == 'excel':
                    form.save_to_excel(self.__config['header'], f'{self.__config.get('user_name', '')}_JD_order.xlsx')
                elif mode == 'mysql':
                    form.save_to_mysql(self.__config['header'], f'{self.__config.get('user_name', '')}_JD_order')            
        except Exception as err:
            self.logger.error(f'run error: {err}')

