"""
This code is refer from:
https://github.com/Sanster/text_renderer/blob/master/textrenderer/renderer.py
"""

import math
import random
import numpy as np
import cv2
from PIL import ImageFont, Image, ImageDraw

from .math_utils import cliped_rand_norm, PerspectiveTransform
from .liner import Liner
from .remaper import Remaper
from .noiser import Noiser


def draw_box(img, pnts, color):
    """
    :param img: gray image, will be convert to BGR image
    :param pnts: left-top, right-top, right-bottom, left-bottom
    :param color:
    :return:
    """
    if isinstance(pnts, np.ndarray):
        pnts = pnts.astype(np.int32)

    if len(img.shape) > 2:
        dst = img
    else:
        dst = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    thickness = 1
    linetype = cv2.LINE_AA
    cv2.line(dst, (pnts[0][0], pnts[0][1]), (pnts[1][0], pnts[1][1]),
             color=color,
             thickness=thickness,
             lineType=linetype)
    cv2.line(dst, (pnts[1][0], pnts[1][1]), (pnts[2][0], pnts[2][1]),
             color=color,
             thickness=thickness,
             lineType=linetype)
    cv2.line(dst, (pnts[2][0], pnts[2][1]), (pnts[3][0], pnts[3][1]),
             color=color,
             thickness=thickness,
             lineType=linetype)
    cv2.line(dst, (pnts[3][0], pnts[3][1]), (pnts[0][0], pnts[0][1]),
             color=color,
             thickness=thickness,
             lineType=linetype)
    return dst


def draw_bbox(img, bbox, color):
    pnts = [[bbox[0], bbox[1]], [bbox[0] + bbox[2], bbox[1]],
            [bbox[0] + bbox[2], bbox[1] + bbox[3]],
            [bbox[0], bbox[1] + bbox[3]]]
    return draw_box(img, pnts, color)


def prob(percent):
    """
    percent: 0 ~ 1, e.g: 如果 percent=0.1，有 10% 的可能性
    """
    assert 0 <= percent <= 1
    if random.uniform(0, 1) <= percent:
        return True
    return False


def apply(cfg_item):
    """
    :param cfg_item: a sub cfg item in default.yml, it should contain enable and fraction. such as
                prydown:
                    enable: true
                    fraction: 0.03
    :return: True/False
    """
    enable = cfg_item['enable']
    fraction = cfg_item['fraction']
    if enable and prob(fraction):
        return True
    return False


