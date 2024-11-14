import requests
import os
import tarfile
import time
import subprocess
from tqdm import tqdm

def download_and_manage_file(url, initial_destination, extract_dir, webdav_path, shared_dir):
    """
    下载 WebDAV 执行文件、解压并启动 WebDAV 服务
    
    Args:
    url (str): WebDAV 文件的下载链接
    initial_destination (str): 下载保存路径
    extract_dir (str): 解压到的目标目录
    webdav_path (str): WebDAV 执行文件路径
    shared_dir (str): 共享目录路径
    """
    try:
        # 发送 GET 请求下载文件
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
        total_size = int(response.headers.get('content-length', 0))

        # 下载文件并显示进度条
        with open(initial_destination, 'wb') as file, tqdm(
                desc="Downloading",
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                progress_bar.update(len(data))

        print("下载完成！")
        time.sleep(2)  # 等待 2 秒

        # 创建目标目录
        os.makedirs(extract_dir, exist_ok=True)

        # 解压文件到目标目录
        try:
            with tarfile.open(initial_destination, 'r:gz') as tar:
                tar.extractall(extract_dir)  # 解压到指定目录
            print(f"解压成功，文件已存放在: {extract_dir}")
        except (tarfile.TarError, EOFError) as e:
            print("文件不是有效的 .tar.gz 格式，无法解压。错误信息：", e)

        # 设置 WebDAV 执行文件权限
        os.chmod(webdav_path, 0o755)  # 给予执行权限
        print(f"已设置 {webdav_path} 为可执行文件。")

        # 创建共享目录
        os.makedirs(shared_dir, exist_ok=True)
        print(f"共享目录 {shared_dir} 已创建。")

        # 启动 WebDAV 服务
        subprocess.Popen([webdav_path, '-a', '0.0.0.0', '-p', '8867', '-P', '/'])  # 启动 WebDAV 服务
        print(f"WebDAV 服务已启动，监听在端口 8867，共享目录: {shared_dir}。")

    except requests.HTTPError as http_err:
        print(f"HTTP 错误发生: {http_err}")
    except Exception as e:
        print("下载或处理失败，错误信息：", e)

# 定义 URL 和路径
url = "https://github.com/hacdias/webdav/releases/download/v5.4.2/linux-amd64-webdav.tar.gz"
initial_destination = "/tmp/linux-amd64-webdav.tar.gz"  # 临时保存路径
extract_dir = "/usr/bin/webdav"  # 解压到 OpenWrt 中的目标目录
webdav_path = os.path.join(extract_dir, "webdav")  # WebDAV 执行文件路径
shared_dir = "/root/share"  # 共享目录路径

# 执行下载、解压、启动操作
download_and_manage_file(url, initial_destination, extract_dir, webdav_path, shared_dir)
