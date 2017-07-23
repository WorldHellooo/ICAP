# Image Caption Annotation Program
## 功能介绍
在对MS COCO数据集进行中文标注时，需要设计一款简单可靠、带有界面的、多平台通用的标注程序，实现显示指定图片及其英文标注参照，采集保存用户的中文标注信息。

## 使用说明
图片数据集下载地址http://msvocds.blob.core.windows.net/coco2014/train2014.zip

json文件请选择本项目里附带的json文件

在进入标注界面后，左侧为全部图像的列表，按回车切换到光标所在图像，也可点击右下角的Next和Last按钮进行切换。中间为当前图像，右侧上方为对应的英文标注参照，其下方有五个文本框，由用户输入五句中文标注，点右侧的Save即可保存。

本项目利用pyInstaller进行了编译，并在dist文件夹下提供了ubuntu版的可执行文件。
