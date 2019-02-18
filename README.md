# alipaycrawl
1、	文件列表：
alitest2.py：程序代码
info：配置文件，填写用户名、密码、输出文件
chromedriver：chrome浏览器的linux驱动程序

2、	部署步骤：
第一步：系统环境准备：yum update
                  yum install Xvfb
yum install libXfont
yum install xorg-x11-fonts*
pip install --upgrade pip
pip install pyvirtualdisplay
pip install selenium
pip uninstallurllib3
pip uninstall chardet
pip install requests

第二步：安装chrome浏览器：
      在目录 /etc/yum.repos.d/ 下新建文件 google-chrome.repo, 并且在该文件中添加如下内容：
 [google-chrome]
 name=google-chrome
 baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch
 enabled=1
 gpgcheck=1
 gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub                                                                

然后：yum -y install google-chrome-stable --nogpgcheck

第三步：创建一般用户 useradd alitest
                     cd /home/alitest
                     su alitest
                 nohup Xvfb -ac :7 -screen 0 1280x1024x8 > /dev/null 2>&1 &
export DISPLAY=:7

第三步：将文件夹内的所有文件拷贝至/home/alitest
                     chmod a+x chromedriver

第三部：填写配置文件，填入用户名/密码/输出文件

第四部：添加定时任务：python alitest2.py每十分钟执行一次，或者直接运行run.sh
