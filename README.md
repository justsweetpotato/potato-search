# search-book-heroku
土豆图书搜索引擎<br>
##### 使用谷歌自定义搜索, 返回图书的搜索结果. <br>
因为谷歌提供的网页嵌入代码在中国大陆无法使用, 所以使用 Django 框架获取用户输入, 将用户输入的内容构造成 请求URL 向谷歌 API 进行请求, 拿到结果后进行提取
再把提取后的内容写入 模板 交由 视图 返回前端页面. <br>
<a href="https://search-books.herokuapp.com/">土豆图书搜索</a><br>
<small>*heroku 的应用托管服务半小时内无连接请求会进入休眠状态, 第一次访问较慢是正常现象, 请稍等, 之后不会有这个问题.</small>


![搜索引擎](https://raw.githubusercontent.com/justsweetpotato/makedown-img-store/master/search/10.png)
![搜索结果](https://raw.githubusercontent.com/justsweetpotato/makedown-img-store/master/search/11.png)



### 版本更新
v2.1<br>
新增一个apikey使每日请求配额达到200, 新增了一个api配额用尽时的提示, 新增了404页面与500页面. 解决了搜索一串乱码时, 服务器返回403的错误(现在会显示未搜索到内容).<br>
已知问题: 分页问题, 目前只显示1页10条结果.

v2.0正式版<br>
在 青空锁云 的帮助下完成了提取部分, 调用谷歌 api 返回数据提取后填充到网页中, 解决了中国大陆无法访问的问题!

v1.1<br>
增加了随机显示名人名言 优化了页面排版.<br>
已知问题: 中国大陆无法使用.

v1.0<br>
基础引擎框架<br>
已知问题: 谷歌 js 在中国大陆无法加载, 反向代理无法解决.<br>


