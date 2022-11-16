# Data Augment

- [1. 简介](#1)
- [2. 环境准备](#2)
- [3. 数据准备](#3)
- [4. 数据自动扩充](#4)
- [5. 扩充数据使用](#5)

<a name="1"></a>
## 1. 简介

近几年很多方向的视觉任务取得了重大的进展，文本识别、目标检测、图像分类等领域均有表现优秀的算法。然而这些算法高度依赖训练数据的多样性，真实数据的标注需要耗费人力和时间成本。因此如何基于有限的数据扩充训练样本，是产业落地的关键问题。此外合成图像质量不一，质量过差或冗余数据过多都可能影响模型训练。如何保证合成数据的质量也是一大关键问题。

数据自动扩充工具 PP-DataAug 旨在合成丰富、有效、精简的数据集，显著提升多个场景任务的效果。本文主要对PP-DataAug流程进行详细介绍。

## 1.1 使用背景

训练视觉任务通常依赖大量的数据，但是真实数据的标注需要耗费人力和时间成本，PP-DataAug主要解决用户在缺少数据的情况下如何提升原有模型的精度。使用本工具的前提是拥有一定的训练数据，并且训练出了一个基础模型。另外，PP-DataAug工具目前只支持整图识别类任务，也即图像分类、文本识别、商品识别等场景，对于检测场景或者是其他多点标注的场景暂不支持。

<a name="2"></a>
## 2. 环境准备

推荐使用源码进行准备环境，首先参考[文档](./quick_start.md)安装PaddlePaddle，如已安装，进行下一步

```bash
git clone https://github.com/PaddlePaddle/EasyData.git
pip install -r requirements.txt
```
我们也提供了相应的whl包快速使用教程，参考[快速开始](./quick_start.md)

<a name="3"></a>
## 3. 数据准备
本项目主要以图像分类、文本识别为例进行讲解，并且提供了一些demo数据，位于[demo](../../../demo/)文件夹下。如若在自己的数据集上进行使用，可以参考下面数据组织形式进行准备数据。

### 3.1 图像分类数据集：

  提供原始图片，PP-DataAug将自动完成基于图片的数据增广、筛选、清洗功能，输出扩充后的数据集。 原始数据组织形式：

  ```
  ├── clas_data
  │   ├── train
  │   ├── train_list.txt
  ```
  train_list.txt文件中默认请将图片路径和图片标签用 空格 分割，txt文件里的内容如下:

  ```
  " 图像文件名 图像类别 "

  train/xxxx1.jpg 0
  train/xxxx2.jpg 1
  ...
  ```


### 3.2 文本识别数据集：

  文本识别数据扩充支持两种模式

  - img2img

  提供原始图片，PP-DataAug将自动完成基于图片的数据增广、筛选、清洗功能，输出扩充后的数据集。

  原始训练数据和标签文件`train_list.txt`组织形式 ：

  ```
  ├── ocr_data
  │   ├── images
  │   ├── train_list.txt
  ```
  train_list.txt文件中 图片路径和图片标签默认使用 \t 分割，具体内容如下:

  ```
  " 图像文件名                 图像标注信息 "

  images/xxxx1.jpg            简单可依赖
  images/xxxx2.jpg        用科技让复杂的世界更简单
  ...
  ```

  - text2img

  提供文本语料、字体、背景图，PP-DataAug自动完成基于语料的文本识别图像生成、筛选、清洗功能，输出扩充后的数据集。


  字体文件、背景图和原始语料文件`corpus.txt`组织形式 :

  ```
  ├──ocr_rec/
  │  |-- bg
  │  |-- corpus.txt
  │  |-- font
  │      |-- 1.ttf
  │      |-- 2.ttf
  ```

  其中`corpus.txt`文件内容为：

  ```
  母婴百汇
  停车场
  品质沙龙
  散作乾坤万里春
  24小时营业
  ```
  **说明：** 每行代表一条语料


<a name="4"></a>

## 4. 数据自动扩充

完成环境和数据准备后，使用PP-DataAug工具进行自动数据扩充。整个流程包含三个部分：离线增强数据、低质数据过滤、重复数据过滤，下面依次进行介绍。

<div align="center">
    <img alt="eda_pipeline" src="https://user-images.githubusercontent.com/87074272/201034520-f38f2c64-0603-4f64-9f77-6413ec4dff2c.png" width=800 hight=400>
</div>


### 4.1 离线增强数据
数据增广普遍应用于训练阶段，且大都采用在线增广的形式来随机生成不同的增广图，但是在线增广图的质量却无法保证，对模型提升的精度有限。PP-DataAug 工具主要参考真实场景的训练数据，离线合成一批丰富有效的增广数据。该工具融合了裁剪类、变换类和擦除类的代表算法，如 RandomCrop, RandAugment, RandomErasing, Gridmask, Tia等。具体地，可以通过指定增广方式和增广数量来离线生成增广数据，以 ImageNet 分类数据集为例，使用 PP-DataAug 工具得到的离线增广效果图如下：

<div align="center">
    <img alt="aug" src="https://user-images.githubusercontent.com/87074272/201034705-69f66eee-0432-43a4-adb3-91101534862a.png" width=800 hight=400>
</div>

### 4.2 重复数据过滤
由于使用了多种增广方式，并且每种增广都具有一定的随机性，如增广的强度，增广的位置，因此大量生成离线增广数据可能会有重复数据，也即图像（特征）极其相似的增广图，不仅增广图和原始图片会产生重复数据，增广图之间也会产生重复，如下图所示：

<div align="center">
    <img alt="repeat" src="https://user-images.githubusercontent.com/87074272/201034854-06835ea8-1f17-4638-8927-5329160fd834.png" width=400 hight=200>
</div>


可以看出，这些增广图具有很高的相似度，因此去除这些重复数据是很有必要的。具体地，采用[PP-ShiTu](https://github.com/PaddlePaddle/PaddleClas/blob/develop/docs/zh_CN/training/PP-ShiTu/feature_extraction.md)模型中的特征提取模块对离线增广的图像进行特征提取，然后将特征相似度高于一定阈值的增广数据进行剔除。为了便于去除所有可能的重复数据，使用原始数据和所有增广后的数据来构建全量特征检索库（gallery），然后依次对增广图进行特征查询（query），保留得分第二高的查询结果，如果得分大于阈值（如0.95），那么判定该数据为重复数据。

### 4.3 低质数据过滤
由于数据增广具有一定的随机性，离线增广后的数据可能会存在一些低质量的数据，这些数据会影响模型的性能，因此针对低质数据进行过滤是一个很有必要的步骤。具体地，采取场景中对应的大模型对离线增广的所有数据进行前向预测，将得分低于某个阈值的增广图进行去除。以 ImageNet 分类数据集为例，使用大模型（PPLCNet）来对离线增广后数据进行前向推理，去除分类得分小于0.2的增广数据，低质数据示例如下：

<div align="center">
    <img alt="low_quality" src="https://user-images.githubusercontent.com/87074272/201034962-464811ab-bc2b-433f-912b-dbf48b45c5c1.png" width=400 hight=200>
</div>

可以看出，图一为采用 RandomErasing 的增广图，关键区域（目标区域）几乎全部被擦除，图二为采用 Gridmask 的增广图，关键区域也被掩盖，这些图像都大大增加了模型学习的难度，因此需要对这些低质数据进行过滤。

完成对离线增广数据的重复数据过滤和低质数据过滤后便可进行模型的训练。

### 4.4 PP-DataAug 实战
在完成环境搭建和数据准备后，可以进行数据扩充，以图像分类为例，运行以下命令进行扩充数据：

```bash
python tools/predict.py -c deploy/configs/ppdataaug_clas.yaml
```

`deploy/configs/ppdataaug_clas.yaml`配置文件解析:
首先是`DataGen`字段，该字段主要包含数据生成对应的参数

```
# 数据生成参数
DataGen:
  ops: # 数据增强类型
    - randaugment
    - random_erasing
    - gridmask
    - tia_distort
    - tia_stretch
    - tia_perspective
  ori_data_dir: "demo/clas_data" # 原始训练数据目录
  label_file: "demo/clas_data/train_list.txt" # 原始数据训练标签
  gen_label: "labels/test.txt" # 新生成的数据标签
  img_save_folder: "test" # 新生成的数据存储目录
  gen_ratio: 0 # 选择一定比例的原始数据进行生成
  gen_num: 5 # 指定每类增强生成的数量
  size: 224 # 图像resize的尺寸
```
其次是重复图像过滤字段`FeatureExtract`和`IndexProcess`，其中`FeatureExtract`字段主要包含特征提取模型对应的配置文件和重复图像过滤的阈值以及过滤后的标签保存路径，`IndexProcess`主要包含构建特征检索库的参数。
```
FeatureExtract:
  config: "deploy/configs/ppcv/feature_extract.yaml" # 特征提取模型对应的配置文件
  thresh: 0.5 # 重复图像过滤的阈值
  file_out: "tmp/rm_repeat.txt" # 重复图像过滤后的标签保存路径

IndexProcess:
  index_method: "HNSW32" # supported: HNSW32, IVF, Flat
  image_root: "./test" # 新生成的数据存储目录
  index_dir: "./augdata/all_aug" # 构建索引库的存储目录
  all_label_file:  *gen_label # 新生成的数据标签, 与DataGen输出标签路径一致
  index_operation: "new" # suported: "append", "remove", "new"
  delimiter: " " # 标签分隔符
  dist_type: "IP"
  embedding_size: 512
  batch_size: 32
  return_k: 5
  score_thres: 0.5
```
最后是低质图像过滤字段`BigModel`，该字段主要包含大模型的配置文件和低质过滤的阈值等参数。
```
BigModel:
  model_type: cls  # support(cls / ocr)
  config: "deploy/configs/ppcv/big_model_classification.yaml" # 大模型对应的配置文件
  batch_size: 8
  thresh: 0.1 # 低质过滤的阈值
  final_label: "high_socre_label.txt" # 最终过滤后的有效数据标签路径
```

如果需要适配自己的数据集，可以更改`DataGen`字段参数，主要涉及`ori_data_dir`，`label_file`这两个参数，分别对应原始数据集目录和原始数据集标签路径。

最终生成的有效数据路径在`DataGen.img_save_folder`字段下，也即默认的`test`目录，对应的数据标签为`BigModel.final_label`字段，也即默认的 `high_socre_label.txt`文件。

增广后的数据示例如下：

<div align="center">
    <img alt="eda_example" src="https://user-images.githubusercontent.com/87074272/201035419-5fa5ccae-4d37-4036-8b99-e1c472cc644c.png" width=800 hight=400>
</div>

全部增广标签位于`DataGen.gen_label`字段下，也即`labels/test.txt`文件，有效标签位于`high_socre_label.txt`文件，可以看出有效标签数据量小于全部增广标签，数据量越大，过滤掉的无效数据也会更多。


如需使用其他场景，更换对应的配置文件即可，不同场景对应配置文件如下：

| 场景    | 配置文件 |
| :--: | :--: |
| 图像分类 |[ppdataaug_clas.yaml](../../../deploy/configs/ppdataaug_clas.yaml)|
| 文本识别 img2img |[ppdataaug_ocr_img2img.yaml](../../../deploy/configs/ppdataaug_ocr_img2img.yaml)|
| 文本识别 text2img |[ppdataaug_ocr_text2img.yaml](../../../deploy/configs/ppdataaug_ocr_text2img.yaml)|
| 图像识别 |[ppdataaug_shitu.yaml](../../../deploy/configs/ppdataaug_shitu.yaml)|

<a name="5"></a>

## 5 扩充数据集使用

完成PP-DataAug数据增广后，便可以在自己的任务上优化模型指标。基于以下多个任务进行实验验证，下面分别介绍这些任务：

**文本识别**

文本识别任务是OCR的一个子任务，主要负责识别文本行的内容。基于[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/tree/release/2.6)中的[PP-OCRv3中文识别模型](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/configs/rec/PP-OCRv3/ch_PP-OCRv3_rec.yml)配置进行验证，数据集采用中英文数据集，约26W。在使用PP-DataAug进行扩充数据后，将增广数据与原始数据以1:1的比例混合，送入模型迭代训练。具体训练步骤可参考[文本识别训练](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/recognition.md#2-%E5%BC%80%E5%A7%8B%E8%AE%AD%E7%BB%83)。

**图像分类**

图像分类任务是计算机视觉中最基本的任务，主要对图像进行类别分类。基于[PaddleClas](https://github.com/PaddlePaddle/PaddleClas/tree/release/2.5)中的[PP-LCNet分类模型](https://github.com/PaddlePaddle/PaddleClas/blob/release/2.5/ppcls/configs/ImageNet/PPLCNet/PPLCNet_x1_0.yaml)配置进行验证，数据集采用ImageNet1K的子集，共计5W。在使用PP-DataAug进行扩充数据后，将增广数据与原始数据以1:1的比例混合，送入模型迭代训练。具体训练步骤可参考[图像分类训练](https://github.com/PaddlePaddle/PaddleClas/blob/develop/docs/zh_CN/training/single_label_classification/training.md#311-%E6%A8%A1%E5%9E%8B%E8%AE%AD%E7%BB%83)。

**识图任务**

识图任务是基于[PP-ShiTu系统](https://github.com/PaddlePaddle/PaddleClas/blob/release/2.5/docs/zh_CN/models/PP-ShiTu/README.md#pp-shitu-v2%E5%9B%BE%E5%83%8F%E8%AF%86%E5%88%AB%E7%B3%BB%E7%BB%9F)，它是一个实用轻量级通用图像识别系统，包含主体检测、特征提取、向量检索三个步骤。该任务主要进行特征提取阶段的模型训练，基于[PaddleClas](https://github.com/PaddlePaddle/PaddleClas/tree/release/2.5)中的[PP-LCNetv2识别模型](https://github.com/PaddlePaddle/PaddleClas/blob/release/2.5/ppcls/configs/GeneralRecognitionV2/GeneralRecognitionV2_PPLCNetV2_base.yaml)配置进行验证，数据集约10W。在使用PP-DataAug进行扩充数据后，将增广数据与原始数据以1:1的比例混合，送入模型迭代训练。具体训练步骤参考[特征提取训练](https://github.com/PaddlePaddle/PaddleClas/blob/develop/docs/zh_CN/training/PP-ShiTu/feature_extraction.md#52-%E6%A8%A1%E5%9E%8B%E8%AE%AD%E7%BB%83)。

**广告码图像过滤**

该任务也是实用轻量图像分类解决方案（PULC, Practical Ultra Lightweight Classification）的一个应用场景，主要是对一张图像中是否含有二维码、条形码等进行分类，基于[PaddleClas](https://github.com/PaddlePaddle/PaddleClas/tree/release/2.5)中的[PULC广告码图像过滤模型](https://github.com/PaddlePaddle/PaddleClas/blob/develop/ppcls/configs/PULC/code_exists/PPLCNet_x1_0.yaml)配置进行验证，数据集，约4W。在使用PP-DataAug进行扩充数据后，将增广数据与原始数据以1:1的比例混合，送入模型迭代训练。具体训练步骤参考[广告码图像过滤训练](https://github.com/PaddlePaddle/PaddleClas/blob/develop/docs/zh_CN/models/PULC/PULC_code_exists.md)

## 5.1 PP-DataAug实验效果
为了验证 PP-DataAug 离线增广数据的效果，在上述不同的场景下进行分别验证，包含文本识别、图像分类、识图任务、广告码图像过滤场景。为了消除数据量变化带来的影响，保证增广后的数据量和baseline数据量相同，会将原始数据进行复制作为baseline，具体实验结果如下表：

| 实验任务 | 模型 | 配置文件 | baseline精度 | 增广后精度 |
| :--: | :--: | :--: |:--: |:------: |
|  文本识别    | ch_PP-OCRv3_rec | [ch_PP-OCRv3_rec.yml](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/configs/rec/PP-OCRv3/ch_PP-OCRv3_rec.yml)  | 72.95%   |   74.15% (+1.20%)  |
|  图像分类    | PP-LCNet        | [PPLCNet_x1_0.yaml](https://github.com/PaddlePaddle/PaddleClas/blob/release/2.5/ppcls/configs/ImageNet/PPLCNet/PPLCNet_x1_0.yaml) | 78.23%   |   80.03% (+1.80%)  |
|  图像分类    | PP-HGNet        | [PPHGNet_small.yaml](https://github.com/PaddlePaddle/PaddleClas/blob/release/2.5/ppcls/configs/ImageNet/PPHGNet/PPHGNet_small.yaml) |   90.80%   |   91.33% (+0.53%)  |
|  识图任务    | PP-LCNetv2      | [GeneralRecognitionV2_PPLCNetV2_base.yaml](https://github.com/PaddlePaddle/PaddleClas/blob/release/2.5/ppcls/configs/GeneralRecognitionV2/GeneralRecognitionV2_PPLCNetV2_base.yaml) | 66.80%   |   67.70% (+0.90%)  |
| 广告码图像过滤| PP-LCNet        | [PPLCNet_x1_0.yaml](https://github.com/PaddlePaddle/PaddleClas/blob/develop/ppcls/configs/PULC/code_exists/PPLCNet_x1_0.yaml) |   94.40%   |   95.73% (+1.33%)  |

可以看出，使用 PP-DataAug 工具对数据进行增广后在不同场景中都有不同程度的效果提升。
