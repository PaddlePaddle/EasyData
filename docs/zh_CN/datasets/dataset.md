
# 数据集&标注工具
EasyData为大家搜集并整理了各个领域经典、前沿、产业的数据集和标注工具，提供可供下载和分享的地址, 覆盖机器学习/深度学习各大领域, 如计算机视觉, 语音, 自然语言处理等等.

- ## [数据集](#数据集)

- ## [标注工具](#标注工具)


具体如下：

### 数据集
* 计算机视觉
    - [目标检测](datasets/Detection.md)
    - [图像分割](datasets/Segmentation.md)
    - [图像分类](datasets/Clas.md)
    - [视频理解](datasets/Video.md)
    - [3D感知](datasets/3D.md)
    - [文字识别](datasets/OCR.md)

  
* 自然语言处理
    * [阅读理解](datasets/NLP.md)
    * [文本分类](datasets/NLP.md)
    * [文本匹配](datasets/NLP.md)
    * [序列标注](datasets/NLP.md)
    * [机器翻译](datasets/NLP.md)
    * [对话系统](datasets/NLP.md)
    * [文本生成](datasets/NLP.md)
    * [语料库](datasets/NLP.md)

* 语音
   * [语音识别](datasets/NLP.md)
   * [语音翻译](datasets/NLP.md)
   * [语音合成](datasets/NLP.md)
   * [声音分类](datasets/NLP.md)
   * [声纹识别](datasets/NLP.md)
   * [唤醒](datasets/NLP.md)


###  标注工具
* [半自动标注工具PPOCRLabelv2](Annotation_tool/PPOCRLabelv2.md)
    -  PPOCRLabel是一款适用于OCR领域的半自动化图形标注工具，内置PP-OCR模型对数据自动标注和重新识别。使用Python3和PyQT5编写，支持矩形框标注、表格标注、不规则文本标注、关键信息标注模式，导出格式可直接用于PaddleOCR检测和识别模型的训练。
<div align="center">
<table>
    <tr>
 <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/PPOCRLabel/data/gif/steps_en.gif" width="80% center"/>  
     <tr>      
</table>
</div>

* [数据合成工具Style-Text](Annotation_tool/Style_Text.md)
    - Style-Text数据合成工具是基于百度和华科合作研发的文本编辑算法《Editing Text in the Wild》https://arxiv.org/abs/1908.03047
<div align="center">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/StyleText/doc/images/3.png" width="600">
</div>

<div align="center">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/StyleText/doc/images/1.png" width="600">
</div>


* [交互式分割标注软件EISeg](Annotation_tool/EISeg.md)

    - EISeg(Efficient Interactive Segmentation)基于飞桨开发的一个高效智能的交互式分割标注软件。它涵盖了通用、人像、遥感、医疗、视频等不同方向的高质量交互式分割模型。 另外，将EISeg获取到的标注应用到PaddleSeg提供的其他分割模型进行训练，便可得到定制化场景的高精度模型，打通分割任务从数据标注到模型训练及预测的全流程。

  * 高效的半自动标注工具，已上线多个Top标注平台
  * 覆盖遥感、医疗、视频、3D医疗等众多垂类场景
  * 多平台兼容，简单易用，支持多类别标签管理
    <div align="center">
    <img src="https://user-images.githubusercontent.com/71769312/141130688-e1529c27-aba8-4bf7-aad8-dda49808c5c7.gif" width="600">
    </div>

* [多功能标注工具PaddleLabel](Annotation_tool/PaddleLabel.md)
    - PaddleLabel 是基于飞桨 PaddlePaddle 各个套件的特性提供的配套标注工具。它涵盖分类、检测、分割三种常见的计算机视觉任务的标注能力，具有手动标注和交互式标注相结合的能力。用户可以使用 PaddleLabel 方便快捷的标注自定义数据集并将导出数据用于飞桨提供的其他套件的训练预测流程中。
    <div align="center">
    <img src="https://user-images.githubusercontent.com/71769312/185099439-3230cf80-798d-4a81-bcae-b88bcb714daa.gif" width="600">
    </div>

* [交互式智能视频标注工具-EIVideo](Annotation_tool/EIVideo.md)
    - EIVideo，基于百度飞桨MA-Net交互式视频分割模型打造的交互式**智能视频**标注工具箱，只需简单标注几帧，即可完成全视频标注，若自动标注结果未达要求还可通过多次和视频交互而不断提升视频分割质量，直至对分割质量满意。  

    <div align="center">
    <img width="600" alt="图片" src="https://ai-studio-static-online.cdn.bcebos.com/f792bac0dd3b4f44ade7d744b58e908e2a85ed8718b541cfb6b2ce9fc8ad4374">
    </div>
* [Labelme](https://github.com/wkentaro/labelme)
    - Labelme是一个开源图像标注工具，对它进行使用及二次开发涉及到比较多的知识，通过研究labelme可以了解很多新知识，除了文中介绍的一些知识外，还有图形开发工具QT Designer，是一种可以集成到pycharm中的图形开发工具，生成ui文件，可以转换为py文件，和pycharm结合，可以进行图形界面开发，python版的labelme就是使用QT开发界面。
     <div align="center">
    <img width="600" alt="图片" src="https://raw.githubusercontent.com/wkentaro/labelme/main/examples/classification/.readme/annotation_cat.jpg">
    </div>