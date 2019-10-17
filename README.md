# Scrapy 专利详情爬虫
>## 思路
>在得到一个url时，scrapy会使用代理，在解析完成后会
>返回response；在这个过程可能会由于代理的原因造成异常，出现异常则再进行
>相关处理。
>当得到一个可用的response之后，会尝试抽取信息，并保存页面结果，之后保存到mongo数据库中。
>## spider
>detail 爬虫：负责爬取详情页
>## middleware
>1. GetFromLocalityMiddleware 用于从本地获取文件，如果获取成功，则直接从本地获取(之后可检测mongo数据库)
>2. RetryOrErrorMiddleware 重写官方示例，添加一个报错日志
>3. ProxyMiddleware 添加了代理
>## pipeline
>1. SavePagePipeline 保存到本地文件
>2. FilterPipeline 把得到的item的格式改为正确的格式
>3. MongoPipeline 保存到mongo数据库中
>## 关于思路
>### 1.代理     
>当splash通过代理访问页面失败时由scrapy处理(scrapy middleware) 代理通过scrapy传递给splash
>每隔一段时间，就会遍历files/page_links下的所有文件夹，然后
>查看每个文件是否已经访问，如果不是，则传递给scrapy，开启并运行。
>### 2.重试
> 每个请求都会重试若干次以上（有的免费代理不可用），同时会在最后一次不再使用代理
>如果这一次仍然失败，则把此次链接记录下来。
>### 3.数据清洗
>数据保存到mongo中，同时，注意保证公开号的唯一
>目前有两个数据类型为数组：发明人和专利分类号(源数据用分号隔开)
>注：发明人 专利分类号 中间用分号隔开 就算只有一个也是用数组

>
>要有两个线程，线程之间相互合作，生产者就是run.py 消费者则是scrapy，它们共同管理
>着一个队列，run.py负责读取文件，并把数据放入队列中；而scrapy则负责从队列中提取数据
>
>category_code 根据文件夹可以得知
>是放在服务器上跑，还是跑完了一大类后再进行。。。
>有的专利页面没有专利代理机构和代理人
>### 数据提取
>可以按照tr[style!='display:none']提取每一行，接着xpath('./td').extract()提取出
>该行所有的td
>```
>for td in tds:
>   if td.text() in self.mapping():
>       key = self.mappings()
>       value = td.next()
>       item[key] = value
>```
