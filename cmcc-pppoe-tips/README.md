# 获得移动宽带用户名和密码

### 获得移动拨号用户名
从源中安装 `uuidgen`，比如：
```
opkg update && opkg install uuidgen
```
然后编辑第五行，填入自己的手机号，执行脚本，输出的内容即为可以使用的 PPPoE 帐号。

### 获得移动拨号动态密码
在拨号之前，直接访问（填入你的手机号）：
```
http://112.21.188.162:808/sms?server=1&newuser=0&phone=<YourPhoneNumber>
```
密码短信就将发送到你的手机。