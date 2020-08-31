# HAUT_autoCheck

------

**河南工业大学完美校园健康打卡**
* 随机温度(36.2℃-36.8℃)🌡
* 每天定时打卡（默认早上7点）⏱
* 微信通知打卡结果(可选)💬
* 基于Github Actions，完全解放你的设备的服务器。✔

## 使用方法 
1. [Fork](https://github.com/YooKing/HAUT_autoCheck/fork)此项目  
2. 进入你的 fork 的仓库，`Settings → Secrets`,  
![](/img/secret.png)
按下面表格添加12个 Secret（利用secret解决隐私问题）：  

<div align=center>

| Secrets| 内容 |
| :----:| :----: |
|DEPTID|手机抓包所得|
|TEXT|学院-专业-班级`探月工程学院-种土豆专业-种豆2020`
|EMERGENCY|紧急联系人手机号|x
|PHONENUM|个人手机号|
|USERNAME|个人姓名|
|STUNUM|学号|
|USERID|手机抓包所得|
|DORMNUM|宿舍门牌号|
|HOMETOWN|籍贯|
|PERSONNUM|身份证号|
|HOME|详细住址 `xx路xx号xx小区`|
|LOCAL|如`河南省-郑州市-中牟县`尽量有连字符
</div>  

3. 进一步打开`main.py`找到`sex = "男"`更改性别

4. 创建ACtions  
自行百度

5. 修改时间  
打开本项目 `workflows/clock.yml` 文件，找到   
```
    schedule:
    - cron: 0 23 * * * 
```  
此时间为国际时间，+8 可推算出北京时间07点，表示每天早上7点运行一次，建议只修改`23`其余不动，要留有空格。  

6. 检查结果  
下图中`run`为服务器反馈结果
![](/img/result.png)  

## 额外功能
* [微信通知](https://github.com/YooKing/HAUT_autoCheck/wiki#wechat)  
微信推送每次打卡结果。
![](/img/wechat.jpg)
🌞每天醒来一条推送，多么惬意！  
* 想到什么添加什么...

## 许可

本项目以 MIT 协议开源，详情请见 [LICENSE](LICENSE) 文件。
