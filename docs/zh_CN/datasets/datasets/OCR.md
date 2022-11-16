## OCR数据集
这里整理了常用文本识别经典数据集，持续更新中，欢迎各位小伙伴贡献数据集～
- [通用中英文OCR数据集](#通用中英文OCR数据集)
- [手写中文OCR数据集](#手写中文OCR数据集)
- [关键信息提取](#关键信息提取)
- [版面分析](#版面分析)
- [表格识别](#表格识别)
- [垂类多语言](#垂类多语言)

具体如下：
<a name="通用中英文OCR数据集"></a>
### 1、通用中英文OCR数据集
- [ICDAR2019-LSVT](#ICDAR2019-LSVT)
- [ICDAR2017-RCTW-17](#ICDAR2017-RCTW-17)
- [中文街景文字识别](#中文街景文字识别)
- [中文文档文字识别](#中文文档文字识别)
- [ICDAR2019-ArT](#ICDAR2019-ArT)
- [电子印章数据集](#电子印章数据集)
 

<a name="ICDAR2019-LSVT"></a>
#### 1、ICDAR2019-LSVT
- **数据来源**：https://ai.baidu.com/broad/introduction?dataset=lsvt
- **数据简介**： 共45w中文街景图像，包含5w（2w测试+3w训练）全标注数据（文本坐标+文本内容），40w弱标注数据（仅文本内容），如下图所示：  
     <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/LSVT_1.jpg"><br>
    (a) 全标注数据  
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/LSVT_2.jpg"><br>
    (b) 弱标注数据  
- **下载地址**：https://ai.baidu.com/broad/download?dataset=lsvt
- **说明**：其中，test数据集的label目前没有开源，如要评估结果，可以去官网提交：https://rrc.cvc.uab.es/?ch=16

<a name="ICDAR2017-RCTW-17"></a>
#### 2、ICDAR2017-RCTW-17
- **数据来源**：https://rctw.vlrlab.net/
- **数据简介**：共包含12,000+图像，大部分图片是通过手机摄像头在野外采集的。有些是截图。这些图片展示了各种各样的场景，包括街景、海报、菜单、室内场景和手机应用程序的截图。

    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/rctw.jpg"><br>
- **下载地址**：https://rctw.vlrlab.net/dataset/

<a name="中文街景文字识别"></a>
#### 3、中文街景文字识别
- **数据来源**：https://aistudio.baidu.com/aistudio/competition/detail/8
- **数据简介**：ICDAR2019-LSVT行识别任务，共包括29万张图片，其中21万张图片作为训练集（带标注），8万张作为测试集（无标注）。数据集采自中国街景，并由街景图片中的文字行区域（例如店铺标牌、地标等等）截取出来而形成。所有图像都经过一些预处理，将文字区域利用仿射变化，等比映射为一张高为48像素的图片，如图所示：  
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/ch_street_rec_1.png"><br>
    (a) 标注：魅派集成吊顶  
     <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/ch_street_rec_2.png"><br> 
    (b) 标注：母婴用品连锁  
- **下载地址**
https://aistudio.baidu.com/aistudio/datasetdetail/8429

<a name="中文文档文字识别"></a>
#### 4、中文文档文字识别
- **数据来源**：https://github.com/YCG09/chinese_ocr  
- **数据简介**：  
    - 共约364万张图片，按照99:1划分成训练集和验证集。
    - 数据利用中文语料库（新闻 + 文言文），通过字体、大小、灰度、模糊、透视、拉伸等变化随机生成
    - 包含汉字、英文字母、数字和标点共5990个字符（字符集合：https://github.com/YCG09/chinese_ocr/blob/master/train/char_std_5990.txt ）
    - 每个样本固定10个字符，字符随机截取自语料库中的句子
    - 图片分辨率统一为280x32  
        <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/ch_doc1.jpg"><br> 
        <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/ch_doc3.jpg"><br> 
- **下载地址**：https://pan.baidu.com/s/1QkI7kjah8SPHwOQ40rS1Pw (密码：lu7m)

<a name="ICDAR2019-ArT"></a>
#### 5、ICDAR2019-ArT
- **数据来源**：https://ai.baidu.com/broad/introduction?dataset=art
- **数据简介**：共包含10,166张图像，训练集5603图，测试集4563图。由Total-Text、SCUT-CTW1500、Baidu Curved Scene Text (ICDAR2019-LSVT部分弯曲数据) 三部分组成，包含水平、多方向和弯曲等多种形状的文本。
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/ArT.jpg"><br>
- **下载地址**：https://ai.baidu.com/broad/download?dataset=art

<a name="电子印章数据集"></a>
#### 6、电子印章数据集
- **数据来源**：https://aistudio.baidu.com/aistudio/datasetdetail/154271/0
- **数据简介**：共包含10000张图像，训练集8000图，测试集2000图。数据集是用程序合成的，并不涉及隐私安全，主要用于印章弯曲文本的训练与检测。由开发者[jingsongliujing](https://github.com/jingsongliujing)贡献
- **下载地址**：https://aistudio.baidu.com/aistudio/datasetdetail/154271/0



<a name="手写OCR数据集"></a>
### 2、手写OCR数据集
这里整理了常用手写数据集，持续更新中，欢迎各位小伙伴贡献数据集～
- [中科院自动化研究所-手写中文数据集](#中科院自动化研究所-手写中文数据集)
- [NIST手写单字数据集-英文](#NIST手写单字数据集-英文)

<a name="中科院自动化研究所-手写中文数据集"></a>
#### 中科院自动化研究所-手写中文数据集
- **数据来源**：http://www.nlpr.ia.ac.cn/databases/handwriting/Download.html
- **数据简介**：
    * 包含在线和离线两类手写数据，`HWDB1.0~1.2`总共有3895135个手写单字样本，分属7356类（7185个汉字和171个英文字母、数字、符号）；`HWDB2.0~2.2`总共有5091页图像，分割为52230个文本行和1349414个文字。所有文字和文本样本均存为灰度图像。部分单字样本图片如下所示。

        <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/CASIA_0.jpg">

- **下载地址**：http://www.nlpr.ia.ac.cn/databases/handwriting/Download.html
- **使用建议**：数据为单字，白色背景，可以大量合成文字行进行训练。白色背景可以处理成透明状态，方便添加各种背景。对于需要语义的情况，建议从真实语料出发，抽取单字组成文字行


<a name="NIST手写单字数据集-英文"></a>
#### NIST手写单字数据集-英文(NIST Handprinted Forms and Characters Database)

- **数据来源**: [https://www.nist.gov/srd/nist-special-database-19](https://www.nist.gov/srd/nist-special-database-19)

- **数据简介**: NIST19数据集适用于手写文档和字符识别的模型训练，从3600位作者的手写样本表格中提取得到，总共包含81万张字符图片。其中9张图片示例如下。

    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/nist_demo.png">



- **下载地址**: [https://www.nist.gov/srd/nist-special-database-19](https://www.nist.gov/srd/nist-special-database-19)


<a name="关键信息抽取数据集"></a>
### 3、关键信息抽取数据集

这里整理了常见的关键信息抽取数据集，持续更新中，欢迎各位小伙伴贡献数据集～

- [FUNSD数据集](#funsd)
- [XFUND数据集](#xfund)
- [wildreceipt数据集](#wildreceipt)

<a name="funsd"></a>

#### 1. FUNSD数据集

- **数据来源**：https://guillaumejaume.github.io/FUNSD/
- **数据简介**：FUNSD数据集是一个用于表单理解的数据集，它包含199张真实的、完全标注的扫描版图片，类型包括市场报告、广告以及学术报告等，并分为149张训练集以及50张测试集。FUNSD数据集适用于多种类型的DocVQA任务，如字段级实体分类、字段级实体连接等。部分图像以及标注框可视化如下所示:
<div align="center">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/funsd_demo/gt_train_00040534.jpg" width="500">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/funsd_demo/gt_train_00070353.jpg" width="500">
</div>
    图中，橙色区域代表`header`，淡蓝色区域代表`question`, 绿色区域表`answer`，粉红色代区域表`other`。

- **下载地址**：https://guillaumejaume.github.io/FUNSD/download/

<a name="xfund"></a>

#### 2. XFUND数据集
- **数据来源**：https://github.com/doc-analysis/XFUND
- **数据简介**：XFUND是一个多语种表单理解数据集，它包含7种不同语种的表单数据，并且全部用人工进行了键-值对形式的标注。其中每个语种的数据都包含了199张表单数据，并分为149张训练集以及50张测试集。部分图像以及标注框可视化如下所示:

<div align="center">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/xfund_demo/gt_zh_train_0.jpg" width="500">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/xfund_demo/gt_zh_train_1.jpg" width="500">
</div>

- **下载地址**：https://github.com/doc-analysis/XFUND/releases/tag/v1.0


<a name="wildreceipt"></a>

#### 3. wildreceipt数据集

- **数据来源**：https://arxiv.org/abs/2103.14470
- **数据简介**：wildreceipt数据集是英文发票数据集，包含26个类别（此处类别体系包含`Ignore`类别），共标注了50000个文本框。其中训练集包含1267张图片，测试集包含472张图片。部分图像以及标注框可视化如下所示:

<div align="center">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/wildreceipt_demo/2769.jpeg" width="500">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/wildreceipt_demo/1bbe854b8817dedb8585e0732089fd1f752d2cec.jpeg" width="500">
</div>

**注：** 这里对于类别为`Ignore`或者`Others`的文本，没有进行可视化。

- **下载地址**：
    - 原始数据下载地址：[链接](https://download.openmmlab.com/mmocr/data/wildreceipt.tar)
    - 数据格式转换后适配于PaddleOCR训练的数据下载地址：[链接](https://paddleocr.bj.bcebos.com/ppstructure/dataset/wildreceipt.tar)


<a name="版面分析数据集"></a>
### 4、版面分析数据集

这里整理了常用版面分析数据集，持续更新中，欢迎各位小伙伴贡献数据集～
- [publaynet数据集](#publaynet)
- [CDLA数据集](#CDLA)
- [TableBank数据集](#TableBank)

版面分析数据集多为目标检测数据集，除了开源数据，用户还可使用合成工具自行合成，如[labelme](https://github.com/wkentaro/labelme)等。


<a name="publaynet"></a>

#### 1、publaynet数据集
- **数据来源**：https://github.com/ibm-aur-nlp/PubLayNet
- **数据简介**：publaynet数据集的训练集合中包含35万张图像，验证集合中包含1.1万张图像。总共包含5个类别，分别是： `text, title, list, table, figure`。部分图像以及标注框可视化如下所示。

<div align="center">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/publaynet_demo/gt_PMC3724501_00006.jpg" width="500">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/publaynet_demo/gt_PMC5086060_00002.jpg" width="500">
</div>

- **下载地址**：https://developer.ibm.com/exchanges/data/all/publaynet/
- **说明**：使用该数据集时，需要遵守[CDLA-Permissive](https://cdla.io/permissive-1-0/)协议。


<a name="CDLA"></a>

#### 2、CDLA数据集
- **数据来源**：https://github.com/buptlihang/CDLA
- **数据简介**：CDLA据集的训练集合中包含5000张图像，验证集合中包含1000张图像。总共包含10个类别，分别是： `Text, Title, Figure, Figure caption, Table, Table caption, Header, Footer, Reference, Equation`。部分图像以及标注框可视化如下所示。

<div align="center">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/CDLA_demo/val_0633.jpg" width="500">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/CDLA_demo/val_0941.jpg" width="500">
</div>

- **下载地址**：https://github.com/buptlihang/CDLA
- **说明**：基于[PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection/tree/develop)套件，在该数据集上训练目标检测模型时，在转换label时，需要将`label.txt`中的`__ignore__`与`_background_`去除。


<a name="TableBank"></a>

#### 3、TableBank数据集
- **数据来源**：https://doc-analysis.github.io/tablebank-page/index.html
- **数据简介**：TableBank数据集包含Latex（训练集187199张，验证集7265张，测试集5719张）与Word（训练集73383张，验证集2735张，测试集2281张）两种类别的文档。仅包含`Table` 1个类别。部分图像以及标注框可视化如下所示。

<div align="center">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/tablebank_demo/004.png" height="700">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/tablebank_demo/005.png" height="700">
</div>

- **下载地址**：https://doc-analysis.github.io/tablebank-page/index.html
- **说明**：使用该数据集时，需要遵守[Apache-2.0](https://github.com/doc-analysis/TableBank/blob/master/LICENSE)协议。


<a name="表格识别数据集"></a>
### 5、表格识别数据集

- [数据集汇总](#数据集汇总)
- [1. PubTabNet数据集](#1-pubtabnet数据集)
- [2. 好未来表格识别竞赛数据集](#2-好未来表格识别竞赛数据集)
- [3. 好未来表格识别竞赛数据集](#2-WTW中文场景表格数据集)

这里整理了常用表格识别数据集，持续更新中，欢迎各位小伙伴贡献数据集～

#### 数据集汇总

| 数据集名称 |图片下载地址| PPOCR标注下载地址 |
|---|---|---|
| PubTabNet |https://github.com/ibm-aur-nlp/PubTabNet| jsonl格式，可直接用[pubtab_dataset.py](../../../ppocr/data/pubtab_dataset.py)加载 |
| 好未来表格识别竞赛数据集 |https://ai.100tal.com/dataset| jsonl格式，可直接用[pubtab_dataset.py](../../../ppocr/data/pubtab_dataset.py)加载 |
| WTW中文场景表格数据集 |https://github.com/wangwen-whu/WTW-Dataset| 需要进行转换后才能用[pubtab_dataset.py](../../../ppocr/data/pubtab_dataset.py)加载 |

#### 1. PubTabNet数据集
- **数据简介**：PubTabNet数据集的训练集合中包含50万张图像，验证集合中包含0.9万张图像。部分图像可视化如下所示。


<div align="center">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/table_PubTabNet_demo/PMC524509_007_00.png" width="500">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/table_PubTabNet_demo/PMC535543_007_01.png" width="500">
</div>

- **说明**：使用该数据集时，需要遵守[CDLA-Permissive](https://cdla.io/permissive-1-0/)协议。

#### 2. 好未来表格识别竞赛数据集
- **数据简介**：好未来表格识别竞赛数据集的训练集合中包含1.6万张图像。验证集未给出可训练的标注。

<div align="center">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/table_tal_demo/1.jpg" width="500">
    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/table_tal_demo/2.jpg" width="500">
</div>

#### 3. WTW中文场景表格数据集
- **数据简介**：WTW中文场景表格数据集包含表格检测和表格数据两部分数据，数据集中同时包含扫描和拍照两张场景的图像。

https://github.com/wangwen-whu/WTW-Dataset/blob/main/demo/20210816_210413.gif

<div align="center">
    <img src="https://raw.githubusercontent.com/wangwen-whu/WTW-Dataset/main/demo/20210816_210413.gif" width="500">
</div>

<a name="垂类多语言OCR数据集"></a>
#### 6、垂类多语言OCR数据集
这里整理了常用垂类和多语言OCR数据集，持续更新中，欢迎各位小伙伴贡献数据集～
- [中国城市车牌数据集](#中国城市车牌数据集)
- [银行信用卡数据集](#银行信用卡数据集)
- [验证码数据集-Captcha](#验证码数据集-Captcha)
- [多语言数据集](#多语言数据集)


<a name="中国城市车牌数据集"></a>
#### 中国城市车牌数据集

- **数据来源**：[https://github.com/detectRecog/CCPD](https://github.com/detectRecog/CCPD)

- **数据简介**: 包含超过25万张中国城市车牌图片及车牌检测、识别信息的标注。包含以下几种不同场景中的车牌图片信息。
    * CCPD-Base: 通用车牌图片
    * CCPD-DB: 车牌区域亮度较亮、较暗或者不均匀
    * CCPD-FN: 车牌离摄像头拍摄位置相对更远或者更近
    * CCPD-Rotate: 车牌包含旋转（水平20\~50度，竖直-10\~10度）
    * CCPD-Tilt: 车牌包含旋转（水平15\~45度，竖直15\~45度）
    * CCPD-Blur: 车牌包含由于摄像机镜头抖动导致的模糊情况
    * CCPD-Weather: 车牌在雨天、雪天或者雾天拍摄得到
    * CCPD-Challenge: 至今在车牌检测识别任务中最有挑战性的一些图片
    * CCPD-NP: 没有安装车牌的新车图片。

    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/ccpd_demo.png"><br>


- **下载地址**
    * 百度云下载地址(提取码是hm0U): [https://pan.baidu.com/s/1i5AOjAbtkwb17Zy-NQGqkw](https://pan.baidu.com/s/1i5AOjAbtkwb17Zy-NQGqkw)
    * Google drive下载地址：[https://drive.google.com/file/d/1rdEsCUcIUaYOVRkx5IMTRNA7PcGMmSgc/view](https://drive.google.com/file/d/1rdEsCUcIUaYOVRkx5IMTRNA7PcGMmSgc/view)


<a name="银行信用卡数据集"></a>
#### 银行信用卡数据集

- **数据来源**: [https://www.kesci.com/home/dataset/5954cf1372ead054a5e25870](https://www.kesci.com/home/dataset/5954cf1372ead054a5e25870)

- **数据简介**: 训练数据共提供了三类数据
    * 1.招行样卡数据： 包括卡面图片数据及标注数据，总共618张图片
    * 2.单字符数据： 包括图片及标注数据，总共37张图片。
    * 3.仅包含其他银行卡面，不具有更细致的信息，总共50张图片。

    * demo图片展示如下，标注信息存储在excel表格中，下面的demo图片标注为
        * 前8位卡号：62257583
        * 卡片种类：本行卡
        * 有效期结束：07/41
        * 卡用户拼音：MICHAEL

    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/cmb_demo.jpg"><br>

- **下载地址**: [https://cdn.kesci.com/cmb2017-2.zip](https://cdn.kesci.com/cmb2017-2.zip)



<a name="验证码数据集-Captcha"></a>
#### 验证码数据集-Captcha

- **数据来源**: [https://github.com/lepture/captcha](https://github.com/lepture/captcha)

- **数据简介**: 这是一个数据合成的工具包，可以根据输入的文本，输出验证码图片，使用该工具包生成几张demo图片如下。

    <img src="https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/doc/datasets/captcha_demo.png">

- **下载地址**: 该数据集是生成得到，无下载地址。



<a name="多语言数据集"></a>
## 多语言数据集(Multi-lingual scene text detection and recognition)

- **数据来源**: [https://rrc.cvc.uab.es/?ch=15&com=downloads](https://rrc.cvc.uab.es/?ch=15&com=downloads)

- **数据简介**: 多语言检测数据集MLT同时包含了语种识别和检测任务。
    * 在检测任务中，训练集包含10000张图片，共有10种语言，每种语言包含1000张训练图片。测试集包含10000张图片。
    * 在识别任务中，训练集包含111998个样本。


- **下载地址**: 训练集较大，分2部分下载，需要在网站上注册之后才能下载：
[https://rrc.cvc.uab.es/?ch=15&com=downloads](https://rrc.cvc.uab.es/?ch=15&com=downloads)
