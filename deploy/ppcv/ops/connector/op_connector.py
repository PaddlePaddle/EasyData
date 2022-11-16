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

__all__ = [
    "ClsCorrectionOp",
    "BboxCropOp",
    "PolyCropOp",
    "FragmentCompositionOp",
    "KeyFrameExtractionOp",
    "TableMatcherOp",
]

import cv2
import numpy as np

from ppcv.core.workspace import register
from .base import ConnectorBaseOp
from .keyframes_extract_helper import LUVAbsDiffKeyFrameExtractor
from .table_matcher import TableMatcher


@register
class ClsCorrectionOp(ConnectorBaseOp):
    """
    rotate
    """

    def __init__(self, model_cfg, env_cfg=None):
        super().__init__(model_cfg, env_cfg)
        self.class_num = model_cfg["class_num"]
        assert self.class_num in [
            2, 4
        ], f"just [2, 4] are supported but got {self.class_num}"
        if self.class_num == 2:
            self.rotate_code = {1: cv2.ROTATE_180, }
        else:
            self.rotate_code = {
                1: cv2.ROTATE_90_COUNTERCLOCKWISE,
                2: cv2.ROTATE_180,
                3: cv2.ROTATE_90_CLOCKWISE,
            }

        self.threshold = model_cfg["threshold"]
        self.check_input_keys()
        return

    @classmethod
    def get_output_keys(self):
        return ["corr_image"]

    def check_input_keys(self, ):
        # image, cls_id, prob is needed.
        assert len(
            self.input_keys
        ) == 3, f"input key of {self} must be 3 but got {len(self.input_keys)}"

    def __call__(self, inputs):
        outputs = []
        for idx in range(len(inputs)):
            images = inputs[idx][self.input_keys[0]]
            cls_ids = inputs[idx][self.input_keys[1]]
            probs = inputs[idx][self.input_keys[2]]
            is_image_list = isinstance(images, (list, tuple))
            if is_image_list is not True:
                images = [images]
                cls_ids = [cls_ids]
                probs = [probs]
            output = []
            for image, cls_id, prob in zip(images, cls_ids, probs):
                cls_id = cls_id[0]
                prob = prob[0]
                corr_image = image.copy()
                if prob >= self.threshold and cls_id in self.rotate_code:
                    corr_image = cv2.rotate(corr_image,
                                            self.rotate_code[cls_id])
                output.append(corr_image)

            if is_image_list is not True:
                output = output[0]
            outputs.append(output)
        return outputs


@register
class BboxCropOp(ConnectorBaseOp):
    """
    BboxCropOp
    """

    def __init__(self, model_cfg, env_cfg=None):
        super().__init__(model_cfg, env_cfg)
        self.check_input_keys()
        return

    @classmethod
    def get_output_keys(self):
        return ["bbox_crop_image"]

    def check_input_keys(self, ):
        # image, bbox is needed.
        assert len(
            self.input_keys
        ) == 2, f"input key of {self} must be 2 but got {len(self.input_keys)}"

    def __call__(self, inputs):
        outputs = []
        for idx in range(len(inputs)):
            images = inputs[idx][self.input_keys[0]]
            bboxes = inputs[idx][self.input_keys[1]]
            is_image_list = isinstance(images, (list, tuple))
            if is_image_list is not True:
                images = [images]
                bboxes = [bboxes]
            output = []
            # bbox: N x 4, x1, y1, x2, y2
            for image, bbox, in zip(images, bboxes):
                crop_imgs = []
                for single_bbox in bbox:
                    xmin, ymin, xmax, ymax = single_bbox.astype("int")
                    crop_img = image[ymin:ymax, xmin:xmax, :].copy()
                    crop_imgs.append(crop_img)
                output.append(crop_imgs)

            if is_image_list is not True:
                output = output[0]
            outputs.append(output)
        return outputs


