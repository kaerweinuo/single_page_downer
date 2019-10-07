# python单页下载类
python的单页下载类，仅下载单页的html、css和js，以及html中包含的img
# 用法
1.引入类<br>  
2.实例化类<br>  
下载普通页面<br>  
d=Download("链接","保存的目录")<br>  
下载ajax生成的动态页面<br>  
d=Download("链接","保存的目录",model= "complex")<br>  
# 尚需完善的内容
1.html中<style></style>中包含的图片<br>  
2.css中包含的图片
