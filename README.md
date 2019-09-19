# 专利爬虫
## 1. scrapy
异步爬虫框架
## 2. Splash
轻量级的web浏览器

> Scrapy负责构造请求，之后请求交给Splash（可以是远程服务器）进行解析，
> Splash会根据对应的lua脚本来解析请求后并返回字符串给scrapy，之后则交给
> scrapy
>针对知网专利，
### splash笔记
> 1. splash如何显示等待页面的加载
> 2. splash主要通过splash:evaljs(js代码)来获取到页面信息
> 3. splash:wait()可以异步等待若干秒,即会做其他的任务，之后再继续执行。
> 4. render.html render.png render.jpeg render.har render.json 包含着大量通用
> 的功能，但是仅仅这样还是不太够的，这时候可以使用execute run。
> splash使用的是lua，详情:[splash lua](https://splash.readthedocs.io/en/stable/scripting-overview.html)
