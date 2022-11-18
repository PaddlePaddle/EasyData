## 通用Segmentation数据集
这里整理了常用图像分割方向数据集，持续更新中，欢迎各位小伙伴贡献数据集～
- [CityScapes](#CityScapes)
- [Pascal VOC 2012](#PascalVOC2012)
- [Coco Stuff](#CocoStuff)
- [ADE20K](#ADE20K)
- [天空图像数据集](#天空图像数据集)
- [CO-SKEL数据集](#CO-SKEL数据集)
- [CAD-120affordance数据集](#CAD-120affordance数据集)
- [Intrinsic_Images_in_the_Wild](#Intrinsic_Images_in_the_Wild)
- [具有细长部分的鸟类昆虫数据集](#具有细长部分的鸟类昆虫数据集)
- [多品种果花检测数据集](#多品种果花检测数据集)
- [OpenSurfaces数据集](#OpenSurfaces数据集)
- [阴影检测/纹理分析数据集](#阴影检测/纹理分析数据集)


<a name="CityScapes"></a>
## 1、CityScapes
- **数据来源**：https://www.cityscapes-dataset.com/
- **数据简介**： Cityscapes是关于城市街道场景的语义理解图片数据集。它主要包含来自50个不同城市的街道场景，拥有5000张（2048 x 1024）高质量像素级注释图像，包含19个类别。Cityscapes数据集的训练集2975张，验证集500张，测试集1525张：  
     <img src="https://www.cityscapes-dataset.com/wordpress/wp-content/uploads/2015/07/stuttgart00-2040x500.png"><br>
    
- **下载地址**：https://paddleseg.bj.bcebos.com/dataset/cityscapes.tar

<a name="PascalVOC2012"></a>
## 2、Pascal VOC 2012
- **数据来源**：http://host.robots.ox.ac.uk/pascal/VOC/
- **数据简介**： Pascal VOC 2012数据集以对象分割为主，包含20个类别和背景类，其中训练集1464张，验证集1449张：  
     <img src="http://host.robots.ox.ac.uk/pascal/VOC/voc2012/segexamples/images/21_object.png"><br>
    
- **下载地址**：http://host.robots.ox.ac.uk/pascal/VOC/

<a name="CocoStuff"></a>
## 3、Coco Stuff
- **数据来源**：https://github.com/nightrome/cocostuff
- **数据简介**： Coco Stuff是基于Coco数据集的像素级别语义分割数据集。它主要覆盖172个类别，包含80个'thing'，91个'stuff'和1个'unlabeled'，我们忽略'unlabeled'类别，并将其index设为255，不记录损失。因此提供的训练版本为171个类别。其中，训练集118k, 验证集5k。：  
     <img src="https://camo.githubusercontent.com/0bff1f2d32ebee5d9e806dc83e6b124f64ebe16ab9d86ced625041799ee26017/687474703a2f2f63616c76696e2e696e662e65642e61632e756b2f77702d636f6e74656e742f75706c6f6164732f646174612f636f636f7374756666646174617365742f636f636f73747566662d6578616d706c65732e706e67"><br>
    
- **下载地址**：https://github.com/nightrome/cocostuff

<a name="ADE20K"></a>
## 4、ADE20K
- **数据来源**：https://groups.csail.mit.edu/vision/datasets/ADE20K/
- **数据简介**： ADE20K数据集由MIT发布的可用于场景感知、分割和多物体识别等多种任务的数据集，其涵盖了150个语义类别，包括训练集20210张，验证集2000张：  
     <img src="https://groups.csail.mit.edu/vision/datasets/ADE20K/assets/images/examples.png"><br>
    
- **下载地址**：https://paddleseg.bj.bcebos.com/dataset/ADEChallengeData2016.zip


<a name="天空图像数据集"></a>
## 5、天空图像数据集
- **数据来源**：http://suo.nz/1ykW0L
- **数据简介**：Sky 数据集包含 60 张带有地面实况的图像，用于天空分割。它基于 R. Fergus 15/02/03 的 Caltech Airplanes Side 数据集。选择数据集中包含天空区域的那些图像，并为它们创建地面实况。原始数据集图像名称保持不变。
<div align="center">
<img src="https://user-images.githubusercontent.com/59186797/202474154-3350bc12-7b02-49af-974b-79c9953c9511.jpg" width="400"><br>
</div>

- **下载地址**：http://suo.nz/1ykW0L

<a name="CO-SKEL数据集"></a>
## 6、CO-SKEL数据集
- **数据来源**：http://suo.nz/1FR95s
- **数据简介**：该数据集由分类骨架和分割掩码组成，用于评估协同骨架化方法。
<div align="center">
<img src="https://user-images.githubusercontent.com/59186797/202474719-f223ec75-5c0f-4400-b52c-89479bf45e79.jpg" width="400"><br>
</div>

- **下载地址**：http://suo.nz/1FR95s


<a name="CAD-120affordance数据集"></a>
## 7、CAD-120affordance数据集
- **数据来源**：http://suo.nz/1NnlU1
- **数据简介**：包含9916个对象实例的3090幅图像的逐像素注释。
<div align="center">
<img src="https://user-images.githubusercontent.com/59186797/202475296-0568a640-c354-4f16-b849-ccebc01755af.jpg" width="400"><br>
</div>

- **下载地址**：http://suo.nz/1NnlU1


<a name="Intrinsic_Images_in_the_Wild"></a>
## 8、Intrinsic_Images_in_the_Wild
- **数据来源**：http://suo.nz/1UTwnq
- **数据简介**：“Intrinsic Images in the Wild”，这是一个用于评估室内场景固有图像分解的大规模公共数据集。作者们通过数百万个众包注释创建了这个基准，这些注释对每个场景中的点对的材料属性进行了相对比较。
<div align="center">
<img src="https://user-images.githubusercontent.com/59186797/202476165-78193553-3935-45bf-9bf5-ce3400d9cb67.jpg" width="400"><br>
</div>

- **下载地址**：http://suo.nz/1UTwnq


<a name="具有细长部分的鸟类昆虫数据集"></a>
## 9、具有细长部分的鸟类昆虫数据集
- **数据来源**：http://suo.nz/22pJs7
- **数据简介**：这些数据库由 280 张具有ground truth的鸟类和昆虫的公共图像组成。
<div align="center">
<img src="https://user-images.githubusercontent.com/59186797/202476571-460fa3a2-1bbd-45b7-a700-34ec731132ba.jpg" width="400"><br>
</div>

- **下载地址**：http://suo.nz/22pJs7


<a name="多品种果花检测数据集"></a>
## 10、多品种果花检测数据集
- **数据来源**：http://suo.nz/29RKnM
- **数据简介**：该数据集包含四组花卉图像，来自三种不同的树种：苹果、桃和梨，以及随附的地面实况图像。
<div align="center">
<img src="https://user-images.githubusercontent.com/59186797/202477068-0783945e-3b49-45bd-9dfa-4fd69365fad5.jpg" width="400"><br>
</div>

- **下载地址**：http://suo.nz/29RKnM

<a name="OpenSurfaces数据集"></a>
## 11、OpenSurfaces数据集
- **数据来源**：http://suo.nz/1bI3Md
- **数据简介**：该数据集包含四组花卉图像，来自三种不同的树种：苹果、桃和梨，以及随附的地面实况图像。
<div align="center">
<img src="https://user-images.githubusercontent.com/59186797/202477464-d8bfa021-63d9-4859-bee9-00949605bbdb.jpg" width="400"><br>
</div>

- **下载地址**：http://suo.nz/1bI3Md


<a name="阴影检测/纹理分析数据集"></a>
## 12、阴影检测/纹理分析数据集
- **数据来源**：http://suo.nz/1iyjoA
- **数据简介**：一个用于阴影检测和纹理分析的简单计算机视觉数据集，专门用于帮助测试移动机器人的阴影检测算法（和纹理分割算法）——即使用 活动（移动）相机进行阴影检测。该数据集专注于纹理分析，因此每个图像序列都包含在许多不同纹理表面前移动的阴影。
<div align="center">
<img src="https://user-images.githubusercontent.com/59186797/202478005-86f5bc75-21fa-4ea7-a581-20955e4b2960.jpg" width="400"><br>
</div>

- **下载地址**：http://suo.nz/1iyjoA