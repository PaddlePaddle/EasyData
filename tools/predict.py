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
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../deploy/')))

from ppcv.core.config import ArgsParser

from python.ppldi import PPDataImprove
from python.ppdataaug import PPDataAug
from utils.utils import load_yaml

def argsparser():
    parser = ArgsParser()

    parser.add_argument("-c","--config",
                        type=str,
                        default=None,
                        help=("Path of configure"),
                        required=True)
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help=
        "Path of input, suport image file, image directory and video file.",
        required=False)
    parser.add_argument("--output_dir",
                        type=str,
                        default="output",
                        help="Directory of output visualization files.")
    parser.add_argument(
        "--run_mode",
        type=str,
        default='paddle',
        help="mode of running(paddle/trt_fp32/trt_fp16/trt_int8)")
    parser.add_argument(
        "--device",
        type=str,
        default='cpu',
        help=
        "Choose the device you want to run, it can be: CPU/GPU/XPU, default is CPU."
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = argsparser()
    config_path = args.config
    yaml_data = load_yaml(config_path)
    if "DataImprove" in yaml_data:
        ppldi = PPDataImprove(args)
        ppldi.run()
    elif "DataGen" in yaml_data:
        ppdataaug = PPDataAug(args)
        ppdataaug.run()
    else:
        raise Exception("Error config")
