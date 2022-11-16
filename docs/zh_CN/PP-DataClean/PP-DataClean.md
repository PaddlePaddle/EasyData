# 数据清洗

------

EasyData 是基于飞桨开发的数据处理工具，旨在帮助视觉开发者在模型开发的过程中更好的处理数据，数据清洗工具（PP-DataClean）是 EasyData 的子模块，其主要帮助开发者可以更好的提升数据质量或者筛选和过滤低质数据。数据清洗工具可以应用到部署时数据的预处理中，可以在增加很少推理时间的情况下大幅增加精度。也可以应用到训练数据、测试数据的筛选过滤中，结合相关的后处理，不仅可以进一步增加模型的精度，也可以增加相关产品的满意度。

作为可插拔的模块，PP-DataClean 可以嵌到任何视觉任务中，其功能可视化如下：

<div align="center">
<img src="https://user-images.githubusercontent.com/45199522/201908925-bde8e9ac-1216-41c9-b39f-5ab77506a396.png">
</div>

目前，数据清洗模块包含图像方向矫正、模糊图像过滤、二维码图像过滤，相关的模型介绍及模型下载链接如下：

| 类别 | 亮点 | 文档说明 | 模型下载 |
| :--: | :--: | :------: | :------: |
|图像方向矫正|自动矫正图像，大大提升多项视觉任务在旋转图像上精度|[文档](image_orientation_correction.md)|[下载链接](https://paddleclas.bj.bcebos.com/models/PULC/inference/image_orientation_infer.tar)|
|模糊图像过滤|判断图像是否模糊，可以广泛应用于模糊图像过滤、视觉相关业务的前处理等|[文档](blured_image_filtering.md)|[下载链接](https://paddleclas.bj.bcebos.com/models/PULC/inference/clarity_assessment_infer.tar)|
|二维码图像过滤|判断图像是否含有二维码、条形码、小程序码，可以广泛应用于广告码过滤、审核等业务|[文档](code_image_filtering.md)|[下载链接](https://paddleclas.bj.bcebos.com/models/PULC/inference/code_exists_infer.tar)|
