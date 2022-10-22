
# is-github-page

判断网站是否托管于Github-Pages (数据源于timqian/chinese-independent-blogs)

- main.py 用于从 timqian/chinese-independent-blogs 批量自动判断网站是否为 GH-Pages
- sigle-check.py 手动输入域名/链接来判断网站是否为 GH-Pages
- gh-pages-check.py
    - 使用 `dnspython` 库完成 DNS 查询
    - 遍历查询域名的 `A`, `CNAME`, `AAAA` 记录, 任一查询结果符合 GitHub Pages 特征则返回结果
    - 支持通过命令行选项设置 nameservers
    - 可使用 `--urls` 选项直接输入 URL 查询
    - 可使用 `--csv` 读取远程或本地的 `.csv` 文件查询, `.csv` 文件格式需要与 [blogs-original.csv](https://raw.githubusercontent.com/timqian/chinese-independent-blogs/master/blogs-original.csv) 一致
    - 可使用 `--output` 选项可将查询结果写入文件
    - 使用 `--help` 选项查看脚本帮助信息

输出结果：gh-domains.txt

- main分支的脚本，采用DNS解析到的IP来简易判断是不是Github采用的IP范围。Github有提供[CIDR格式的IP列表](https://docs.github.com/cn/authentication/keeping-your-account-and-data-secure/about-githubs-ip-addresses)，我懒得转换CIDR，直接取IP的前3位和Github的CIDR格式的IP列表直接字符串匹配，所以脚本会有很小很小很小的概率出现判断错误（把不是Github的IP当成是Github的IP）。但实际跑了几百个域名，没有发现这样的情况。
- header分支的脚本，根据http请求回传的header中是否有`Server: Github.com`字段来判断是不是Github托管的网站，判断几乎不可能出错，但是脚本跑得慢（比IP方法慢4倍，毕竟要握手）。
