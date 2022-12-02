# EasyData



## 简介

EasyData 旨在打造一套通用、领先且实用的数据自动扩充与数据清洗工具库，并提供开源数据集与标注工具大全，助力开发者获得高质量的训练、推理数据，从而提升 AI 算法的实用效果。


|  <img src="https://user-images.githubusercontent.com/45199522/202378223-f7899f71-ae05-4f2a-b814-60707c013c1f.gif"  width = "300" height="60%" />                      | <img src="https://user-images.githubusercontent.com/59186797/202600222-a18e467d-5d93-41e1-80de-e3cac93c71fd.gif" width="300" height="60%"/> |
| :----------------------------------------------------: | :-------------: |
| DataClean 数据清洗效果图   | DataAug 数据自动扩充效果图 |

  <img src="https://user-images.githubusercontent.com/59186797/202604566-56083c28-a17c-4a60-ba6c-acfb1bdda2d7.gif"  width = "300" height = "60%" />                      | <img src="https://user-images.githubusercontent.com/59186797/202602413-00a7c51e-4e97-4f37-9fa0-febe6c2f69f3.gif" width="300" height = "60%"/> |
| :----------------------------------------------------: | :-------------: |
| 120+经典产业数据集   | 7+半自动标注工具 |





## 📣 近期更新

- **💥 直播预告**:12.6-7日每晚8点半，EasyData研发团队详解数据清洗策略和数据合成工具。微信扫描下方二维码，关注公众号并填写问卷后进入官方交流群，获取获取直播链接与20G重磅EasyData学习大礼包(自研半自动标注应用程序，数据处理相关CVPR、AAAI、ACL、IJCAI顶级会议paper list，手把手教学视频以及学习资料)，获取发布最新资讯。

 <div align="center">
<img src="https://user-images.githubusercontent.com/59186797/200607111-ae440419-d302-4bdc-9970-5d9dba08ea0f.jpg"  width = "150" height = "150" />
</div>

- **🔥2022.11 发布 EasyData beta/0.5**
  - 发布数据清洗工具，包括图像方向矫正、低质图像过滤能力，使用该工具可以在多个视觉任务中提升效果。
  - 发布数据扩充工具，支持增广数据生成、重复和低质数据过滤，使用该工具可以在整图识别场景中提升效果。
  - 新增CV、NLP、Speech方向的120+[数据集](docs/zh_CN/datasets/dataset.md)，7经典+自研半自动[标注工具](docs/zh_CN/datasets/dataset.md)



## ⚡ 快速开始

- [数据清洗快速体验](docs/zh_CN/DataClean/quick_start.md)
- [数据合成工具快速体验](docs/zh_CN/DataAug/quick_start.md)
- [开源数据集和标注工具大全](docs/zh_CN/datasets/dataset.md)

## 👫 开源社区

- **📑项目合作：** 如果您是企业开发者且有明确的EasyData应用需求，填写问卷链接待更新后可免费与官方团队展开不同层次的合作。
- **👫加入社区：** 微信扫描二维码并填写问卷之后，加入交流群与EasyData研发工程师1V1交流
- **🎁社区共建**：EasyData欢迎与大家一起打造行业把数据治理打造成业界的新标准



## 🛠️ EasyData 模型列表（更新中）

