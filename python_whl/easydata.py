# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
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
import platform

parent = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(parent, './deploy/')))

import argparse

from ppcv.engine.pipeline import Pipeline
from utils.utils import load_yaml
from python.ppdataaug import PPDataAug
from python.ppdataaug.utils import config
from python.ppdataaug.gen_ocr_rec import GenOCR
from python.ppdataaug.utils import logger

__all__ = ['EasyData']

VERSION = '0.5.0.1'

PPDA_CONFIG = {
    'img2img': {
        'config': 'deploy/configs/ppdataaug_clas.yaml'
    },
    'text2img': {
        'config': 'deploy/configs/ppdataaug_ocr_text2img.yaml'
    }
}


class LoopDict(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def loop_set(self, key_list, value):
        # for key in key_list:
        key = key_list[0]
        if key not in self:
            self[key] = LoopDict()
        if len(key_list) == 1:
            self[key] = value
        else:
            self[key].loop_set(key_list[1:], value)


def argsparser():

    def str2bool(v):
        return v.lower() in ("true", "t", "1")

    parser = argparse.ArgumentParser()

    parser.add_argument("--model", type=str, required=True, help="Model name.")

    parser.add_argument("--output_dir",
                        type=str,
                        default=None,
                        help="Directory of output visualization files.")

    args = parser.parse_args()
    return vars(args)


def init_pipeline_config(**cfg):
    # only support PPLDI now
    model_name = cfg["model"]
    base_cfg_path = f"./deploy/configs/ppcv/{model_name}.yaml"
    __dir__ = os.path.dirname(__file__)
    base_cfg_path = os.path.join(__dir__, base_cfg_path)
    base_cfg = load_yaml(base_cfg_path)

    # ENV config
    env_config = {}
    if "output_dir" in cfg and cfg["output_dir"]:
        env_config["output_dir"] = cfg["output_dir"]
    if "run_mode" in cfg and cfg["run_mode"]:
        env_config["run_mode"] = cfg["run_mode"]
    if "device" in cfg and cfg["device"]:
        env_config["device"] = cfg["device"]
    if "print_res" in cfg and cfg["print_res"] is not None:
        env_config["print_res"] = cfg["print_res"]
    if "return_res" in cfg and cfg["return_res"] is not None:
        env_config["return_res"] = cfg["return_res"]

    # MODEL config
    model_config = LoopDict()
    # replace path of class_id_map_file by absolute path
    for model_cfg in base_cfg["MODEL"]:
        op_name = list(model_cfg.keys())[0]
        if op_name == "ClassificationOp":
            postprocess_ops = model_cfg[op_name].get("PostProcess", [])
            for postprocess_op in postprocess_ops:
                postprocess_op_name = list(postprocess_op.keys())[0]
                if postprocess_op_name in ["ThreshOutput", "Topk"]:
                    class_id_map_file_path = postprocess_op[
                        postprocess_op_name].get("class_id_map_file", None)
                    if class_id_map_file_path is not None:
                        class_id_map_file_path = os.path.join(
                            __dir__, class_id_map_file_path)
                        model_config.loop_set([
                            "0", "ClassificationOp", "PostProcess", "0",
                            postprocess_op_name, "class_id_map_file"
                        ], class_id_map_file_path)
    if "threshold" in cfg and cfg["threshold"]:
        model_config.loop_set([
            "0", "ClassificationOp", "PostProcess", "0", "ThreshOutput",
            "threshold"
        ], cfg["threshold"])

    opt_config = {"MODEL": model_config, "ENV": env_config}
    FLAGS = argparse.Namespace(**{"config": base_cfg_path, "opt": opt_config})
    return FLAGS


def parse_args():

    def str2bool(v):
        return v.lower() in ("true", "t", "1")

    parser = argparse.ArgumentParser()

    # common args
    parser.add_argument(
        "--model",
        type=str,
        default="ppdataaug",
    )
    parser.add_argument(
        "--run_mode",
        type=str,
        default="paddle",
        help="mode of running(paddle/trt_fp32/trt_fp16/trt_int8)")
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help=
        "Choose the device you want to run, it can be: CPU/GPU/XPU, default is CPU."
    )
    parser.add_argument("--print_res", type=str2bool, default=True)

    # PPLDI args
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help=
        "Path of input, suport image file, image directory and video file.",
        required=False)
    parser.add_argument("--threshold", type=float, default=0, required=False)

    # PPDA args
    parser.add_argument("--gen_mode", type=str, default="img2img")
    parser.add_argument("--gen_num", type=int, default=10)
    parser.add_argument("--gen_ratio", type=float, default=0)

    # params for aug
    parser.add_argument("--ops",
                        type=list,
                        default=[
                            "randaugment", "random_erasing", "gridmask",
                            "tia_distort", "tia_stretch", "tia_perspective"
                        ])
    parser.add_argument("--ori_data_dir",
                        type=str,
                        default="demo/clas_data",
                        required=False)
    parser.add_argument("--label_file",
                        type=str,
                        default="demo/clas_data/train_list.txt",
                        required=False)
    parser.add_argument("--gen_label", type=str, default="labels/test.txt")
    parser.add_argument("--out_dir", type=str, default="test")
    parser.add_argument("--size", type=int, default=224)

    # params for ocr_rec
    parser.add_argument("--bg_num_per_word", type=int, default=5)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--bg_img_dir", type=str, default="demo/ocr_rec/bg")
    parser.add_argument("--font_dir", type=str, default="demo/ocr_rec/font")
    parser.add_argument("--corpus_file",
                        type=str,
                        default="demo/ocr_rec/corpus.txt")

    parser.add_argument("--delimiter", type=str, default=" ")

    # FeatureExtract args
    parser.add_argument("--repeat_ratio", type=float, default=0.9)
    parser.add_argument("--compare_out", type=str, default="tmp/rm_repeat.txt")

    # BigModel args
    parser.add_argument("--use_big_model", type=str2bool, default=True)
    parser.add_argument("--quality_ratio", type=float, default=0.4)
    parser.add_argument("--final_label",
                        type=str,
                        default="high_socre_label.txt")
    parser.add_argument("--model_type", type=str, default="cls")
    return parser.parse_args()


