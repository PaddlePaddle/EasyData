# coding: utf-8
import io
from multiprocessing import Pool
import glob
import random
from PIL import ImageFont, Image, ImageDraw
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
import yaml
import os
from .utils.data_utils import GeneratorEnqueuer
from .utils.renderer import Renderer

VERSION = '1.0.0'


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_help = True
    parser.add_argument("--config", type=str, default='utils/default.yaml')
    parser.add_argument("--bg_num", type=int, default=5)
    parser.add_argument("--threads", type=int, default=5)
    parser.add_argument("--gen_num", type=int, default=10)
    parser.add_argument("--bg_img_dir", type=str, default="train_data/bg")
    parser.add_argument("--font_dir", type=str, default="train_data/fonts")
    parser.add_argument("--word_file",
                        type=str,
                        default="./train_data/corpus.txt")
    parser.add_argument("--save_dir", type=str, default='output_img')

    return parser.parse_args()


class AttrDict(dict):
    """Single level attribute dict, NOT recursive"""

    def __init__(self, **kwargs):
        super(AttrDict, self).__init__()
        super(AttrDict, self).update(kwargs)

    def __getattr__(self, key):
        if key in self:
            return self[key]
        raise AttributeError("object has no attribute '{}'".format(key))


global_config = AttrDict()


def merge_config(config):
    """
    Merge config into global config.

    Args:
    config (dict): Config to be merged.

    Returns: global config
    """
    for key, value in config.items():
        if "." not in key:
            if isinstance(value, dict) and key in global_config:
                global_config[key].update(value)
            else:
                global_config[key] = value
        else:
            sub_keys = key.split('.')
            assert (sub_keys[0] in global_config)
            cur = global_config[sub_keys[0]]
            for idx, sub_key in enumerate(sub_keys[1:]):
                assert (sub_key in cur)
                if idx == len(sub_keys) - 2:
                    cur[sub_key] = value
                else:
                    cur = cur[sub_key]


def load_config(file_path):
    """
    Load config from file.

    Args:
    file_path (str): Path of the config file to be loaded.

    Returns: global config
    """
    _, ext = os.path.splitext(file_path)
    assert ext in ['.yml', '.yaml'], "only support yaml files for now"
    merge_config(
        yaml.load(open(file_path, encoding="utf-8"), Loader=yaml.Loader))
    return global_config


def select_bg(bg_dir, number):
    filenames = os.listdir(bg_dir)
    samples = []
    num = max(1, int(number))
    pathDir = glob.glob('{}/**.*'.format(bg_dir))
    if len(pathDir) < num:
        for _ in range(num):
            sample = random.sample(pathDir, 1)
            samples.extend(sample)
    else:
        sample = random.sample(pathDir, num)
        samples.extend(sample)
    return samples


def chunker(iter, count):
    chunks = []
    if len(iter) < count:
        return iter
    size = int(np.ceil(len(iter) * 1.0 / count))
    for i in range(0, len(iter), size):
        chunks.append(iter[i:(i + size)])
    return chunks


def compute_thread_count(thread_word_list, all_count):
    len_list = np.array([len(x) for x in thread_word_list])
    ratio_list = len_list / len_list.sum()
    thread_count_list = ratio_list * all_count
    thread_count_list = thread_count_list.astype(np.int)
    remaind_count = all_count - thread_count_list.sum()
    thread_count_list[np.argmin(thread_count_list)] += remaind_count
    return thread_count_list


class GenOCR(object):
    """
    gen ocr rec data
    """

    def __init__(self, config):
        self.reader = Renderer(load_config(config))

    def gen_ocr_img(self,
                    word_list,
                    label_file,
                    save_number,
                    bg_img_dir,
                    font_path,
                    all_count,
                    bg_img_per_word_num,
                    img_save_folder,
                    delimiter="\t"):
        os.makedirs(img_save_folder, exist_ok=True)
        count = 0
        label_file = io.open(label_file, "w", encoding="utf-8")
        for word in word_list:
            bg_list = select_bg(bg_img_dir, bg_img_per_word_num)

            cur_thread_img_save_folder = '{}/{}'.format(
                img_save_folder, save_number)
            os.makedirs(cur_thread_img_save_folder, exist_ok=True)
            for bg_path in bg_list:
                start_time = time.time()
                font = random.sample(os.listdir(font_path), 1)
                try:
                    out, word = self.reader.gen_img_list(
                        word, os.path.join(font_path, font[0]), bg_path)
                except:
                    import traceback
                    traceback.print_exc()
                    continue
                out = out.astype(np.uint8)
                out = out.astype(np.int32)
                file_name = os.path.basename(bg_path)
                img_save_path = "{}/{}_{}".format(cur_thread_img_save_folder,
                                                  count, file_name)
                label_file.write("{}/{}_{}{}{}\n".format(
                    save_number, count, file_name, delimiter, word))
                cv2.imwrite(img_save_path, out[:, :, ::-1])
                label_file.flush()
                count += 1
                if count >= all_count:
                    return

    def __call__(self,
                 bg_img_dir="train_data/bg",
                 font_dir="train_data/font",
                 corpus_file="train_data/corpus.txt",
                 gen_num=10,
                 img_save_folder="output",
                 bg_img_per_word_num=5,
                 threads=5,
                 delimiter="\t"):
        with open(corpus_file, "r", encoding="utf-8") as f:
            word_list = []
            for lines in f.readlines():
                word_list.append(str(lines).replace("\n", ""))

        assert len(word_list) > 0, "Can not find any words in {}".format(
            corpus_file)
        assert len(os.listdir(
            font_dir)) > 0, "Can not find any font in {}".format(font_dir)
        assert len(os.listdir(
            bg_img_dir)) > 0, "Can not find any img in {}".format(bg_img_dir)

        if threads == 1:
            label_filename = "{}/label_{}.txt".format(img_save_folder, 0)
            print("label_file_name: {}".format(label_filename))
            self.gen_ocr_img(word_list, label_filename, 0, bg_img_dir,
                             font_dir, gen_num, bg_img_per_word_num,
                             img_save_folder, delimiter)

        elif threads > 1:
            thread_word_list = chunker(word_list, threads)
            thread_count_list = compute_thread_count(thread_word_list, gen_num)

            process_pool = Pool(threads)

            for part_id in range(0, threads):
                label_filename = "{}/label_{}.txt".format(
                    img_save_folder, part_id)

                print("label_file_name: {}".format(label_filename))

                process_pool.apply_async(
                    self.gen_ocr_img,
                    args=(thread_word_list[part_id], label_filename, part_id,
                          bg_img_dir, font_dir, thread_count_list[part_id],
                          bg_img_per_word_num, img_save_folder, delimiter))

            print('Waiting for all subprocesses done...')
            process_pool.close()
            process_pool.join()
            print('All subprocesses done.')


def main():
    args = parse_args()

    cfg = load_config(args.config)

    gen_ocr = GenOCR(cfg)

    gen_ocr(bg_img_dir="train_data/bg",
            font_dir="train_data/font",
            corpus_file="train_data/corpus.txt",
            gen_num=5,
            img_save_folder="output",
            bg_img_per_word_num=5,
            threads=1)


if __name__ == "__main__":
    main()
