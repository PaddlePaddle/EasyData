
# 数据集&标注工具
EasyData为大家搜集并整理了各个领域经典、前沿、产业的数据集和标注工具，提供可供下载和分享的地址, 覆盖机器学习/深度学习各大领域, 如计算机视觉, 语音, 自然语言处理等等.

- ### [数据集](#数据集)

- ### [标注工具](#标注工具)


### 数据集
- 发布数据集覆盖CV、NLP、Speech等20+任务的125产业数据集，并针对开源产业数据集提供了便捷的下载脚本、读取API以及规范化格式方便开发者使用飞桨套件快速进行训练
<table style="margin-left:auto;margin-right:auto;font-size:1.3vw;padding:5px 8px;text-align:center;vertical-align:center;">
  <tr>
    <td colspan="4" style="font-weight:bold;">计算机视觉</td>
  </tr>
  <tr>
    <td><a href="./datasets/Detection.md">目标检测</a>(9)</td>
    <td><a href="./datasets/Segmentation.md">图像分割</a> (12)</td>
    <td><a href="./datasets/Clas.md">图像分类</a> (5)</td>
    <td><a href="./datasets/Video.md">视频理解</a> (4)</td>
   
  <tr>
    <td><a href="./datasets/OCR.md">文字识别</a> (21)</td>
    <td><a href="./datasets/Keypoints.md">关键点检测</a> (6)</td>
    <td><a href="./datasets/Image_Denoising.md">图像去噪</a> (5)</td>
     <td><a href="./datasets/3D.md">3D感知</a> (3)</td>
    
  </tr>
  <tr>

  
  </tr>
  <tr>
    <td colspan="4" style="font-weight:bold;">自然语言处理</td>
  </tr>
  <tr>
    <td><a href="./datasets/NLP.md">阅读理解</a> (7)</td>
    <td><a href="./datasets/NLP.md">文本分类</a> (33)</td>
    <td><a href="./datasets/NLP.md">文本匹配</a> (1)</td>
    <td><a href="./datasets/NLP.md">序列标注</a> (3)</td>
  </tr>
  
  <tr>
    <td><a href="./datasets/NLP.md">机器翻译</a> (2)</td>
    <td><a href="./datasets/NLP.md">对话系统</a> (1)</td>
    <td><a href="./datasets/NLP.md">文本生成</a> (6)</td>
    <td><a href="./datasets/NLP.md">语料库</a> (2)</td>
  </tr>
  
<tr>
    <td colspan="4" style="font-weight:bold;">语音</td>
  </tr>
  <tr>
    <td><a href="./datasets/Speech.md">语音识别</a> (1)</td>
    <td><a href="./datasets/Speech.md">语音合成</a> (1)</td>
    <td><a href="./datasets/Speech.md">声音分类</a> (1)</td>
    <td><a href="./datasets/Speech.md">声纹识别</a> (1)</td>
  </tr>
    <tr>
    <td><a href="./datasets/Speech.md">语音唤醒</a> (1)</td>
  </tr>

</table>





###  标注工具
- 7个产业经典和自研半自动标注工具：涵盖了通用、人像、遥感、医疗、视频、文本、体育等不同方向的高质量交互式模型进行数据预标注，高效的节省人力；并将自研标注工具获取到的标注应用到飞桨各个套件的模型可以直接进行训练，得到定制化场景的高精度模型，打通任务从数据标注到模型训练及预测的全流程

<table style="margin-left:auto;margin-right:auto;font-size:1.3vw;padding:3px 5px;text-align:center;vertical-align:center;">
  <tr>
    <td colspan="5" style="font-weight:bold;">计算机视觉</td>
  </tr>
  <tr>
    <td><a href="./Annotation_tool/PPOCRLabelv2.md">半自动标注工具PPOCRLabelv2</a></td>
     <td>适用于OCR领域的半自动化图形标注工具</td>
    <td>
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/PPOCRLabel/data/gif/steps_en.gif" width="400"> 
    </td>
 
  <tr>
    <td><a href="./Annotation_tool/EISeg.md">交互式分割标注软件EISeg</a></td>
     <td>交互式分割标注软件。涵盖通用、人像、遥感、医疗、视频等任务的高质量交互式分割模型</td>
    <td>
    <img src="https://user-images.githubusercontent.com/71769312/141130688-e1529c27-aba8-4bf7-aad8-dda49808c5c7.gif" width="600"> 
    </td>
   
   <tr>
    <td><a href="./Annotation_tool/PaddleLabel.md">多功能标注工具PaddleLabel</a></td>
     <td>支持图像分类、检测、分割三种常见的计算机视觉任务</td>
    <td>
    <img src="https://user-images.githubusercontent.com/71769312/185099439-3230cf80-798d-4a81-bcae-b88bcb714daa.gif" width="400"> 
    </td>
   
<tr>
    <td><a href="./Annotation_tool/EIVideo.md">交互式智能视频标注工具EIVideo</a></td>
     <td>只需简单标注几帧，即可完成全视频标注</td>
    <td>
    <img src="https://ai-studio-static-online.cdn.bcebos.com/f792bac0dd3b4f44ade7d744b58e908e2a85ed8718b541cfb6b2ce9fc8ad4374" width="400"> 
    </td>
 <tr>
    <td><a href="https://github.com/wkentaro/labelme">Labelme</a></td>
     <td>开源图像标注工具，方便进行使用及二次开发，支持图像所有任务</td>
    <td>
    <img src="https://raw.githubusercontent.com/wkentaro/labelme/main/examples/classification/.readme/annotation_cat.jpg" width="400"> 
    </td>
     
 <tr>
    <td colspan="5" style="font-weight:bold;">自然语言处理</td>
  </tr>
  <tr>
    <td><a href="./Annotation_tool/doccano.md">Doccano</a></td>
     <td>文本标注工具，为NLP任务的语料库进行打标。支持情感分析，命名实体识别，文本摘要等任务</td>
    <td>
    <img src="https://raw.githubusercontent.com/doccano/doccano/master/docs/images/demo/demo.gif" width="400"> 
    </td>

 <tr>
    <td colspan="5" style="font-weight:bold;">语音</td>
  </tr>
  <tr>
    <td><a href="./Annotation_tool/Speech.md">Praat</a></td>
     <td>支持语音合成任务</td>
    <td>
    <img src="https://user-images.githubusercontent.com/30135920/197728536-14cc083b-6f7a-40dd-b66a-a8a9fe56924f.png" width="400"> 
    </td>
 <tr>
    <td><a href="./Annotation_tool/Speech.md">label-studio</a></td>
     <td>多功能标注工具，可以用于语音识别，说话人识别等多种语音标注任务</td>
    <td>
    <img src="https://user-images.githubusercontent.com/30135920/198205186-f99026f9-32a9-4b17-8e9b-9af18c119f41.png" width="400"> 
    </td>





</table>