class PPDA(PPDataAug):

    def __init__(self, **kwargs):
        args = parse_args()
        args.__dict__.update(**kwargs)
        self.save_list = []
        model_config = PPDA_CONFIG[args.gen_mode]['config']
        if args.model_type == "ocr_rec":
            args.delimiter = "\t"
        self.config = config.get_config(model_config, show=False)
        self.config = config.merge_gen_config(self.config, args.__dict__,
                                              "DataGen")
        self.delimiter = self.config["DataGen"].get('delimiter', ' ')
        self.output_dir = args.out_dir
        if args.gen_mode == "text2img":
            self.gen_ocr = GenOCR(self.config["DataGen"]["config"])
            self.bg_img_dir = args.bg_img_dir
            self.font_dir = args.font_dir
            self.corpus_file = args.corpus_file
            self.bg_img_per_word_num = args.bg_num_per_word
            if platform.system().lower() == 'windows':
                self.threads = 1
                logger.warning('Windows has not support threads > 1')
            else:
                self.threads = args.threads
        self.aug_type = args.ops
        self.gen_num = args.gen_num
        self.gen_ratio = args.gen_ratio
        self.gen_label = args.gen_label
        self.gen_mode = args.gen_mode
        self.compare_out = args.compare_out
        self.feature_thresh = args.repeat_ratio

        self.config["FeatureExtract"]["thresh"] = args.repeat_ratio
        self.config["IndexProcess"]["all_label_file"] = args.gen_label
        self.config["IndexProcess"]["image_root"] = args.out_dir
        self.config["IndexProcess"]["delimiter"] = args.delimiter

        if not os.path.exists("tmp"):
            os.makedirs("tmp")
        if not args.use_big_model:
            self.config.pop("BigModel")
            self.compare_out = args.final_label
        else:
            self.config["BigModel"]["thresh"] = args.quality_ratio
            self.config["BigModel"]["final_label"] = args.final_label
            self.big_model_out = args.final_label
            self.model_type = args.model_type
        config.print_config(self.config)

    def predict(self):
        self.run()


class EasyData(object):

    def __init__(self, **cfg):
        self.model = cfg['model']
        if self.model == "ppdataaug":
            self.pipeline = PPDA(**cfg)
        else:
            FLAGS = init_pipeline_config(**cfg)
            self.pipeline = Pipeline(FLAGS)

    def predict(self, input=None):
        if self.model == "ppdataaug":
            return self.pipeline.predict()
        else:
            return self.pipeline.run(input)


# for CLI
def main():
    args = parse_args()
    easydata = EasyData(**(args.__dict__))
    easydata.predict(args.input)


if __name__ == "__main__":
    main()
