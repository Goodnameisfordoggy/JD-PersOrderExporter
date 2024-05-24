# 项目简介

## 宇宙安全声名
1. 本仓库发布的`JD_PersDataExporter`项目中涉及的任何脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。

2. 本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。

3. `Goodnameisfordoggy | huo dong jun | HDJ` 对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害.

4. 间接使用脚本的任何用户，包括但不限于建立VPS或在某些行为违反国家/地区法律或相关法规的情况下进行传播, `Goodnameisfordoggy | huo dong jun | HDJ`对于由此引起的任何隐私泄漏或其他后果概不负责。

5. 请勿将`JD_PersDataExporter`项目的任何内容用于商业或非法目的，否则后果自负。

6. 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关脚本。

7. 以任何方式查看此项目的人或直接或间接使用`JD_PersDataExporter`项目的任何脚本的使用者都应仔细阅读此声明。`Goodnameisfordoggy | huo dong jun | HDJ` 保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或`JD_PersDataExporter`项目，则视为您已接受此免责声明。

8. 您必须在下载后的24小时内从设备中完全删除以上内容。

9. 本项目遵循Apache-2.0 License协议，如果本特别声明与Apache-2.0 License协议有冲突之处，以本特别声明为准。

## 功能说明
- 该项目是一个本地自动化工具，用于导出京东个人账户的订单信息。


## 使用说明
下载解压项目压缩包后按照以下说明进行
1. 使用前配置：
    - 打开config.json（配置文件）
    - 在`"user_name"`后的`""`内填充完整的账号名。该账号名仅用于登录成功验证。
    - 在`"date_range"`后的`[]`内写入要获取的订单的时间分组。必须写入完整的选项字段！若不设置则默认获取最近三个月订单信息。\
    示例：`["ALL"]`将获取账号内全部订单信息；`["2022年订单", "2023年订单", "2016年订单"]`将获取2023年，2022年，2016年这三年的全部订单信息。
  
        |时间分组可选项(与我的订单页面一致)|
        |---|
        |ALL (新增)
        |近三个月订单
        |今年内订单
        |2023年订单
        |2022年订单
        |2021年订单
        |2020年订单
        |2019年订单
        |2018年订单
        |2017年订单
        |2016年订单
        |2015年订单
        |2014年订单
        |2023年订单
        |2014年以前订单
- 在`"header"`后的`[]`中设置需要获取订单的信息类型。默认为全部获取。将用于Excel文件的表头生成。\
  示例：`["product_name", "order_id", "amount"]`生成的Excel文件第一列信息为商品名称，第二列信息为订单号，第三列信息为总金额(实付)。

    |可选项|信息类型|
    |---|---|
    order_id|订单号
    product_name|商品名称
    goods_number|商品数量
    amount|总金额(实付)
    order_time|下单时间
    order_status|订单状态
    consignee_name|收件人姓名(进行轻度脱敏)
    consignee_address|收货地址(进行轻度脱敏)
    consignee_phone_number|收件人联系方式(该信息源已脱敏)
- `"filter_config"`的子项中可以选择筛选订单的类型，最后会影响输出结果。
  示例：若`"去除券(包)类订单"`设置为`true`,那么输出的订单中将不包含券(包)类订单。\
  此外，还设置了通过关键词自定义筛选，其中`"header_item"`的值只能为已有的header_item的名称；`"keyword"`填入要筛选的一个或多个关键词。\
  示例：若`"header_item"`值为`"product_name"`，`"keyword"`值为`["小米", "泡腾片"]`那么最后只会保留商品名称中存在“小米”或“泡腾片”的订单。

- "`header_items"`的值目前不建议更改。
1. 启动工具并使用
- 双击运行exe文件，等待浏览器跳转到登录界面。
- 登录你的京东账号，建议使用扫码登录(方便快捷)，其他方式也行。
- 部分账号有概率会出现二次安全验证。如：图形验证，滑块验证，手机号验证码再次登录验证，身份证前几位和后几位验证等。(再次声明，所有信息均在本地使用和处理，请放心通过安全验证)
- 等待程序执行，期间不要关闭浏览器窗口(可以最小化)；程序结束会自动关闭终端窗口，此时在exe文件所在目录可以找到包含订单信息的Excel文件。
## 环境与依赖
- python版本: 3.12.0
- Chrome, 与Chrome对应版本的chromedriver
- 部分包为较新版本,但不代表低版本不可用.
  
    |包名|版本|
    |:---:|:---:|
    parsel|1.9.1
    selenium|4.21.0
    openpyxl|3.1.2
    pandas|2.2.2
  
# Update log
- 1.2.3: 将部分类属性私有化；修复了自定义筛选订单类型功能，在部分情况下的异常。
- 1.2.2：将项目按照面向对象规则重组，并使用包结构管理源码。
- 1.1.2: 优化了数据筛选方法。减少了数据迭代次数，提升了性能。
- 1.1.1：新增了订单类型筛选功能。
- 1.0.1: 优化了商品名称，商品数量获取方法。考虑了一个订单号下有多个同店铺商品未进行订单拆分的情况。