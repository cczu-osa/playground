#Web Scripts

一些实用的JavaScript代码

### 快速评教
在评教页面执行，对所有指标选中非常满意
```JavaScript
document.querySelectorAll('input[type="radio"]').forEach(item => item.value === "100" && item.click())
```
