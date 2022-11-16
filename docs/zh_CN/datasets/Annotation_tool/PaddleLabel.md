

<div align="center">

<p align="center">
  <img src="https://user-images.githubusercontent.com/35907364/182084617-ea94f744-3a34-4193-98fe-5d6869a118fc.png" align="middle" alt="LOGO" width = "500" />
</p>

**飞桨智能标注，让标注快人一步**

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/) ![PyPI](https://img.shields.io/pypi/v/paddlelabel?color=blue) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE) [![Start](https://img.shields.io/github/stars/PaddleCV-SIG/PaddleLabel?color=orange)]() [![Fork](https://img.shields.io/github/forks/PaddleCV-SIG/PaddleLabel?color=orange)]() ![PyPI - Downloads](https://img.shields.io/pypi/dm/paddlelabel?color=orange) [![OS](https://img.shields.io/badge/os-linux%2C%20windows%2C%20macos-green.svg)]()

</div>

## 最新动态

- 【2022-08-18】 :fire: PaddleLabel 0.1 版本发布！
  - 【分类】支持单分类与多分类标注及标签的导入导出。简单灵活实现自定义数据集分类标注任务并导出供[PaddleClas](https://github.com/PaddlePaddle/PaddleClas)进行训练。
  - 【检测】支持检测框标注及标签的导入导出。快速上手生成自己的检测数据集并应用到[PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection)。
  - 【分割】支持多边形、笔刷及交互式等多种标注方式，支持标注语义分割与实例分割两种场景。多种分割标注方式可灵活选择，方便将导出数据应用在[PaddleSeg](https://github.com/PaddlePaddle/PaddleSeg)获取个性化定制模型。

## 简介

PaddleLabel 是基于飞桨 PaddlePaddle 各个套件的特性提供的配套标注工具。它涵盖分类、检测、分割三种常见的计算机视觉任务的标注能力，具有手动标注和交互式标注相结合的能力。用户可以使用 PaddleLabel 方便快捷的标注自定义数据集并将导出数据用于飞桨提供的其他套件的训练预测流程中。
整个 PaddleLabel 包括三部分，本项目包含 PaddleLabel 的后端实现。 [PaddleLabel-Frontend](https://github.com/PaddleCV-SIG/PaddleLabel-Frontend)是基于 React 和 Ant Design 构建的 PaddleLabel 前端，[PaddleLabel-ML](https://github.com/PaddleCV-SIG/PaddleLabel-ML)是基于 PaddlePaddle 的自动和交互式标注的机器学习后端。

![demo720](https://user-images.githubusercontent.com/71769312/185099439-3230cf80-798d-4a81-bcae-b88bcb714daa.gif)

## 特性

- **简单** 手动标注能力直观易操作，方便用户快速上手。
- **高效** 支持交互式分割功能，分割精度及效率提升显著。
- **灵活** 分类支持单分类和多分类的标注，分割支持多边形、笔刷及交互式分割等多种功能，方便用户根据场景需求切换标注方式。
- **全流程** 与其他飞桨套件密切配合，方便用户完成数据标注、模型训练、模型导出等全流程操作。



## 使用教程

**文档**

- [安装指南](https://github.com/PaddleCV-SIG/PaddleLabel/blob/v0.1.0/doc/CN/install.md)
- [快速开始](https://github.com/PaddleCV-SIG/PaddleLabel/blob/v0.1.0/doc/CN/quick_start.md)

**进行标注**

- [图像分类](https://github.com/PaddleCV-SIG/PaddleLabel/blob/v0.1.0/doc/CN/project/classification.md)
- [目标检测](https://github.com/PaddleCV-SIG/PaddleLabel/blob/v0.1.0/doc/CN/project/detection.md)
- [语义分割](https://github.com/PaddleCV-SIG/PaddleLabel/blob/v0.1.0/doc/CN/project/semantic_segmentation.md)
- [实例分割](https://github.com/PaddleCV-SIG/PaddleLabel/blob/v0.1.0/doc/CN/project/instance_segmentation.md)

**训练教程**

- [如何用 PaddleClas 进行训练](https://github.com/PaddleCV-SIG/PaddleLabel/blob/v0.1.0/doc/CN/training/PdLabel_PdClas.md)
- [如何用 PaddleDet 进行训练](https://github.com/PaddleCV-SIG/PaddleLabel/blob/v0.1.0/doc/CN/training/PdLabel_PdDet.md)
- [如何使用 PaddleSeg 进行训练](https://github.com/PaddleCV-SIG/PaddleLabel/blob/v0.1.0/doc/CN/training/PdLabel_PdSeg.md)
- [如何使用 PaddleX 进行训练](https://github.com/PaddleCV-SIG/PaddleLabel/blob/v0.1.0/doc/CN/training/PdLabel_PdX.md)

**AI Studio 项目**

- [花朵分类](https://aistudio.baidu.com/aistudio/projectdetail/4337003)
- [道路标志检测](https://aistudio.baidu.com/aistudio/projectdetail/4349280)
- [图像分割](https://aistudio.baidu.com/aistudio/projectdetail/4353528)
- [如何使用 PaddleX 进行训练](https://aistudio.baidu.com/aistudio/projectdetail/4383953)