@register
class PolyCropOp(ConnectorBaseOp):
    """
    PolyCropOp
    """

    def __init__(self, model_cfg, env_cfg=None):
        super().__init__(model_cfg, env_cfg)
        self.check_input_keys()
        return

    @classmethod
    def get_output_keys(self):
        return ["crop_image"]

    def check_input_keys(self, ):
        # image, bbox is needed.
        assert len(
            self.input_keys
        ) == 2, f"input key of {self} must be 2 but got {len(self.input_keys)}"

    def get_rotate_crop_image(self, img, points):
        '''
        img_height, img_width = img.shape[0:2]
        left = int(np.min(points[:, 0]))
        right = int(np.max(points[:, 0]))
        top = int(np.min(points[:, 1]))
        bottom = int(np.max(points[:, 1]))
        img_crop = img[top:bottom, left:right, :].copy()
        points[:, 0] = points[:, 0] - left
        points[:, 1] = points[:, 1] - top
        '''
        assert len(points) == 4, "shape of points must be 4*2"
        img_crop_width = int(
            max(
                np.linalg.norm(points[0] - points[1]),
                np.linalg.norm(points[2] - points[3])))
        img_crop_height = int(
            max(
                np.linalg.norm(points[0] - points[3]),
                np.linalg.norm(points[1] - points[2])))
        pts_std = np.float32([[0, 0], [img_crop_width, 0],
                              [img_crop_width, img_crop_height],
                              [0, img_crop_height]])
        M = cv2.getPerspectiveTransform(points.astype(np.float32), pts_std)
        dst_img = cv2.warpPerspective(
            img,
            M, (img_crop_width, img_crop_height),
            borderMode=cv2.BORDER_REPLICATE,
            flags=cv2.INTER_CUBIC)
        dst_img_height, dst_img_width = dst_img.shape[0:2]
        if dst_img_height * 1.0 / dst_img_width >= 1.5:
            dst_img = np.rot90(dst_img)
        return dst_img

    def sorted_boxes(self, dt_boxes):
        """
        Sort text boxes in order from top to bottom, left to right
        args:
            dt_boxes(array):detected text boxes with shape [4, 2]
        return:
            sorted boxes(array) with shape [4, 2]
        """
        num_boxes = dt_boxes.shape[0]
        sorted_boxes = sorted(dt_boxes, key=lambda x: (x[0][1], x[0][0]))
        _boxes = list(sorted_boxes)

        for i in range(num_boxes - 1):
            for j in range(i, 0, -1):
                if abs(_boxes[j + 1][0][1] - _boxes[j][0][1]) < 10 and \
                        (_boxes[j + 1][0][0] < _boxes[j][0][0]):
                    tmp = _boxes[j]
                    _boxes[j] = _boxes[j + 1]
                    _boxes[j + 1] = tmp
                else:
                    break
        return _boxes

    def __call__(self, inputs):
        outputs = []
        for idx in range(len(inputs)):
            images = inputs[idx][self.input_keys[0]]
            polys = inputs[idx][self.input_keys[1]]
            is_image_list = isinstance(images, (list, tuple))
            if is_image_list is not True:
                images = [images]
                polys = [polys]
            output = []
            # bbox: N x 4 x 2, x1,y1, x2,y2, x3,y3, x4,y4
            for image, poly, in zip(images, polys):
                crop_imgs = []
                for single_poly in poly:
                    crop_img = self.get_rotate_crop_image(image, single_poly)
                    crop_imgs.append(crop_img)
                output.append(crop_imgs)

            if is_image_list is not True:
                output = output[0]

            outputs.append({self.output_keys[0]: output, })
        return outputs


@register
class FragmentCompositionOp(ConnectorBaseOp):
    """
    FragmentCompositionOp
    """

    def __init__(self, model_cfg, env_cfg=None):
        super().__init__(model_cfg, env_cfg)
        self.split = model_cfg.get("split", " ")
        self.check_input_keys()
        return

    @classmethod
    def get_output_keys(self):
        return ["merged_text"]

    def check_input_keys(self, ):
        # list of string is needed
        assert len(
            self.input_keys
        ) == 1, f"input key of {self} must be 1 but got {len(self.input_keys)}"

    def __call__(self, inputs):
        outputs = []
        for idx in range(len(inputs)):
            strs = inputs[idx][self.input_keys[0]]
            output = self.split.join(strs)
            outputs.append(output)
        return outputs


@register
class KeyFrameExtractionOp(ConnectorBaseOp):
    """
    KeyFrameExtractionOp
    """

    def __init__(self, model_cfg, env_cfg=None):
        super().__init__(model_cfg, env_cfg)
        self.check_input_keys()
        assert model_cfg["algo"] in ["luv_diff", ]
        if model_cfg["algo"] == "luv_diff":
            self.extractor = LUVAbsDiffKeyFrameExtractor(model_cfg["params"])

    @classmethod
    def get_output_keys(self):
        return ["key_frames", "key_frames_id"]

    def check_input_keys(self, ):
        # video is needed
        assert len(
            self.input_keys
        ) == 1, f"input key of {self} must be 1 but got {len(self.input_keys)}"

    def __call__(self, inputs):
        outputs = []
        for idx in range(len(inputs)):
            input = inputs[idx][self.input_keys[0]]
            key_frames, key_frames_id = self.extractor(input)
            outputs.append([key_frames, key_frames_id])
        return outputs


@register
class TableMatcherOp(ConnectorBaseOp):
    """
    TableMatcherOp
    """

    def __init__(self, model_cfg, env_cfg=None):
        super().__init__(model_cfg, env_cfg)
        self.check_input_keys()
        filter_ocr_result = model_cfg.get("filter_ocr_result", False)
        self.matcher = TableMatcher(filter_ocr_result=filter_ocr_result)

    @classmethod
    def get_output_keys(self):
        return ["pred_html", ]

    def check_input_keys(self, ):
        #  pred_structure, pred_bboxes, dt_boxes, res_res are needed
        assert len(
            self.input_keys
        ) == 4, f"input key of {self} must be 4 but got {len(self.input_keys)}"

    def __call__(self, inputs):
        outputs = []
        for idx in range(len(inputs)):
            structure_strs = inputs[idx][self.input_keys[0]]
            structure_bboxes = inputs[idx][self.input_keys[1]]
            dt_boxes = inputs[idx][self.input_keys[2]]
            rec_res = inputs[idx][self.input_keys[3]]
            is_list = isinstance(structure_bboxes, (list, tuple))
            if is_list is not True:
                structure_strs = [structure_strs]
                structure_bboxes = [structure_bboxes]
                dt_boxes = [dt_boxes]
                rec_res = [rec_res]
            output = []
            for single_structure_strs, single_structure_bboxes, single_dt_boxes, single_rec_res, in zip(
                    structure_strs, structure_bboxes, dt_boxes, rec_res):
                pred_html = self.matcher(single_structure_strs,
                                         single_structure_bboxes,
                                         single_dt_boxes, single_rec_res)
                output.append(pred_html)
            if is_list is not True:
                output = output[0]
            outputs.append(output)
        return outputs
