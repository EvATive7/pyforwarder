# PyForwarder
一个基于Flask的反代服务器，使用指定的代理服务器发起代理请求。

## 使用
1. `git clone`
1. 调整`Data/Config`中的配置文件。
1. 调整你的反代服务器配置，设定域名，将反向代理的目标服务器指向本服务，启用请求头传递，且请求头的Host字段务必传递原始请求头中的Host字段。  
    一个在nginx中可行的配置例子：
    ``` nginx
    server {
        listen listeningPort;
        server_name *.your.domain;
        
        location / {
            proxy_pass_request_headers on;
            proxy_set_header Host $host;
            proxy_pass http://ip:port;
        }
    }
    ```
    其中，`listeningPort`为nginx server监听的端口，如果你启用了HTTPS，那么为443，否则为80；`*.your.domain`为你要匹配的域名；`ip`为本服务的ip地址；`port`为本服务的端口。
1. 配置域名解析服务，将你在上面配置的域名解析到ip。
1. `python main.py`

## 注意
- 配置文件支持热加载，这意味着当你想更改某些字段时，可以直接修改而无需重启本服务。热加载的生效时间单位为每次字段访问。
- 在Windows中，可以通过修改hosts来将自定义域名指向localhost。这可能利于开发。

## 目标
- springboot重构 for 性能优化
