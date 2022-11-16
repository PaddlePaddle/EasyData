# copyright (c) 2021 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import subprocess

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '../')))

os.environ["FLAGS_allocator_strategy"] = 'auto_growth'

import cv2
import copy
import argparse
import random
import numpy as np
import faiss
import pickle
import json
import time
import logging
from PIL import Image

parent = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(parent, '../../deploy/')))

from ppcv.engine.pipeline import Pipeline
from ppcv.utils.logger import setup_logger
from ppcv.core.config import ArgsParser

from python.ppdataaug.utils.utility import get_label, rm_repeat, check_dir, concat_file
from python.ppdataaug.utils import config
from python.ppdataaug.utils import logger
from python.ppdataaug.utils.get_image_list import get_image_list_from_label_file
from python.ppdataaug.gen_img import GenAug
from python.ppdataaug.gen_ocr_rec import GenOCR
from python.ppdataaug.predict.build_gallery import GalleryBuilder


class PPDataAug(object):

    def __init__(self, cfg):
        self.save_list = []
        config_args = config.parse_args()
        self.config = config.get_config(cfg.config, show=True)

        gen_params = self.config["DataGen"]
        self.gen_num = gen_params["gen_num"]
        self.output_dir = gen_params["img_save_folder"]
        self.gen_label = gen_params["gen_label"]
        self.gen_mode = gen_params.get('mode', 'img2img').lower()
        assert self.gen_mode in [
            "img2img", "text2img"
        ], 'param gen_mode must in {}, but got {}'.format(
            ["img2img", "text2img"], self.gen_mode)
        if self.gen_mode == "text2img":
            self.bg_img_per_word_num = gen_params["bg_num_per_word"]
            self.threads = gen_params["threads"]
            self.bg_img_dir = gen_params["bg_img_dir"]
            self.font_dir = gen_params["font_dir"]
            self.corpus_file = gen_params["corpus_file"]
            self.gen_ocr = GenOCR(gen_params["config"])
            self.delimiter = gen_params.get('delimiter', '\t')
        elif self.gen_mode == "img2img":
            self.gen_ratio = gen_params["gen_ratio"]
            self.delimiter = gen_params.get('delimiter', ' ')
            self.ori_label = gen_params["label_file"]
            self.aug_type = gen_params["ops"]

        self.compare_out = self.config["FeatureExtract"]["file_out"]
        check_dir(self.compare_out)
        self.feature_thresh = self.config["FeatureExtract"]["thresh"]

        if not os.path.exists("tmp"):
            os.makedirs("tmp")

    def build_big_model(self):
        if "BigModel" in self.config:
            self.score_thresh = self.config["BigModel"]["thresh"]
            self.big_model_out = self.config["BigModel"]["final_label"]
            self.model_type = self.config["BigModel"]["model_type"]
            assert self.model_type in [
                "ocr_rec", "cls"
            ], 'param lang must in {}, but got {}'.format(["ocr_rec", "cls"],
                                                          self.model_type)
            FLAGS = argparse.Namespace(
                **{"config": self.config["BigModel"]["config"]})
            big_model = Pipeline(FLAGS)
            return big_model
        else:
            return False

    def build_feature_compare(self):
        FLAGS = argparse.Namespace(
            **{"config": self.config["FeatureExtract"]["config"]})
        feature_extract = Pipeline(FLAGS)
        return feature_extract

    def build_search(self):
        assert 'IndexProcess' in self.config.keys(
        ), "Index config not found ... "
        self.return_k = self.config['IndexProcess']['return_k']

        index_dir = self.config["IndexProcess"]["index_dir"]
        self.all_label_file = self.config["IndexProcess"]["all_label_file"]

        if self.config['IndexProcess'].get("dist_type") == "hamming":
            self.Searcher = faiss.read_index_binary(
                os.path.join(index_dir, "vector.index"))
        else:
            self.Searcher = faiss.read_index(
                os.path.join(index_dir, "vector.index"))

        with open(os.path.join(index_dir, "id_map.pkl"), "rb") as fd:
            self.id_map = pickle.load(fd)

    def run(self):
        # gen aug data
        logger.info('{}Start Gen Img{}'.format('*' * 10, '*' * 10))
        check_dir(self.gen_label)
        check_dir(self.compare_out)

        if self.gen_mode == "text2img":
            self.gen_ocr(self.bg_img_dir, self.font_dir, self.corpus_file,
                         self.gen_num, self.output_dir,
                         self.bg_img_per_word_num, self.threads,
                         self.delimiter)

            concat_file(label_dir=self.output_dir, all_file=self.gen_label)

        else:
            with open(self.gen_label, "w", encoding="utf-8") as f:
                for aug_type in self.aug_type:
                    self.config["DataGen"]["aug"] = aug_type
                    dataaug = GenAug(self.config)
                    dataaug(gen_num=self.gen_num, trans_label=f)

        assert os.path.getsize(
            self.gen_label
        ), "Data generate Failed, Please check data_dir and label_file. "

        logger.info('{}Generate Img has been saved in {} {}'.format(
            '*' * 10, self.output_dir, '*' * 10))

        # build gallery
        logger.info('{}Start compare img feature{}'.format('*' * 10, '*' * 10))
        feature_extract = self.build_feature_compare()

        GalleryBuilder(self.config, feature_extract)
        self.build_search()
        # feather compare
        root_path = self.config["IndexProcess"]["image_root"]
        image_list, gt = get_image_list_from_label_file(
            self.all_label_file, self.delimiter)

        with open("tmp/repeat.txt", "w", encoding="utf-8") as write_file:
            for idx, image_file in enumerate(image_list):
                preds = {}
                output = []
                rec_results = feature_extract.run(
                    os.path.join(root_path, image_file))
                feature = np.array([rec_results[0]["feature"]])
                scores, docs = self.Searcher.search(feature, self.return_k)

                if scores[0][0] >= self.config["IndexProcess"]["score_thres"]:
                    preds["rec_docs"] = [
                        self.id_map[docs[0][i]] for i in range(self.return_k)
                    ]
                    preds["rec_scores"] = scores[0]
                    output.append(preds)
                if len(output):
                    write_file.write(image_file + "\t" +
                                     output[0]['rec_docs'][1][:-2] + "\t" +
                                     str(output[0]['rec_scores'][1]) + "\n")

        # rm repeat
        all_label = get_label(self.all_label_file, self.delimiter)
        final_count = rm_repeat(all_label,
                                self.save_list,
                                compare_file="tmp/repeat.txt",
                                out_file=self.compare_out,
                                thresh=self.feature_thresh,
                                delimiter=self.delimiter)

        logger.info("Repeat img has been removed, new label file is {}".format(
            self.compare_out))

        # filter low score data
        image_list, gt_labels = get_image_list_from_label_file(
            self.compare_out, self.delimiter)
        batch_names = []
        batch_labels = []

        big_model = self.build_big_model()
        if not big_model:
            logger.info("You didn't need big model, final label is {}".format(
                self.compare_out))
            return

        logger.info('{}Start use big model to filer quality{}'.format(
            '*' * 10, '*' * 10))
        cnt = 0
        with open(self.big_model_out, "w", encoding="utf-8") as save_file:
            for idx, img_path in enumerate(image_list):
                file_name = os.path.join(root_path, img_path)
                if os.path.exists(file_name):
                    batch_names.append(file_name)
                    batch_labels.append(gt_labels[idx])
                    cnt += 1
                else:
                    logger.warning(
                        "Image file failed to read and has been skipped. The path: {}"
                        .format(img_path))

                if cnt % self.config["BigModel"]["batch_size"] == 0 or (
                        idx + 1) == len(image_list):
                    if len(batch_names) == 0:
                        continue
                    # big model predict
                    batch_results = big_model.predict_images(batch_names)

                    for number, result_dict in enumerate(batch_results):
                        if self.model_type == "cls":
                            filename = batch_names[number]
                            scores_str = "[{}]".format(", ".join(
                                "{:.2f}".format(r)
                                for r in result_dict["scores"]))
                            if float(scores_str[1:-1]) > self.score_thresh:
                                save_file.write("{}{}{}\n".format(
                                    filename, self.delimiter,
                                    batch_labels[number]))
                        elif self.model_type == "ocr_rec":
                            filename = batch_names[number]
                            scores = result_dict["rec_score"]
                            if scores > self.score_thresh:
                                save_file.write("{}{}{}\n".format(
                                    filename, self.delimiter,
                                    batch_labels[number]))
                    batch_labels = []
                    batch_names = []
        logger.info(
            "Low quality img has been removed, new label file is {}".format(
                self.big_model_out))
