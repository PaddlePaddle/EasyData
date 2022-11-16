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
import numpy as np
import math
import paddle
import collections
from collections import defaultdict
from collections.abc import Sequence
import yaml
import copy
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from ppcv.utils.logger import setup_logger
import ppcv
from ppcv.ops import *

logger = setup_logger('config')


class ArgsParser(ArgumentParser):
    def __init__(self):
        super(ArgsParser, self).__init__(
            formatter_class=RawDescriptionHelpFormatter)
        self.add_argument(
            "-o", "--opt", nargs='*', help="set configuration options")

    def parse_args(self, argv=None):
        args = super(ArgsParser, self).parse_args(argv)
        assert args.config is not None, \
            "Please specify --config=configure_file_path."
        args.opt = self._parse_opt(args.opt)
        return args

    def _parse_opt(self, opts):
        config = {}
        if not opts:
            return config
        for s in opts:
            s = s.strip()
            k, v = s.split('=', 1)
            if '.' not in k:
                config[k] = yaml.load(v, Loader=yaml.Loader)
            else:
                keys = k.split('.')
                if keys[0] not in config:
                    config[keys[0]] = {}
                cur = config[keys[0]]
                for idx, key in enumerate(keys[1:]):
                    if idx == len(keys) - 2:
                        cur[key] = yaml.load(v, Loader=yaml.Loader)
                    else:
                        cur[key] = {}
                        cur = cur[key]
        return config


class ConfigParser(object):
    def __init__(self, args):
        with open(args.config) as f:
            cfg = yaml.safe_load(f)
        self.model_cfg, self.env_cfg = self.merge_cfg(args, cfg)
        self.check_cfg()

    def merge_cfg(self, args, cfg):
        env_cfg = cfg['ENV']
        model_cfg = cfg['MODEL']

        def str2num(v):
            try:
                return eval(v)
            except Exception:
                return v

        def merge(cfg, arg):
            merge_cfg = copy.deepcopy(cfg)
            for k, v in env_cfg.items():
                if k in arg:
                    merge_cfg[k] = arg[k]
                else:
                    if isinstance(v, dict):
                        merge_cfg[k] = merge(v, arg)
            return merge_cfg

        def override(cfg, arg):
            assert isinstance(cfg, (dict, list))
            if isinstance(cfg, list):
                for key in arg.keys():
                    idx = str2num(key)
                    value = arg[key]
                    if isinstance(value, (dict, list)):
                        override(cfg[idx], value)
                    else:
                        cfg[idx] = value
            else:
                for key in arg.keys():
                    value = arg[key]
                    if isinstance(value, (dict, list)):
                        override(cfg[key], value)
                    else:
                        cfg[key] = value

        def merge_opt(cfg, arg):
            override(cfg, arg)
            return cfg

        args_dict = vars(args)
        env_cfg = merge(env_cfg, args_dict)
        if 'opt' in args_dict.keys() and args_dict['opt']:
            opt_dict = args_dict['opt']
            if opt_dict.get('ENV', None):
                env_cfg = merge_opt(env_cfg, opt_dict['ENV'])
            if opt_dict.get('MODEL', None):
                model_cfg = merge_opt(model_cfg, opt_dict['MODEL'])

        return model_cfg, env_cfg

    def check_cfg(self):
        unique_name = set()
        unique_name.add('input')
        op_list = ppcv.ops.__all__
        output_set = {'input.image', 'input.video'}
        for model in self.model_cfg:
            model_name = list(model.keys())[0]
            model_dict = list(model.values())[0]

            # check the name and last_ops is legal
            if 'name' not in model_dict or 'last_ops' not in model_dict:
                raise ValueError(
                    'Missing name or last_op field in {} model config'.format(
                        model_name))

            last_ops = model_dict['last_ops']
            assert isinstance(
                last_ops, Sequence
            ), 'The last_ops must be sequence, but the type in {} is {}'.format(
                model_name, type(last_ops))
            for last_op in last_ops:
                assert last_op in unique_name, 'The last_op {} in {} model config is not exist.'.format(
                    model_dict['last_ops'], model_name)
            unique_name.add(model_dict['name'])

        device = self.env_cfg['device']
        assert device.upper() in ['CPU', 'GPU', 'XPU'
                                  ], "device should be CPU, GPU or XPU"

    def parse(self):
        return self.model_cfg, self.env_cfg

    def print_cfg(self):
        print('----------- Environment Arguments -----------')
        buffer = yaml.dump(self.env_cfg)
        print(buffer)
        print('------------- Model Arguments ---------------')
        buffer = yaml.dump(self.model_cfg)
        print(buffer)
        print('---------------------------------------------')
