import cv2
import os
import numpy as np
import argparse
import random
from random import sample
from tqdm import tqdm
import traceback

from python.ppdataaug.utils import logger
from .data.preprocess import transform
from .data.preprocess.ops.operators import DecodeImage, ResizeImage
from .data.preprocess.ops.randaugment import RandAugment
from .data.preprocess.ops.random_erasing import RandomErasing, RandomErasingOCR
from .data.preprocess.ops.grid import GridMask, GridMaskOCR
from .data.imaug.text_image_aug.augment import tia_distort, tia_perspective, tia_stretch


def init_args():
    parser = argparse.ArgumentParser()
    # params for prediction engine
    parser.add_argument("--ops", type=str, default="randaugment")
    parser.add_argument("--label_file",
                        type=str,
                        default="dataset/imgnet100/train_list_100.txt")
    parser.add_argument("--output_file", type=str, default="test.txt")
    parser.add_argument("--out_dir", type=str, default="test")
    parser.add_argument("--data_dir", type=str, default="dataset/imgnet100")
    parser.add_argument("--gen_ratio", type=float, default="0")
    parser.add_argument("--gen_num", type=int, default="5")
    parser.add_argument("--size", type=int, default="224")
    return parser


def parse_args():
    parser = init_args()
    return parser.parse_args()


def get_image_file_list(img_file):
    imgs_lists = []
    if not os.path.exists(img_file):
        raise Exception("{} does not exist!".format(img_file))
    with open(img_file, "r", encoding="utf-8") as file:
        for data_line in file.readlines():
            imgs_lists.append(data_line)
    return imgs_lists


class GenAug(object):
    """gen aug data
    """

    def __init__(self, config):
        config = config["DataGen"]
        self.ops = config["aug"]
        self.size = config["size"]
        self.model_type = config.get("model_type", 'cls')
        self.delimiter = config.get("delimiter", ' ')
        decode_op = DecodeImage()
        if type(self.size) is int:
            size = (self.size, self.size)
        else:
            assert len(
                self.size) == 2, "size shape must be 2, but got {}".format(
                    len(self.size))
            size = self.size
        resize_op = ResizeImage(size)
        if self.ops == "randaugment":
            aug_op = RandAugment()
        if self.ops == "random_erasing":
            if self.model_type == 'ocr_rec':
                aug_op = RandomErasingOCR(prob=1.0)
            else:
                aug_op = RandomErasing(EPSILON=1.0)
        if self.ops == "gridmask":
            if self.model_type == 'ocr_rec':
                aug_op = GridMaskOCR(prob=1.0)
            else:
                aug_op = GridMask(d1=96,
                                  d2=self.size,
                                  rotate=1,
                                  ratio=0.6,
                                  mode=1,
                                  prob=0.8)

        if self.ops in ["randaugment", "random_erasing", "gridmask"]:
            self.all_op = [decode_op, resize_op, aug_op]
        else:
            self.all_op = [decode_op, resize_op]
        if self.model_type == 'ocr_rec':
            self.all_op.pop(1)

        self.gen_num = config["gen_num"]
        self.img_list = get_image_file_list(config["label_file"])

        self.imgs_dir = config["ori_data_dir"]

        if not os.path.exists(config["img_save_folder"] + "/" + self.ops):
            os.makedirs(config["img_save_folder"] + "/" + self.ops)

        self.all_num = 0
        self.output_file = config["gen_label"]
        self.out_dir = config["img_save_folder"]

    def __call__(self, gen_num=5, gen_ratio=0, trans_label=None):
        if gen_ratio > 0:
            gen_num = int(len(self.img_list) * gen_ratio)

        if gen_num > 0:
            if gen_num <= len(self.img_list):
                gen_img_list = sample(self.img_list, gen_num)
            else:
                ratio = gen_num // len(self.img_list)
                res = gen_num % len(self.img_list)
                gen_img_list = self.img_list * ratio
                gen_img_list += sample(self.img_list, res)
        else:
            gen_img_list = self.img_list

        for line in tqdm(gen_img_list, desc='in aug {} '.format(self.ops)):
            self.all_num += 1
            try:
                file_name, label = line.split(self.delimiter)
                img_path = os.path.join(self.imgs_dir, file_name)
                if not os.path.exists(img_path):
                    raise Exception("{} does not exist!".format(img_path))
                label = label.strip("\n")
                with open(os.path.join(self.imgs_dir, file_name), 'rb') as f:
                    data = f.read()
                data = transform(data, self.all_op)
                if self.ops == "tia_distort":
                    data = tia_distort(data, random.randint(1, 3))
                if self.ops == "tia_stretch":
                    data = tia_stretch(data, random.randint(1, 3))
                if self.ops == "tia_perspective":
                    data = tia_perspective(data)
                img_name_pure = os.path.split(file_name)[-1]
                cv2.imwrite(
                    "{}/{}/{}_{}".format(self.out_dir, self.ops, self.all_num,
                                         img_name_pure), np.array(data))
                trans_label.write("{}/{}_{}{}{}\n".format(
                    self.ops, self.all_num, img_name_pure, self.delimiter,
                    label))
            except:
                logger.error(
                    "error in generat aug image:{}, err msg: {}".format(
                        line, traceback.format_exc()))
        return self.output_file


if __name__ == "__main__":
    args = parse_args()
    for k, v in sorted(vars(args).items()):
        print(k, '=', v)
    op_list = [
        "randaugment", "random_erasing", "gridmask", "tia_distort",
        "tia_stretch", "tia_perspective"
    ]
    for op in op_list:
        args.ops = op
        gen_op = GenAug(args)
        gen_op(5)
