# PP-dataClean快速开始

------


## 目录


- [1. 环境配置](#1)
  - [1.1 安装PaddlePaddle](#11)
  - [1.2 安装EasyData whl包](#12)
- [2. 便捷使用](#2)
  - [2.1 命令行使用](#21)
      - [2.1.1 图像方向矫正模型](#211)
      - [2.1.2 模糊图像过滤模型](#212)
      - [2.1.3 广告码图像过滤模型](#232)
  - [2.2 Python脚本使用](#22)
- [3.小结](#3)


<a name="1"></a>
## 1. 安装

<a name="11"></a>
### 1.1 安装PaddlePaddle

- 您的机器安装的是CUDA9或CUDA10，请运行以下命令安装

  ```bash
  python3 -m pip install paddlepaddle-gpu -i https://mirror.baidu.com/pypi/simple
  ```

- 您的机器是CPU，请运行以下命令安装

  ```bash
  python3 -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
  ```

更多的版本需求，请参照[飞桨官网安装文档](https://www.paddlepaddle.org.cn/install/quick)中的说明进行操作。

<a name="12"></a>
### 1.2 安装 EasyData whl 包

您可以从 PyPi 安装我们最新的发布版本，也可以获取 EasyData 项目代码本地安装。

<a name="121"></a>
### 1.2.1 PyPi

直接通过 pip 工具从 PyPi 等源进行安装，命令如下：

```bash
pip install easy-data
```

<a name="122"></a>
### 1.2.2 本地安装

本地安装需要先获取 EasyData 项目代码，命令如下：

```bash
git clone https://github.com/PaddlePaddle/EasyData.git
```

然后进入 EasyData 项目根目录并安装，命令如下：

```bash
cd EasyData
python setup.py install
```

<a name="2"></a>
## 2. 便捷使用
<a name="21"></a>
### 2.1 命令行使用

EasyData 提供了测试图片用于验证，点击[这里](https://paddleclas.bj.bcebos.com/data/PULC/easydata_demo_imgs.tar)下载并解压，然后在终端中切换到相应目录：

```
cd ./easydata_demo_imgs/
```

如果不使用提供的测试图片，可以将下方`--input`参数替换为相应的测试图片路径。

<a name="211"></a>

#### 2.1.1 图像方向矫正模型

EasyData 提供了图像方向矫正模型，通过下方代码即可快速体验，其中参数 `--model image_orientation` 指定了所使用的模型；参数 `--input ./image_orientation/1.jpg` 指定了待预测图像文件路径；参数 `--device cpu` 指定了使用 CPU 进行预测，同样可以通过 `--device gpu` 指定使用 GPU 进行预测。

```bash
easydata --model image_orientation --input ./image_orientation/1.jpg --device cpu
```

预测结果以 dict 格式输出，预测结果包含了预测图像文件路径、分类结果、score 和分类结果对应的标签：

```bash
{'filename': '/paddle/data/easydata_demo_imgs/image_orientation/1.jpg', 'class_ids': 1, 'scores': 0.9346007, 'label_names': '90°'}
```

预测结果中，类别 id 与分类标签的映射关系如下：

* 0: 0°，表示图像方向为正，未进行旋转；
* 1: 90°，表示该图像逆时针旋转了90度；
* 2: 180°，表示该图像逆时针旋转了180度；
* 3: 270°，表示该图像逆时针旋转了270度；

另外，EasyData 同样支持对多张图像进行预测，仅需通过参数 `--input` 指定包含预测图像的目录即可：

```bash
easydata --model image_orientation --input ./image_orientation/ --device cpu
```

此时，会将每个图像的预测结果依次打印：

```bash
{'filename': '/paddle/data/easydata_demo_imgs/image_orientation/2.jpg', 'class_ids': 2, 'scores': 0.9217471, 'label_names': '180°'}
{'filename': '/paddle/data/easydata_demo_imgs/image_orientation/3.jpg', 'class_ids': 3, 'scores': 0.9218502, 'label_names': '270°'}
{'filename': '/paddle/data/easydata_demo_imgs/image_orientation/1.jpg', 'class_ids': 1, 'scores': 0.9346007, 'label_names': '90°'}
{'filename': '/paddle/data/easydata_demo_imgs/image_orientation/0.jpg', 'class_ids': 0, 'scores': 0.9267141, 'label_names': '0°'}
```

对于图像方向矫正模型，还可以通过参数 `--thresh` 设置 score 的阈值。设置阈值则意味着，当 top1 score > thresh 时，预测值为 top1 对应类别，否则预测值为默认类别 0，即表示 0°。而阈值默认值为0，表示以 top1 score 结果作为预测值。如将阈值设置为 0.93，命令如下所示：

```bash
easydata --model image_orientation --input ./image_orientation/ --device cpu --thresh 0.93
```

上述命令的运行结果如下所示：

```bash
{'filename': '/paddle/data/easydata_demo_imgs/image_orientation/3.jpg', 'class_ids': 0, 'scores': 0.023812257, 'label_names': '0°'}
{'filename': '/paddle/data/easydata_demo_imgs/image_orientation/2.jpg', 'class_ids': 0, 'scores': 0.02494335, 'label_names': '0°'}
{'filename': '/paddle/data/easydata_demo_imgs/image_orientation/0.jpg', 'class_ids': 0, 'scores': 0.92671424, 'label_names': '0°'}
{'filename': '/paddle/data/easydata_demo_imgs/image_orientation/1.jpg', 'class_ids': 1, 'scores': 0.93460053, 'label_names': '90°'}
```

<a name="212"></a>

#### 2.1.2 模糊图像过滤模型

EasyData 提供了模糊图像过滤模型，通过下方代码即可快速体验：

``` bash
easydata --model clarity_assessment --input ./clarity_assessment/ --device cpu
```

上述命令的预测结果如下所示：

```text
{'filename': '/paddle/data/easydata_demo_imgs/clarity_assessment/clarity_demo.jpg', 'class_ids': [0], 'scores': [0.89864], 'label_names': ['clarity']}
{'filename': '/paddle/data/easydata_demo_imgs/clarity_assessment/blured_demo.jpg', 'class_ids': [1], 'scores': [0.97749], 'label_names': ['blured']}
```

预测结果中，类别 id 与分类标签的映射关系如下：

* 0: clarity，表示该图像为清晰图像；
* 1: blured，表示该图像为模糊图像。

<a name="213"></a>

#### 2.1.3 广告码图像过滤模型

EasyData 提供了广告码图像过滤模型，支持识别图像中是否包含条形码、二维码、微信小程序码，通过下方代码即可快速体验：

``` bash
easydata --model code_exists --input ./code_exists/ --device cpu
```

上述命令的预测结果如下所示：

```text
{'filename': '/paddle/data/easydata_demo_imgs/code_exists/no_code_demo.jpg', 'class_ids': [0], 'scores': [0.996], 'label_names': ['no code']}
{'filename': '/paddle/data/easydata_demo_imgs/code_exists/contains_code_demo.jpg', 'class_ids': [1], 'scores': [1.0], 'label_names': ['contains code']}
```

预测结果中，类别 id 与分类标签的映射关系如下：

* 0: no code，表示该图像中不存在广告码；
* 1: contains code，表示该图像中存在广告码。

<a name="22"></a>

### 2.2 Python脚本使用

EasyData 同样可以通过 whl 包的形式集成到 Python 脚本中。在 Python 脚本中使用时，只需 import 导入 EasyData 包，并实例化 EasyData 对象即可进行预测。以图像方向矫正模型为例，使用方法为：

```python
from easydata import EasyData
model = EasyData(model="image_orientation", device="cpu", return_res=True, print_res=False)
results = model.predict("./image_orientation/")
print(results)
```

结果是一个list，其中元素为 dict 类型，包含了预测图像文件路径、预测结果id、score 和预测类别名：

```bash
[{'filename': '/paddle/data/easydata_demo_imgs/image_orientation/2.jpg', 'class_ids': 2, 'scores': 0.92174697, 'label_names': '180°'}, {'filename': '/paddle/data/easydata_demo_imgs/image_orientation/3.jpg', 'class_ids': 3, 'scores': 0.9218502, 'label_names': '270°'}, {'filename': '/paddle/data/easydata_demo_imgs/image_orientation/1.jpg', 'class_ids': 1, 'scores': 0.93460053, 'label_names': '90°'}, {'filename': '/paddle/data/easydata_demo_imgs/image_orientation/0.jpg', 'class_ids': 0, 'scores': 0.92671424, 'label_names': '0°'}]
```

如上例所示，在实例化 EasyData 对象时，相关参数说明如下：

* `model`：用于指定预测模型，目前支持图像方向矫正模型 `image_orientation`、模糊图像过滤模型 `clarity_assessment`、广告码图像过滤模型 `code_exists`；
* `device`：用于指定预测平台，目前支持 `CPU`、`GPU`，默认为 `CPU`；

同样以图像方向矫正模型为例，在与 PaddleClas 图像分类模型结合使用时，可以参考示例[代码](../../../deploy/python/ppldi/demo.py)。

## 3. 小结

通过本节内容，相信您已经熟练掌握 EasyData whl 包的使用方法并获得了初步效果。EasyData 是一套数据治理工具，目前支持对图像方向、清晰度、是否包含广告码进行分类。
