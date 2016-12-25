# Web Scripts

一些实用的JavaScript代码

### 快速评教

在评教页面执行，对所有指标选中非常满意

```JavaScript
// 编辑总体评价
document.querySelector('select').value = '很好';
// 全选优秀
document.querySelectorAll('input[type="radio"]').forEach(item => item.value === "100" && item.click());
// 随机一个良好
(function() {this[Math.ceil(this.length * Math.random())].click()}).call(Array.from(document.querySelectorAll('input[type="radio"]')).filter(item => item.value === "80"));
// 检查结果
document.querySelector('input[type="submit"]').click()
```
