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


class NormalizeFeature(object):
    def __init__(self, normalize=True):
        super().__init__()
        self.normalize = normalize

    def __call__(self, x, output_keys):
        if self.normalize:
            feas_norm = np.sqrt(np.sum(np.square(x), axis=1, keepdims=True))
            x = np.divide(x, feas_norm)

        y = []
        for idx, feature in enumerate(x):
            result = {output_keys[0]: feature}
            y.append(result)
        return y
