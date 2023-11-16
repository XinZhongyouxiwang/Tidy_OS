# parsing 帮助文档

## 文件信息
- 文件地址: /terminal/parsing.py
- 主要作用: 解析从 /Tterminal.py 传入的命令后按照指定文件的 [command_dict](../command_dic%20帮助文档.md) 字典解析参数后传入文件
- 缺少次文件该主程序的影响: 导致整个程序无法正常运行
- 修改后影响: <font color='red'>高</font>

## i_terminal 函数
### 函数介绍
i _terminal 函数为 parsing.py 文件的主要函数, 作用是对用户端传入的命令找出指定的命令并调用[trigger函数](#trigger-函数)后向用户端返回指定的状态码<br>
住: python 文件的查找路径为 /apm/package/
### 状态码(return)
#### 200
- 正常

#### 400
- 警告
- 可能导致原因: 无法找到有效的 python文件
- 建议修复方法:
<br>1. 查看 /apm/package/ 目录下是否存在指定的python文件, 若不存在可以使用 `apm install <package>` 命令安装该python文件

#### 401
- 错误(严重)
- 可能导致原因: 指定的 python文件出现严重错误
- 建议修复方法: 
<br>1. 检查 /apm/package/ 目录下的文件是否存在错误
<br>2. 检查当前 python 版本是否符合 Tterminal 或 指定python文件 的运行条件
<br>3. 检查当前环境是否安装了指定python文件的第三方运行库
<br>4. 如果指定python文件中使用了 pyautogui 库时, 应 pyautogui 库不支持WSL环境, 请退出WSL环境后重试



## trigger 函数
### 函数介绍
触发对应的python 文件并向这个文件传入一些参数

### 状态码(return)
#### 200
- 正常

#### 400
- 错误
- 表示问题: 映射表内存有该命令, 但无法在 /apm/package/ 目录下找到
- 可能导致原因: /apm/package 目录下的指定python 文件被删除
- 建议修复方法:
<br>1. 检查指定文件的文件名名是否与 [/apm/_command.json](../../apm/_command.json) 文件下指定文件中的 "file" 的值相符合
<br>2. 如果 /apm/package/ 目录下不存在指定的python文件, 那么您可以尝试使用 `apm -b <package>` 命令重新安装该命令