| 类别 | 亮点 | 文档说明 | 模型下载 |
| :--: | :--: | :------: | :------: |
|图像方向矫正|自动矫正图像，大大提升多项视觉任务在旋转图像上精度|[文档](docs/zh_CN/DataClean/image_orientation_correction.md)|[下载链接](https://paddleclas.bj.bcebos.com/models/PULC/inference/image_orientation_infer.tar)|
|模糊图像过滤|判断图像是否模糊，可以广泛应用于模糊图像过滤、视觉相关业务的前处理等|[文档](docs/zh_CN/DataClean/blured_image_filtering.md)|[下载链接](https://paddleclas.bj.bcebos.com/models/PULC/inference/clarity_assessment_infer.tar)|
|广告码图像过滤|判断图像是否含有二维码、条形码、小程序码，可以广泛应用于广告码过滤、审核等业务|[文档](docs/zh_CN/DataClean/code_image_filtering.md)|[下载链接](https://paddleclas.bj.bcebos.com/models/PULC/inference/code_exists_infer.tar)|


## 📖 文档教程

- 数据清洗
  - [快速体验](docs/zh_CN/DataClean/quick_start.md)
  - [数据清洗工具集](docs/zh_CN/DataClean/DataClean.md)
    - [图像方向校正工具](docs/zh_CN/DataClean/image_orientation_correction.md)
    - [模糊图像过滤工具](docs/zh_CN/DataClean/blured_image_filtering.md)
    - [二维码图像过滤工具](docs/zh_CN/DataClean/code_image_filtering.md)
- 数据扩充
  - [快速体验](docs/zh_CN/DataAug/quick_start.md)
  - [流程详解](docs/zh_CN/DataAug/DataAug.md)

- [标注工具](docs/zh_CN/datasets/dataset.md)
  - 计算机视觉
    - [半自动标注工具PPOCRLabelv2](docs/zh_CN/datasets/Annotation_tool/PPOCRLabelv2.md)
    - [交互式分割标注软件EISeg](docs/zh_CN/datasets/Annotation_tool/EISeg.md)
    - [多功能标注工具PaddleLabel](docs/zh_CN/datasets/Annotation_tool/PaddleLabel.md)
    - [交互式智能视频标注工具-EIVideo](docs/zh_CN/datasets/Annotation_tool/EIVideo.md)
    - [Labelme](https://github.com/wkentaro/labelme)
  - 自然语言处理
    - [Doccano](docs/zh_CN/datasets/Annotation_tool/doccano.md)
  - 语音
    - [Praat](docs/zh_CN/datasets/Annotation_tool/Speech.md)
    - [label-studio](docs/zh_CN/datasets/Annotation_tool/Speech.md)
- [数据集](docs/zh_CN/datasets/dataset.md)
  - 计算机视觉
    - [目标检测](docs/zh_CN/datasets/datasets/Detection.md)
    - [图像分割](docs/zh_CN/datasets/datasets/Segmentation.md)
    - [图像分类](docs/zh_CN/datasets/datasets/Clas.md)
    - [视频理解](docs/zh_CN/datasets/datasets/Video.md)
    - [文字识别](docs/zh_CN/datasets/datasets/OCR.md)
    - [关键点检测](docs/zh_CN/datasets/datasets/Keypoints.md)
    - [图像去噪](docs/zh_CN/datasets/datasets/Image_Denoising.md)
    - [3D感知](docs/zh_CN/datasets/datasets/3D.md)

  - 自然语言处理
    - [阅读理解](docs/zh_CN/datasets/datasets/NLP.md)
    - [文本分类](docs/zh_CN/datasets/datasets/NLP.md)
    - [文本匹配](docs/zh_CN/datasets/datasets/NLP.md)
    - [序列标注](docs/zh_CN/datasets/datasets/NLP.md)
    - [机器翻译](docs/zh_CN/datasets/datasets/NLP.md)
    - [对话系统](docs/zh_CN/datasets/datasets/NLP.md)
    - [文本生成](docs/zh_CN/datasets/datasets/NLP.md)
    - [语料库](docs/zh_CN/datasets/datasets/NLP.md)
  - 语音
    - [语音识别](docs/zh_CN/datasets/datasets/Speech.md)
    - [语音合成](docs/zh_CN/datasets/datasets/Speech.md)
    - [声音分类](docs/zh_CN/datasets/datasets/Speech.md)
    - [声纹识别](docs/zh_CN/datasets/datasets/Speech.md)
    - [语音唤醒](docs/zh_CN/datasets/datasets/Speech.md)
- 许可证书


## 许可证书
本项目的发布受<a href="https://github.com/PaddlePaddle/PaddleOCR/blob/master/LICENSE">Apache 2.0 license</a>许可认证。
