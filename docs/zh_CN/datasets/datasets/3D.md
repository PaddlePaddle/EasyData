## 通用3D数据集
这里整理了常用3D方向数据集，持续更新中，欢迎各位小伙伴贡献数据集～
- [KITTI](#KITTI)
- [nuScenes](#nuScenes)
- [Waymo](#Waymo)


<a name="KITTI"></a>
## 1、KITTI
- **数据来源**：https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d
- **数据简介**： KITTI数据集由卡尔斯鲁厄理工学院发布，用于评估自动驾驶场景3D目标检测等感知任务。数据采集真实道路场景，共包含3712个训练样本，3769个验证样本以及7518个测试样本。每个样本都包含lidar和camera两种模态的数据，train和validation都有标注数据，test没有标注数据。需要注意其标注的3d bbox坐标是在camera坐标系下进行的，且只标注了camera FOV内的目标,如下图：  
     <img src="https://www.cvlibs.net/datasets/kitti/images/header_3dobject.jpg"><br>
    
- **下载地址**：https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d


<a name="nuScenes"></a>
## 2、nuScenes
- **数据来源**：https://www.nuscenes.org/nuscenesobj_benchmark=3d
- **数据简介**： nuScenes数据集用于评估自动驾驶3D感知和规划任务，数据采集来自不同城市的1000个场景中，采集车上配备6个相机（CAM）、1个激光雷达（LIDAR）、5个毫米波雷达（RADAR）。采集的数据包括lidar和camera两种模态数据，共包含28k个训练样本，6k个验证样本，以及6k个测试样本，标注数据提供了物体的3d bbox坐标和类别信息：  
     <img src="https://www.nuscenes.org/static/media/data.9ef46c59.png"><br>
    
- **下载地址**：https://www.nuscenes.org/nuscenes
- **其他说明**：nuScenes的camera数据是360度环视相机拍摄，部分相机的FOV具有重叠，环视数据可用于BEV任务。

<a name="Waymo"></a>
## 3、Waymo
- **数据来源**：https://waymo.com/open/data/perception/
- **数据简介**： Waymo是谷歌Waymo无人驾驶公司在2020年发布的数据集，包含Mothion和Perception两大类，用于自动驾驶3D感知和预测任务。采集设备包括5个Lidar，5个Camera。Perception数据中训练集包含798个segment，每个segment包含约200个frame，总共约158361个样本，验证集包含202个segment，总共约40077个样本，每个样本都包含了lidar和camera模态数据。标注数据提供了物体的3d bbox坐标和物体类别信息，标注的坐标均为右手坐标系：  
    
- **下载地址**：https://waymo.com/open/data/perception/
- **其他说明**：waymo数据更新多次版本，为了获取更准确的标注信息和应用其它任务，请下载v1.3.2及其之后的版本。

