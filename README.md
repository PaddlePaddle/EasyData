# EasyData



## 简介

EasyData 旨在打造一套通用、领先且实用的数据自动扩充与数据清洗工具库，并提供开源数据集与标注工具大全，助力开发者获得高质量的训练、推理数据，从而提升 AI 算法的实用效果。


|             PP-DataClean 数据清洗效果图             |
| :----------------------------------------------------: |
| <img src="./docs/images/PP-dataClean/PP-DataClean-demo.gif"  width = "800" /> |

[EDA数据合成效果图@晓婷]

<div align="center">
<table>
    <tr>
        <td><img src="docs/zh_CN/datasets/dataset_picture/EIvideo.gif" width=300></td>
        <td><img src="docs/zh_CN/datasets/dataset_picture/kie.gif" width=350></td>
    <tr>
    <tr>    
         <td align="center">交互式智能视频标注工具</td>
         <td align="center">OCR领域多功能半自动化图形标注</td>
    <tr>
  
  
</table>
</div>

<div align="center">
<table>
    <tr>
        <td><img src="docs/zh_CN/datasets/dataset_picture/EIseg.gif"  width=600></td>
    <tr>
    <tr>    
         <td align="center">交互式分割标注涵盖通用、人像、遥感、医疗、视频等功能</td>
    <tr>
  
  
</table>
</div>

<div align="center">
<table>
   
  <tr>
        <td><img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleDetection/release/2.5/docs/images/picedet_demo.jpeg" width=600></td>
  
  <tr>
   
   <tr>    
         <td align="center">涵盖CV、NLP、Speech等方向的数据集</td>
        
  <tr>
  
  
</table>
</div>


## 📣 近期更新

- **💥 直播预告**:11.23-11.24日每晚8点半，EasyData研发团队详解数据清洗策略和数据合成工具。微信扫描下方二维码，关注公众号并填写问卷后进入官方交流群，获取获取直播链接与20G重磅EasyData学习大礼包(自研半自动标注应用程序，数据处理相关CVPR、AAAI、ACL、IJCAI顶级会议paper list，手把手教学视频以及学习资料)，获取发布最新资讯。

 <div align="center">
<img src="https://user-images.githubusercontent.com/59186797/200607111-ae440419-d302-4bdc-9970-5d9dba08ea0f.jpg"  width = "150" height = "150" />
</div>

- **🔥2022.11 发布 EasyData beta/0.5**
  - 发布数据清洗工具，包括图像方向矫正、低质图像过滤能力，使用该工具可以在多个视觉任务中提升效果。
  - 发布数据扩充工具，支持增广数据生成、重复和低质数据过滤，使用该工具可以在整图识别场景中提升效果。
  - 新增CV、NLP、Speech方向的50+[数据集](docs/zh_CN/datasets/dataset.md)，6+[自研半自动标注工具](docs/zh_CN/datasets/dataset.md)



## ⚡ 快速开始

- [数据清洗快速体验](docs/zh_CN/PP-DataClean/quick_start.md)
- [数据合成工具快速体验](docs/zh_CN/PP-EDA/quick_start.md)
- [开源数据集和标注工具大全](docs/zh_CN/datasets/dataset.md)

## 👫 开源社区

- **📑项目合作：** 如果您是企业开发者且有明确的EasyData应用需求，填写问卷链接待更新后可免费与官方团队展开不同层次的合作。
- **👫加入社区：** 微信扫描二维码并填写问卷之后，加入交流群与EasyData研发工程师1V1交流  
- **🎁社区共建**：EasyData欢迎与大家一起打造行业把数据治理打造成业界的新标准

<div align="center">
<img src="https://user-images.githubusercontent.com/59186797/200607111-ae440419-d302-4bdc-9970-5d9dba08ea0f.jpg"  width = "150" height = "150" />
</div>

## 🛠️ EasyData 模型列表（更新中）

| 类别 | 亮点 | 文档说明 | 模型下载 |
| :--: | :--: | :------: | :------: |
|图像方向矫正|自动矫正图像，大大提升多项视觉任务在旋转图像上精度|[文档](docs/zh_CN/PP-DataClean/image_orientation_correction.md)|[下载链接](https://paddleclas.bj.bcebos.com/models/PULC/inference/image_orientation_infer.tar)|
|模糊图像过滤|判断图像是否模糊，可以广泛应用于模糊图像过滤、视觉相关业务的前处理等|[文档](docs/zh_CN/PP-DataClean/blured_image_filtering.md)|[下载链接](https://paddleclas.bj.bcebos.com/models/PULC/inference/clarity_assessment_infer.tar)|
|广告码图像过滤|判断图像是否含有二维码、条形码、小程序码，可以广泛应用于广告码过滤、审核等业务|[文档](docs/zh_CN/PP-DataClean/code_image_filtering.md)|[下载链接](https://paddleclas.bj.bcebos.com/models/PULC/inference/code_exists_infer.tar)|


## 📖 文档教程

- 运行环境准备 @晓婷
- 数据清洗
  - [快速体验](docs/zh_CN/PP-DataClean/quick_start.md)
  - [数据清洗工具集](docs/zh_CN/PP-DataClean/PP-DataClean.md)
    - [图像方向校正工具](docs/zh_CN/PP-DataClean/image_orientation_correction.md)
    - [模糊图像过滤工具](docs/zh_CN/PP-DataClean/blured_image_filtering.md)
    - [二维码图像过滤工具](docs/zh_CN/PP-DataClean/code_image_filtering.md)
- 数据扩充
  - [快速体验](docs/zh_CN/PP-EDA/quick_start.md)
  - [流程详解](docs/zh_CN/PP-EDA/EasyDataAug.md)
- 开源数据集
  - [目标检测](docs/zh_CN/datasets/datasets/Detection.md)
  - [图像分割](docs/zh_CN/datasets/datasets/Segmentation.md)
  - [图像分类](docs/zh_CN/datasets/datasets/Clas.md)
  - [视频理解](docs/zh_CN/datasets/datasets/Video.md)
  - [3D感知](docs/zh_CN/datasets/datasets/3D.md)
  - [文字识别](docs/zh_CN/datasets/datasets/OCR.md)
  - [自然语言处理](docs/zh_CN/datasets/datasets/NLP.md)
  - [语音](docs/zh_CN/datasets/datasets/Speech.md)
- 数据标注工具大全
  * [半自动标注工具PPOCRLabelv2](docs/zh_CN/datasets/Annotation_tool/PPOCRLabelv2.md)
  * [数据合成工具Style-Text](docs/zh_CN/datasets/Annotation_tool/Style_Text.md)
  * [交互式分割标注软件EISeg](docs/zh_CN/datasets/Annotation_tool/EISeg.md)
  * [多功能标注工具PaddleLabel](docs/zh_CN/datasets/Annotation_tool/PaddleLabel.md)
  * [交互式智能视频标注工具-EIVideo](docs/zh_CN/datasets/Annotation_tool/EIVideo.md)
  * [Labelme](https://github.com/wkentaro/labelme)

- 许可证书


## 许可证书
本项目的发布受<a href="https://github.com/PaddlePaddle/PaddleOCR/blob/master/LICENSE">Apache 2.0 license</a>许可认证。