class Renderer():

    def __init__(self, cfg, height=48):
        self.cfg = cfg
        self.out_width = 0
        self.out_height = height
        self.liner = Liner(cfg)
        self.remaper = Remaper(cfg)
        self.noiser = Noiser(cfg)
        self.debug = False
        self.create_kernals()

    def gen_img_list(self, word, font_path, bg_img_path):
        self.out_height = self.cfg['img_size']['h']
        font_size = random.randint(self.cfg['font_size']['min'],
                                   self.cfg['font_size']['max'])
        font = ImageFont.truetype(font_path, font_size)
        word_size = self.get_word_size(font, word)

        # Background's height should much larger than raw word image's height,
        # to make sure we can crop full word image after apply perspective

        bg = self.gen_bg(bg_img_path,
                         width=word_size[0] * 8,
                         height=word_size[1] * 8)
        word_img, text_box_pnts, word_color = self.draw_text_on_bg(
            word, font, bg)
        self.dmsg("After draw_text_on_bg")

        if apply(self.cfg['crop']):
            text_box_pnts = self.apply_crop(text_box_pnts, self.cfg['crop'])

        if apply(self.cfg['line']):
            word_img, text_box_pnts = self.liner.apply(word_img.copy(),
                                                       text_box_pnts,
                                                       word_color)
            self.dmsg("After draw line")

        if self.debug:
            word_img = draw_box(word_img, text_box_pnts, (0, 255, 155))
            # pass
        if apply(self.cfg['curve']):
            word_img, text_box_pnts = self.remaper.apply(
                word_img, text_box_pnts, word_color)

        if self.debug:
            word_img = draw_box(word_img, text_box_pnts, (155, 255, 0))

        word_img, img_pnts_transformed, text_box_pnts_transformed = \
            self.apply_perspective_transform(word_img, text_box_pnts,
                                             max_x=self.cfg['perspective_transform']['max_x'],
                                             max_y=self.cfg['perspective_transform']['max_y'],
                                             max_z=self.cfg['perspective_transform']['max_z'])
        self.dmsg("After perspective transform")

        if self.debug:
            _, crop_bbox = self.crop_img(word_img, text_box_pnts_transformed)
            word_img = draw_bbox(word_img, crop_bbox, (255, 0, 0))
        else:
            word_img, crop_bbox = self.crop_img(word_img,
                                                text_box_pnts_transformed)

        if apply(self.cfg['noise']):
            word_img = np.clip(word_img, 0., 255.)
            word_img = self.noiser.apply(word_img)

        blured = False
        if apply(self.cfg['blur']):
            blured = True
            word_img = self.apply_blur_on_output(word_img)
            self.dmsg("After blur")

        if not blured:
            if apply(self.cfg['prydown']):
                word_img = self.apply_prydown(word_img)
                self.dmsg("After prydown")

        word_img = np.clip(word_img, 0., 255.)

        if apply(self.cfg['reverse_color']):
            word_img = self.reverse_img(word_img)
            self.dmsg("After reverse_img")

        if apply(self.cfg['emboss']):
            word_img = self.apply_emboss(word_img)
            self.dmsg("After emboss")

        if apply(self.cfg['sharp']):
            word_img = self.apply_sharp(word_img)
            self.dmsg("After sharp")

        return word_img, word

    def dmsg(self, msg):
        if self.debug:
            print(msg)

    def get_word_size(self, font, word):
        """
        Get word size removed offset
        :param font: truetype
        :param word:
        :return:
            size: word size, removed offset (width, height)
        """
        offset = font.getoffset(word)
        size = font.getsize(word)
        size = (size[0] - offset[0], size[1] - offset[1])
        return size

    def random_xy_offset(self, src_height, src_width, dst_height, dst_width):
        """
        Get random left-top point for putting a small rect in a large rect.
        Normally dst_height>src_height and dst_width>src_width
        """
        y_max_offset = 0
        if dst_height > src_height:
            y_max_offset = dst_height - src_height

        x_max_offset = 0
        if dst_width > src_width:
            x_max_offset = dst_width - src_width

        y_offset = 0
        if y_max_offset != 0:
            y_offset = random.randint(0, y_max_offset)

        x_offset = 0
        if x_max_offset != 0:
            x_offset = random.randint(0, x_max_offset)

        return x_offset, y_offset

    def crop_img(self, img, text_box_pnts_transformed):
        """
        Crop text from large input image
        :param img: image to crop
        :param text_box_pnts_transformed: text_bbox_pnts after apply_perspective_transform
        :return:
            dst: image with desired output size, height=32, width=flags.img_width
            crop_bbox: bounding box on input image
        """
        bbox = cv2.boundingRect(text_box_pnts_transformed)
        bbox_width = bbox[2]
        bbox_height = bbox[3]

        # Output shape is (self.out_width, self.out_height)
        # We randomly put bounding box of transformed text in the output shape
        # so the max value of dst_height is out_height

        # TODO: If rotate angle(z) of text is too big, text will become very small,
        # we should do something to prevent text too small

        # dst_height and dst_width is used to leave some padding around text bbox
        # dst_height = random.randint(self.out_height // 4 * 3, self.out_height)
        dst_height = self.out_height
        if self.out_width == 0:
            scale = bbox_height / dst_height
        else:
            dst_width = self.out_width
            scale = max(bbox_height / dst_height, bbox_width / self.out_width)
        s_bbox_width = math.ceil(bbox_width / scale)
        s_bbox_height = math.ceil(bbox_height / scale)

        if self.out_width == 0:
            padding = random.randint(s_bbox_width // 18, s_bbox_width // 15)
            dst_width = s_bbox_width

        s_bbox = (np.around(bbox[0] / scale), np.around(bbox[1] / scale),
                  np.around(bbox[2] / scale), np.around(bbox[3] / scale))

        x_offset, y_offset = self.random_xy_offset(s_bbox_height, s_bbox_width,
                                                   self.out_height, dst_width)
        dst_bbox = (self.int_around((s_bbox[0] - x_offset) * scale),
                    self.int_around((s_bbox[1] - y_offset) * scale),
                    self.int_around(dst_width * scale),
                    self.int_around(self.out_height * scale))

        dst_bbox = (self.int_around((s_bbox[0] - x_offset) * scale),
                    self.int_around((s_bbox[1] - y_offset) * scale),
                    self.int_around(dst_width * scale),
                    self.int_around(self.out_height * scale))

        # It's important do crop first and than do resize for speed consider
        dst = img[dst_bbox[1]:dst_bbox[1] + dst_bbox[3],
                  dst_bbox[0]:dst_bbox[0] + dst_bbox[2]]
        dst = cv2.resize(dst, (dst_width, self.out_height),
                         interpolation=cv2.INTER_CUBIC)

        return dst, dst_bbox

    def int_around(self, val):
        return int(np.around(val))

    def get_gray_word_color(self, bg, text_x, text_y, word_height, word_width):
        """
        Only use word roi area to get word color
        """
        offset = 10
        ymin = text_y - offset
        ymax = text_y + word_height + offset
        xmin = text_x - offset
        xmax = text_x + word_width + offset

        word_roi_bg = bg[ymin:ymax, xmin:xmax]

        bg_mean = int(np.mean(word_roi_bg) * (2 / 3))
        word_color = random.randint(0, bg_mean)
        return word_color

    def get_word_color(self):
        p = []
        colors = []
        for k, v in self.cfg['font_color'].items():
            if k == 'enable':
                continue
            p.append(v['fraction'])
            colors.append(k)

        # pick color by fraction
        color_name = np.random.choice(colors, p=p)
        l_boundary = self.cfg.font_color[color_name]['l_boundary']
        h_boundary = self.cfg.font_color[color_name]['h_boundary']
        # random color by low and high RGB boundary
        r = np.random.randint(l_boundary[0], h_boundary[0])
        g = np.random.randint(l_boundary[1], h_boundary[1])
        b = np.random.randint(l_boundary[2], h_boundary[2])
        return b, g, r

    def draw_text_on_bg(self, word, font, bg):
        """
        Draw word in the center of background
        :param word: word to draw
        :param font: font to draw word
        :param bg: background numpy image
        :return:
            np_img: word image
            text_box_pnts: left-top, right-top, right-bottom, left-bottom
        """
        if apply(self.cfg['random_direction']):
            bg_height = bg.shape[0]
            bg_width = bg.shape[1]

            word_size = self.get_word_size(font, word)
            word_height = word_size[1]
            word_width = word_size[0]

            offset = font.getoffset(word)

            pil_img = Image.fromarray(np.uint8(bg))
            draw = ImageDraw.Draw(pil_img)

            # Draw text in the center of bg
            text_x = int((bg_width - word_width) / 2)
            text_y = int((bg_height - word_height) / 2)

            if self.is_bgr():
                word_color = self.get_word_color()
            else:
                word_color = self.get_gray_word_color(bg, text_x, text_y,
                                                      word_height, word_width)
            if apply(self.cfg['random_space']) and len(word) < 6:
                text_x, text_y, word_width, _ = \
                    self.draw_text_with_random_space(
                        draw, font, word, word_color, bg_width, bg_height, "horizon")
                np_img = np.array(pil_img)
            else:
                if apply(self.cfg['seamless_clone']):
                    np_img = self.draw_text_seamless(font, bg, word,
                                                     word_color, word_height,
                                                     word_width, offset)
                else:
                    self.draw_text_wrapper(draw, word, text_x - offset[0],
                                           text_y - offset[1], font,
                                           word_color)

                    np_img = np.array(pil_img)

            text_box_pnts = [[text_x, text_y], [text_x + word_width, text_y],
                             [text_x + word_width, text_y + word_height],
                             [text_x, text_y + word_height]]

            return np_img, text_box_pnts, word_color
        else:
            v_bg = np.rot90(bg, -1)
            bg_height = v_bg.shape[0]
            bg_width = v_bg.shape[1]

            word_size = self.get_word_size(font, word)
            word_height = word_size[1]
            word_width = word_size[0]

            offset = font.getoffset(word)

            pil_img = Image.fromarray(np.uint8(v_bg))

            draw = ImageDraw.Draw(pil_img)

            # Draw text in the center of bg
            text_x = int((bg_width - word_width / len(word)) / 2)
            text_y = int((bg_height - word_height) / 2)

            leftx, lefty, rightx, righty = 0, 0, 0, 0

            if self.is_bgr():
                word_color = self.get_word_color()
            else:
                word_color = self.get_gray_word_color(v_bg, text_x, text_y,
                                                      word_height, word_width)

            if apply(self.cfg.random_space):
                text_x, text_y, word_width, word_height = self.draw_text_with_random_space(
                    draw, font, word, word_color, bg_width, bg_height,
                    "vertical")
                h_bg = np.rot90(pil_img, 1)
                leftx, lefty = text_y, text_x
                rightx, righty = leftx + word_height, lefty + word_width
                np_img = np.array(h_bg).astype(np.float32)
            else:
                startx, starty = text_x - offset[0], text_y - offset[1]
                leftx, lefty = int(starty), int(startx)
                border_color = None
                if apply(self.cfg['text_border']):
                    for item in word:
                        border_color = self.draw_border_text(
                            draw, item, startx, starty, font, word_color,
                            border_color)
                        starty += word_height
                else:
                    for item in word:
                        draw.text((startx, starty),
                                  item,
                                  fill=word_color,
                                  font=font)
                        starty += word_height

                rightx = int(starty) + word_height
                righty = int(lefty + font.getsize(word[0])[0])

                h_bg = np.rot90(pil_img, 1)
                np_img = np.array(h_bg).astype(np.float32)

            text_box_pnts = [[leftx, lefty], [rightx, lefty], [rightx, righty],
                             [leftx, righty]]

            return np_img, text_box_pnts, word_color

    def draw_text_seamless(self, font, bg, word, word_color, word_height,
                           word_width, offset):
        # For better seamlessClone
        seamless_offset = 6

        # Draw text on a white image, than draw it on background
        if self.is_bgr():
            white_bg = np.ones((word_height + seamless_offset,
                                word_width + seamless_offset, 3)) * 255
        else:
            white_bg = np.ones((word_height + seamless_offset,
                                word_width + seamless_offset)) * 255

        text_img = Image.fromarray(np.uint8(white_bg))
        draw = ImageDraw.Draw(text_img)

        self.draw_text_wrapper(draw, word, 0 + seamless_offset // 2,
                               0 - offset[1] + seamless_offset // 2, font,
                               word_color)

        # assume whole text_img as mask
        text_img = np.array(text_img).astype(np.uint8)
        text_mask = 255 * np.ones(text_img.shape, text_img.dtype)

        # This is where the CENTER of the airplane will be placed
        center = (bg.shape[1] // 2, bg.shape[0] // 2)

        # opencv seamlessClone require bgr image
        if not self.is_bgr():
            text_img_bgr = np.ones((text_img.shape[0], text_img.shape[1], 3),
                                   np.uint8)
            bg_bgr = np.ones((bg.shape[0], bg.shape[1], 3), np.uint8)
            cv2.cvtColor(text_img, cv2.COLOR_GRAY2BGR, text_img_bgr)
            cv2.cvtColor(bg, cv2.COLOR_GRAY2BGR, bg_bgr)
        else:
            text_img_bgr = text_img
            bg_bgr = bg

        flag = np.random.choice(
            [cv2.NORMAL_CLONE, cv2.MIXED_CLONE, cv2.MONOCHROME_TRANSFER])

        mixed_clone = cv2.seamlessClone(text_img_bgr, bg_bgr, text_mask,
                                        center, flag)

        if not self.is_bgr():
            return cv2.cvtColor(mixed_clone, cv2.COLOR_BGR2GRAY)
        else:
            return mixed_clone

    def draw_text_with_random_space(self, draw, font, word, word_color,
                                    bg_width, bg_height, dir):
        """ If random_space applied, text_x, text_y, word_width, word_height may change"""
        if dir == 'horizon':
            width = 0
            height = 46
            chars_size = []
            y_offset = 10**5
            y_offset = 46
            for c in word:
                size = font.getsize(c)
                chars_size.append(size)

                width += size[0]

                # Min chars y offset as word y offset
                # Assume only y offset
                c_offset = font.getoffset(c)
                if c_offset[1] < y_offset:
                    y_offset = c_offset[1]
            space = np.random.uniform(self.cfg['random_space']['min'],
                                      self.cfg['random_space']['max'])
            char_space_width = int(height * space)

            width += (char_space_width * (len(word) - 1))

            text_x = int((bg_width - width) / 2)
            text_y = int((bg_height - height) / 2)

            c_x = text_x
            c_y = text_y
            for i, c in enumerate(word):
                draw.text((c_x, c_y - y_offset), c, fill=word_color, font=font)

                c_x += (chars_size[i][0] + char_space_width)
            return text_x, text_y, width, height
        elif dir == "vertical":
            width = 0
            height = 0
            chars_size = []
            x_offset = 46
            for c in word:
                size = font.getsize(c)
                chars_size.append(size)

                height += size[1]

                # Min chars y offset as word y offset
                # Assume only y offset
                c_offset = font.getoffset(c)
                if c_offset[0] < x_offset:
                    x_offset = c_offset[0]

            char_space_height = int(width * np.random.uniform(
                self.cfg.random_space.min, self.cfg.random_space.max))
            height += (char_space_height * (len(word) - 1))

            text_x = int((bg_width - width) / 2)
            text_y = int((bg_height - height) / 2)

            c_x = text_x
            c_y = text_y
            for i, c in enumerate(word):
                draw.text((c_x - x_offset, c_y), c, fill=word_color, font=font)
                c_y += (chars_size[i][1] + char_space_height)

            return text_x, text_y, width, height

    def draw_text_wrapper(self, draw, text, x, y, font, text_color):
        """
        :param x/y: 应该是移除了 offset 的
        """
        if apply(self.cfg['text_border']):
            self.draw_border_text(draw, text, x, y, font, text_color)
        else:
            draw.text((x, y), text, fill=text_color, font=font)

    def draw_border_text(self,
                         draw,
                         text,
                         x,
                         y,
                         font,
                         text_color,
                         border_color=None):
        """
        :param x/y: 应该是移除了 offset 的
        """
        # thickness larger than 1 may give bad border result
        thickness = 1

        choices = []
        p = []
        if border_color == None:
            if self.cfg['text_border']['light']['enable']:
                choices.append(0)
                p.append(self.cfg['text_border']['light']['fraction'])
            if self.cfg['text_border']['dark']['enable']:
                choices.append(1)
                p.append(self.cfg['text_border']['dark']['fraction'])

            light_or_dark = np.random.choice(choices, p=p)

            if light_or_dark == 0:
                if self.is_bgr():
                    border_color = (
                        text_color[0] +
                        np.random.randint(0, 255 - text_color[0] - 1),
                        text_color[1] +
                        np.random.randint(0, 255 - text_color[1] - 1),
                        text_color[2] +
                        np.random.randint(0, 255 - text_color[2] - 1))
                else:
                    border_color = text_color + np.random.randint(
                        0, 255 - text_color - 1)
            elif light_or_dark == 1:
                if self.is_bgr():
                    border_color = (text_color[0] -
                                    np.random.randint(0, text_color[0] + 1),
                                    text_color[1] -
                                    np.random.randint(0, text_color[1] + 1),
                                    text_color[2] -
                                    np.random.randint(0, text_color[2] + 1))
                else:
                    border_color = text_color - np.random.randint(
                        0, text_color + 1)

        # thin border
        draw.text((x - thickness, y), text, font=font, fill=border_color)
        draw.text((x + thickness, y), text, font=font, fill=border_color)
        draw.text((x, y - thickness), text, font=font, fill=border_color)
        draw.text((x, y + thickness), text, font=font, fill=border_color)

        # thicker border
        draw.text((x - thickness, y - thickness),
                  text,
                  font=font,
                  fill=border_color)
        draw.text((x + thickness, y - thickness),
                  text,
                  font=font,
                  fill=border_color)
        draw.text((x - thickness, y + thickness),
                  text,
                  font=font,
                  fill=border_color)
        draw.text((x + thickness, y + thickness),
                  text,
                  font=font,
                  fill=border_color)

        # now draw the text over it
        draw.text((x, y), text, font=font, fill=text_color)
        return border_color

    def gen_bg(self, bg_img_path, width, height):
        if apply(self.cfg['img_bg']):
            try:
                bg = self.gen_bg_from_image(bg_img_path, int(width),
                                            int(height))
            except:
                bg = self.gen_rand_bg(int(width), int(height))
        else:
            bg = self.gen_rand_bg(int(width), int(height))
        return bg

    def gen_rand_bg(self, width, height):
        """
        Generate random background
        """
        bg_high = random.uniform(220, 255)
        bg_low = bg_high - random.uniform(1, 60)

        bg = np.random.randint(bg_low, bg_high,
                               (height, width)).astype(np.uint8)
        bg = self.apply_gauss_blur(bg)
        if self.is_bgr():
            bg = cv2.cvtColor(bg, cv2.COLOR_GRAY2BGR)
        return bg

    def gen_bg_from_image(self, bg_img_path, width, height):
        """
        Resize background, let bg_width>=width, bg_height >=height, and random crop from resized background
        """
        assert width > height
        bg = cv2.imread(bg_img_path)
        scale = max(width / bg.shape[1], height / bg.shape[0])
        out = cv2.resize(bg, None, fx=scale, fy=scale)
        x_offset, y_offset = self.random_xy_offset(height, width, out.shape[0],
                                                   out.shape[1])
        out = out[y_offset:y_offset + height, x_offset:x_offset + width]
        out = self.apply_gauss_blur(out, ks=[7, 11, 13, 15, 17])
        bg_mean = int(np.mean(out))
        alpha = 255 / bg_mean  # 对比度
        beta = np.random.randint(bg_mean // 4, bg_mean // 2)  # 亮度
        out = np.uint8(np.clip((alpha * out + beta), 0, 255))
        return out

    def pick_font(self, img_index):
        """
        :param img_index when use list corpus, this param is used
        :return:
            font: truetype
            size: word size, removed offset (width, height)
        """
        word = self.corpus.get_sample(img_index)

        if self.clip_max_chars and len(word) > self.max_chars:
            word = word[:self.max_chars]

        font_path = random.choice(self.fonts)

        if self.strict:
            unsupport_chars = self.font_unsupport_chars[font_path]
            for c in word:
                if c == ' ':
                    continue
                if c in unsupport_chars:
                    print(
                        'Retry pick_font(), \'%s\' contains chars \'%s\' not supported by font %s'
                        % (word, c, font_path))
                    raise Exception

        # Font size in point
        font_size = random.randint(self.cfg.font_size.min,
                                   self.cfg.font_size.max)
        font = ImageFont.truetype(font_path, font_size)

        return word, font, self.get_word_size(font, word)

    def apply_perspective_transform(self,
                                    img,
                                    text_box_pnts,
                                    max_x,
                                    max_y,
                                    max_z,
                                    gpu=False):
        """
        Apply perspective transform on image
        :param img: origin numpy image
        :param text_box_pnts: four corner points of text
        :param x: max rotate angle around X-axis
        :param y: max rotate angle around Y-axis
        :param z: max rotate angle around Z-axis
        :return:
            dst_img:
            dst_img_pnts: points of whole word image after apply perspective transform
            dst_text_pnts: points of text after apply perspective transform
        """

        x = cliped_rand_norm(0, max_x)
        y = cliped_rand_norm(0, max_y)
        z = cliped_rand_norm(0, max_z)

        # print("x: %f, y: %f, z: %f" % (x, y, z))

        transformer = PerspectiveTransform(x, y, z, scale=1.0, fovy=50)

        dst_img, M33, dst_img_pnts = transformer.transform_image(img, gpu)
        dst_text_pnts = transformer.transform_pnts(text_box_pnts, M33)

        return dst_img, dst_img_pnts, dst_text_pnts

    def apply_blur_on_output(self, img):
        if prob(0.5):
            return self.apply_gauss_blur(img, [3, 5])
        else:
            return self.apply_norm_blur(img)

    def apply_gauss_blur(self, img, ks=None):
        if ks is None:
            ks = [7, 9, 11, 13]
        ksize = random.choice(ks)

        sigmas = [0, 1, 2, 3, 4, 5, 6, 7]
        sigma = 0
        if ksize <= 3:
            sigma = random.choice(sigmas)
        # print("img:",img)
        img = cv2.GaussianBlur(img, (ksize, ksize), sigma)
        return img

    def apply_norm_blur(self, img, ks=None):
        # kernel == 1, the output image will be the same
        if ks is None:
            ks = [2, 3]
        kernel = random.choice(ks)
        img = cv2.blur(img, (kernel, kernel))
        return img

    def apply_prydown(self, img):
        """
        模糊图像，模拟小图片放大的效果
        """
        scale = random.uniform(1, self.cfg['prydown']['max_scale'])
        height = img.shape[0]
        width = img.shape[1]

        out = cv2.resize(img, (int(width / scale), int(height / scale)),
                         interpolation=cv2.INTER_AREA)
        return cv2.resize(out, (width, height), interpolation=cv2.INTER_AREA)

    def reverse_img(self, word_img):
        offset = np.random.randint(-10, 10)
        return 255 + offset - word_img

    def create_kernals(self):
        self.emboss_kernal = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])

        self.sharp_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

    def apply_emboss(self, word_img):
        return cv2.filter2D(word_img, -1, self.emboss_kernal)

    def apply_sharp(self, word_img):
        return cv2.filter2D(word_img, -1, self.sharp_kernel)

    def apply_crop(self, text_box_pnts, crop_cfg):
        """
        Random crop text box height top or bottom, we don't need image information in this step, only change box pnts
        :param text_box_pnts: bbox of text [left-top, right-top, right-bottom, left-bottom]
        :param crop_cfg:
        :return:
            croped_text_box_pnts
        """
        height = abs(text_box_pnts[0][1] - text_box_pnts[3][1])
        scale = float(height) / float(self.out_height)

        croped_text_box_pnts = text_box_pnts

        if prob(0.5):
            top_crop = int(
                random.randint(crop_cfg['top']['min'], crop_cfg['top']['max'])
                * scale)
            croped_text_box_pnts[0][1] += top_crop
            croped_text_box_pnts[1][1] += top_crop
        else:
            bottom_crop = int(
                random.randint(crop_cfg['bottom']['min'],
                               crop_cfg['bottom']['max']) * scale)
            croped_text_box_pnts[2][1] -= bottom_crop
            croped_text_box_pnts[3][1] -= bottom_crop

        return croped_text_box_pnts

    def is_bgr(self):
        return self.cfg['font_color']['enable'] or self.cfg['line_color'][
            'enable']
