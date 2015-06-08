# python_small_project
用python写的一些小工具
一、mail:<br>
1、mail是一个用于从邮箱服务器上下载邮件附件的小项目（为了帮助自己更快地收作业。。。）<br>
2、文件结构：
（1）downMail:代码文件。里面的很多代码参考了廖学峰的博客里面pop3部分教程的代码。自己写了downloaFile()函数用于下载附件和写了getConfig()用于把读取配置项<br>
（2）config.txt：是downMail的配置文件，用于配置邮件服务器，用户名，密码，文件存储路径，匹配关键词（只有附件的名称有对应的keyword的时候才会下载）还有开始检查的邮件位置和检查的邮件总数等。
