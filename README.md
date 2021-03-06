# Scrapy 专利详情爬虫
>在得到一个url时，scrapy会首先把它发送给splash，之后splash（代理）在解析完成后会
>返回response；在这个过程可能会由于代理的原因造成异常，目前不知道这个异常是由splash
>处理还是由scrapy处理。
>当得到一个可用的response之后，会尝试抽取信息，并保存页面结果。
## 需要解决的问题
> 1. ~~代理的设置~~
> 3. splash请求问题
> 4. 在页面有效的情况下会同时保存页面 （Item pipeline中进行）
> 5. 爬取专利页面 在redis中创建一个唯一的
> 6. 请求失败问题。
> 7. scrapy的日志
> 8. 数据清洗问题
>### 1.代理
>当splash通过代理访问页面失败时由scrapy处理(scrapy middleware) 代理通过scrapy传递给splash
>每隔一段时间，就会遍历files/page_links下的所有文件夹，然后
>查看每个文件是否已经访问，如果不是，则传递给scrapy，开启并运行。
>### 2.splash请求问题
>splash并不解析页面的结构，当出现验证码时需要换个代理重新请求
>### 3.重试
> 每个请求都会重试若干次以上（有的免费代理不可用），同时会在最后一次不再使用代理
>如果这一次仍然失败，则把此次链接记录下来。
>### 4.数据清洗
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
>(```)
>for td in tds:
>   if td.text() in self.mapping():
>       key = self.mappings()
>       value = td.next()
>       item[key] = value
>(```)
>在访问一个json文件中的url的中间突然中断的时候，会造成剩下的链接无法再次获取。
>计划添加一个全局的计数器，只有在写入到mongo后才会真正的写入到redis中。
>为节省服务器的压力，可以从已经有的文件中直接读取文件
>使用脚本每隔一段时间运行scrapy，但是在运行前会检测这个项目已经在运行，
>如果有了则不执行。
>
### splash笔记
> 1. splash如何显示等待页面的加载
> 2. splash主要通过splash:evaljs(js代码)来获取到页面信息
> 3. splash:wait()可以异步等待若干秒,即会做其他的任务，之后再继续执行。
> 4. render.html render.png render.jpeg render.har render.json 包含着大量通用
> 的功能，但是仅仅这样还是不太够的，这时候可以使用execute run。
> splash使用的是lua，详情:[splash lua](https://splash.readthedocs.io/en/stable/scripting-overview.html)
