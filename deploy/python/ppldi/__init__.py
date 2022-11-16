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

from ppcv.engine.pipeline import Pipeline

from utils.utils import load_yaml


class PPDataImprove(object):
    def __init__(self, args):
        self.input = os.path.abspath(args.input)
        self.model_list = self.build_pipeline(args)

    def build_pipeline(self, args):
        config = load_yaml(args.config)
        config.pop("DataImprove")
        model_list = []
        for model in config.keys():
            pipeline_config_path = config[model]
            args.config = pipeline_config_path
            model_list.append(Pipeline(args))
        return model_list

    def run(self):
        for model in self.model_list:
            model.run(self.input)
