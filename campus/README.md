# wanmei_campus

完美校园模拟登录控件

```python3
from campus import open_device, CampusCard

if __name__ == '__main__':
    campus = CampusCard("完美校园账号", "完美校园密码", open_device('userinfo.txt'))
    print(campus.get_main_info())
```
