# install_webdav_openwrt

* 主要改动：
移除 --tls false 参数：直接使用默认的非加密模式（HTTP）来启动 WebDAV 服务。
执行步骤：
上传并执行脚本：

* 上传并运行：
``bash
复制代码
``python3 script_name.py
访问 WebDAV 服务：

在浏览器或 WebDAV 客户端中访问 WebDAV 服务：
arduino
复制代码
http://<OpenWrt_IP>:8867
