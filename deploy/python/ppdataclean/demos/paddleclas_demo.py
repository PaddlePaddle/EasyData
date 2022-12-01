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

import numpy as np
import cv2
from easydata import EasyData
from paddleclas import PaddleClas


def main(img_path):
    orientation_model = EasyData(model="image_orientation",
                                 device="cpu",
                                 return_res=True,
                                 print_res=False)
    clas_model = PaddleClas(model_name="PPLCNet_x0_25")

    orientation_result = orientation_model.predict(img_path)
    orientation_id = orientation_result[0]["class_ids"]

    img = cv2.imread(img_path)[:, :, ::-1]
    img = np.rot90(img, -1 * orientation_id)

    clas_result = clas_model.predict(img)
    print(next(clas_result))


if __name__ == "__main__":
    img_path = "./easydata_demo_imgs/image_orientation/1.jpg"
    main(img_path)
