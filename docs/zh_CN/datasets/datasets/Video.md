## 动作识别经典数据集
这里整理了常用视频理解领域数据集，持续更新中，欢迎各位小伙伴贡献数据集～
- [Kinetics-400](#Kinetics-400)
- [UCF101](#UCF101)
- [YouTube-8M](#3、YouTube-8M)
- [AVA](#4、AVA)
 

<a name="Kinetics-400"></a>
## 1、Kinetics-400
- [数据集介绍](#数据集介绍)
- [下载video数据](#下载video数据)
- [提取frames数据](#提取frames数据)

---


- **数据集介绍**

    Kinetics-400是视频领域benchmark常用数据集，详细介绍可以参考其官方网站[Kinetics](https://deepmind.com/research/open-source/kinetics)。下载方式可参考官方地址[ActivityNet](https://github.com/activitynet/ActivityNet/tree/master/Crawler/Kinetics)，使用其提供的下载脚本下载数据集。


- **下载video数据**

    考虑到K400数据集下载困难的问题，我们提供了两种下载方式： (1) 百度网盘下载 (2) 脚本下载

- **百度网盘下载**

    网盘链接：https://pan.baidu.com/s/1S_CGBjWOUAuxL_cCX5kMPg
提取码：ppvi

- **脚本下载**

    - 下载训练集链接列表文件[train_link.list](https://ai-rank.bj.bcebos.com/Kinetics400/train_link.list)和验证集链接列表文件[val_link.list](https://ai-rank.bj.bcebos.com/Kinetics400/val_link.list)。

    编写下载脚本`download.sh`如下:
```bash
file=$1

while read line 
do
  wget "$line"
done <$file
```

下载训练集命令：
```bash
bash download.sh train_link.list
```

下载验证集命令:
```bash
bash download.sh val_link.list
```

---

|类别 | 数据条数  | list文件 |
| :------: | :----------: | :----: |
|训练集 | 234619  |  [train.list](https://videotag.bj.bcebos.com/PaddleVideo/Data/Kinetic400/train.list)|
|验证集 | 19761 |  [val.list](https://videotag.bj.bcebos.com/PaddleVideo/Data/Kinetic400/val.list)|

- 下载后自行解压，并将数据路径添加到相应的list文件中。

- 由于部分视频原始链接失效，数据有部分缺失，全部文件大概需要135G左右的存储空间，PaddleVideo使用的也是这份数据。

> 此份数据仅限于学术研究，若对您有帮助，欢迎给[项目](https://github.com/PaddlePaddle/PaddleVideo)star~


- **提取frames数据**
为了加速网络的训练过程，我们首先对视频文件（K400视频文件为mp4格式）提取帧 (frames)。相对于直接通过视频文件进行网络训练的方式，frames的方式能够极大加快网络训练的速度。

输入如下命令，即可提取K400视频文件的frames

```python
python extract_rawframes.py ./videos/ ./rawframes/ --level 2 --ext mp4
```

视频文件frames提取完成后，会存储在指定的`./rawframes`路径下，大小约为2T左右。

|类别 | 数据条数  | list文件 |
| :------: | :----------: | :----: |
|训练集 | 234619  |  [train_frames.list](https://videotag.bj.bcebos.com/PaddleVideo/Data/Kinetic400/train_frames.list)|
|验证集 | 19761 |  [val_frames.list](https://videotag.bj.bcebos.com/PaddleVideo/Data/Kinetic400/val_frames.list)|

<a name="UCF101"></a>
## 2、UCF101
- **UCF101数据准备**

    UCF101数据的相关准备。主要包括UCF101的video文件下载，video文件提取frames，以及生成文件的路径list。

---
- **数据下载**
    UCF101数据的详细信息可以参考网站[UCF101](https://www.crcv.ucf.edu/data/UCF101.php)。 为了方便使用，PaddleVideo提供了UCF101数据的annotations文件和videos文件的下载脚本。

- **下载annotations文件**
首先，请确保在[data/ucf101/ 目录](https://github.com/PaddlePaddle/PaddleVideo/tree/develop/data/ucf101)下，输入如下UCF101数据集的标注文件的命令。
```shell
bash download_annotations.sh
```

- **下载UCF101的视频文件**
同样需要确保在[data/ucf101/ 目录](https://github.com/PaddlePaddle/PaddleVideo/tree/develop/data/ucf101)下，输入下述命令下载视频文件

```shell
bash download_videos.sh
```
- 运行该命令需要安装unrar解压工具，可使用pip方式安装。

- 下载完成后视频文件会存储在[data/ucf101/videos/ 文件夹](https://github.com/PaddlePaddle/PaddleVideo/tree/develop/data/ucf101)下，视频文件大小为6.8G。

---
- **提取视频文件的frames**
为了加速网络的训练过程，我们首先对视频文件（ucf101视频文件为avi格式）提取帧 (frames)。相对于直接通过视频文件进行网络训练的方式，frames的方式能够加快网络训练的速度。

直接输入如下命令，即可提取ucf101视频文件的frames

``` python
python extract_rawframes.py ./videos/ ./rawframes/ --level 2 --ext avi
```

视频文件frames提取完成后，会存储在`./rawframes`文件夹下，大小为56G。

---
- **生成frames文件和视频文件的路径list**
生成视频文件的路径list，输入如下命令

```python
python build_ucf101_file_list.py videos/ --level 2 --format videos --out_list_path ./
```
生成frames文件的路径list，输入如下命令：
```python
python build_ucf101_file_list.py rawframes/ --level 2 --format rawframes --out_list_path ./
```

**参数说明**

`videos/` 或者 `rawframes/` ： 表示视频或者frames文件的存储路径

`--level 2` ： 表示文件的存储结构

`--format`： 表示是针对视频还是frames生成路径list

`--out_list_path `： 表示生成的路径list文件存储位置


- **以上步骤完成后，文件组织形式如下所示**

```
├── data
|   ├── dataset
|   │   ├── ucf101
|   │   │   ├── ucf101_{train,val}_split_{1,2,3}_rawframes.txt
|   │   │   ├── ucf101_{train,val}_split_{1,2,3}_videos.txt
|   │   │   ├── annotations
|   │   │   ├── videos
|   │   │   │   ├── ApplyEyeMakeup
|   │   │   │   │   ├── v_ApplyEyeMakeup_g01_c01.avi
|   │   │   │   │   └── ...
|   │   │   │   ├── YoYo
|   │   │   │   │   ├── v_YoYo_g25_c05.avi
|   │   │   │   │   └── ...
|   │   │   │   └── ...
|   │   │   ├── rawframes
|   │   │   │   ├── ApplyEyeMakeup
|   │   │   │   │   ├── v_ApplyEyeMakeup_g01_c01
|   │   │   │   │   │   ├── img_00001.jpg
|   │   │   │   │   │   ├── img_00002.jpg
|   │   │   │   │   │   ├── ...
|   │   │   │   │   │   ├── flow_x_00001.jpg
|   │   │   │   │   │   ├── flow_x_00002.jpg
|   │   │   │   │   │   ├── ...
|   │   │   │   │   │   ├── flow_y_00001.jpg
|   │   │   │   │   │   ├── flow_y_00002.jpg
|   │   │   │   ├── ...
|   │   │   │   ├── YoYo
|   │   │   │   │   ├── v_YoYo_g01_c01
|   │   │   │   │   ├── ...
|   │   │   │   │   ├── v_YoYo_g25_c05

```


<a name="YouTube-8M"></a>
## 3、YouTube-8M

- **数据准备**

    - [数据集简介](#数据集简介)
    - [数据集下载](#数据集下载)
    - [数据格式转化](#数据格式转化)


- **数据集简介**

    YouTube-8M 是一个大规模视频分类数据集，包含800多万个视频url，标签体系涵盖3800多种知识图谱实体，1个视频对应多个标签(平均3-4个)，使用机器进行标注。

    **每个视频的长度在120s到500s之间
    由于视频数据量太大，因此预先使用图像分类模型提取了frame-level的特征，并使用PCA对特征进行了降维处理得到多帧1024维的特征，类似地用音频模型处理得到多帧128维的音频特征。**
    > 这里用到的是YouTube-8M 2018年更新之后的数据集（May 2018 version (current): 6.1M videos, 3862 classes, 3.0 labels/video, 2.6B audio-visual features）。  
  

- **数据集下载**

    1. 新建存放特征的目录（以PaddleVideo目录下为例）
    ```bash
    cd data/yt8m
    mkdir frame
    cd frame
    ```
    2. 下载训练、验证集到frame文件夹中
    ```bash
    curl data.yt8m.org/download.py | partition=2/frame/train mirror=asia python
    curl data.yt8m.org/download.py | partition=2/frame/validate mirror=asia python
    ```
    下载过程如图所示
    ![image](https://user-images.githubusercontent.com/23737287/140709613-1e2d6ec0-a82e-474d-b220-7803065b0153.png)

    数据下载完成后，将会得到3844个训练数据文件和3844个验证数据文件（TFRecord格式）


- **数据格式转化**
    1. 安装tensorflow-gpu用于读入tfrecord数据
    ```bash
    python3.7 -m pip install tensorflow-gpu==1.14.0
    ```
    2. 将下载的TFRecord文件转化为pickle文件以便PaddlePaddle使用
    ```bash
    cd .. # 从frame目录回到yt8m目录
    python3.7 tf2pkl.py ./frame ./pkl_frame/ # 将frame文件夹下的train*.tfrecord和validate*.tfrecord转化为pkl格式
    ```
    3. 生成单个pkl文件路径集合，并根据此文件将pkl拆分为多个小pkl文件，并生成最终需要的拆分pkl文件路径
    ```bash
    ls pkl_frame/train*.pkl > train.list # 将train*.pkl的路径写入train.list
    ls pkl_frame/validate*.pkl > val.list # 将validate*.pkl的路径写入val.list

    python3.7 split_yt8m.py train.list # 拆分每个train*.pkl变成多个train*_split*.pkl
    python3.7 split_yt8m.py val.list # 拆分每个validate*.pkl变成多个validate*_split*.pkl
    
    ls pkl_frame/train*_split*.pkl > train.list # 将train*_split*.pkl的路径重新写入train.list
    ls pkl_frame/validate*_split*.pkl > val.list # 将validate*_split*.pkl的路径重新写入val.list
    ```

<a name="AVA"></a>
## 4、AVA
### AVA数据准备
此文档主要介绍AVA数据集的相关准备流程。主要介绍 AVA数据集的视频文件下载，标注文件准备，视频文件切分视频文件提取帧数据，以及拉取提名文件等。以[PaddleVideo](https://github.com/PaddlePaddle/PaddleVideo)为例在开始之前，请把当前工作目录设定在 `$PaddleVideo/data/ava/shell`

---

### 1.  视频数据下载
想要获取更多有关AVA数据集的信息，您可以访问其官方网站[AVA](https://research.google.com/ava/index.html).
至于数据集下载，您可以参看考[AVA Download](https://github.com/cvdfoundation/ava-dataset) ，该Repo详细介绍了AVA视频数据的下载方法.
我们也提供了视频文件的下载脚本：

```shell
bash download_videos.sh
```

为了方便用户，我们将视频文件以zip包的形式上传到百度网盘，您可以直接进行下载 [Link]() <sup>coming soon</sup>.


**注意: 您自己下载的视频文件应当被放置在`data/ava/videos`文件夹下**  

---
### 2.准备标注文件

接下来，您可以使用下面的脚本来准备标注文件

```shell
bash download_annotations.sh
```

该脚本会默认下载`ava_v2.1.zip`，如果您想下载`v2.2`,您可以使用：

```shell
VERSION=2.2 bash download_annotations.sh
```

**注意：事实上，我们也同样在百度网盘中提供了该标注文件，所以您无需自己下载** 

---
### 3. 切分视频文件

以帧率30fps,切分视频文件从第15分钟到第30分钟

```shell
bash cut_videos.sh
```
---

### 4. 提取RGB帧

您可以通过以下的脚本使用`ffmpeg`来提取RGB帧.

```shell
bash extract_rgb_frames.sh
```

---

### 5.拉取提名文件

这个脚本来自于Facbook研究院[Long-Term Feature Banks](https://github.com/facebookresearch/video-long-term-feature-banks). 
您可以使用如下的脚本来获取预计算的提名文件列表。

```shell
bash fetch_ava_proposals.sh
```

---
### 6.目录结构

经过整个AVA数据处理流程后，您可以获得AVA的帧文件，视频文件和标注文件

整个项目(AVA)的目录结构如下所示：

```
PaddleVideo
├── configs
├── paddlevideo
├── docs
├── tools
├── data
│   ├── ava
│   │   ├── annotations
│   │   |   ├── ava_dense_proposals_train.FAIR.recall_93.9.pkl
│   │   |   ├── ava_dense_proposals_val.FAIR.recall_93.9.pkl
│   │   |   ├── ava_dense_proposals_test.FAIR.recall_93.9.pkl
│   │   |   ├── ava_train_v2.1.csv
│   │   |   ├── ava_val_v2.1.csv
│   │   |   ├── ava_train_excluded_timestamps_v2.1.csv
│   │   |   ├── ava_val_excluded_timestamps_v2.1.csv
│   │   |   ├── ava_action_list_v2.1_for_activitynet_2018.pbtxt
│   │   ├── videos
│   │   │   ├── 053oq2xB3oU.mkv
│   │   │   ├── 0f39OWEqJ24.mp4
│   │   │   ├── ...
│   │   ├── videos_15min
│   │   │   ├── 053oq2xB3oU.mkv
│   │   │   ├── 0f39OWEqJ24.mp4
│   │   │   ├── ...
│   │   ├── rawframes
│   │   │   ├── 053oq2xB3oU
|   │   │   │   ├── img_00001.jpg
|   │   │   │   ├── img_00002.jpg
|   │   │   │   ├── ...
```
