# LTP-Flask

<img width="690" alt="image" src="https://user-images.githubusercontent.com/38573173/202845959-c0f4048f-767d-4aab-b5e8-3e7571bd5493.png">

## 基本情况  
语言： Python  
（开发时使用3.10.6，仅供参考）  
基于 Flask、LTP

## 模型
哈工大 Base2模型与Legacy模型  
[模型获取 Base2](https://huggingface.co/LTP/base2)  
[模型获取 Legacy](https://huggingface.co/LTP/legacy)  
目录结构： 
![image](https://user-images.githubusercontent.com/38573173/202848279-f50e3c9c-59f6-4fd6-b8c0-226caa106211.png)


## 端口
默认 8848 

host为 0.0.0.0

## 使用

`set_up.py` 安装所需库

`server.py` 运行服务

浏览器打开 `localhost:8848`即可

若需要局域访问以调试，请在防火墙中手动添加`8848端口`

## 输入
自己指定文件夹目录

## 输出
output文件夹内

## 其它
发现问题，您可以在Issues里告诉我，我有空会fix
