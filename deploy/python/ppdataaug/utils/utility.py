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

parent = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(parent, '../deploy/')))

from python.ppdataaug.utils import logger


def get_label(data_file, delimiter=" "):
    all_label = {}
    with open(data_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            path, label = line.strip().split(delimiter)
            path = path.split("/")[-1]
            all_label[path] = label
    return all_label


def rm_repeat(all_label, save_list, compare_file, out_file, thresh, delimiter):
    count = 0
    with open(out_file, "w", encoding="utf-8") as new_aug_file:
        with open(compare_file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                query = line.strip().split("\t")[0]
                gallery = line.strip().split("\t")[1:-1]
                score = line.strip().split("\t")[-1]
                path = query.split("/")[-1]
                if float(score) > thresh and (gallery
                                              or query) not in save_list:
                    count += 1
                    save_list.append(gallery)
                    save_list.append(query)
                    new_aug_file.write(query + delimiter +
                                       str(all_label[path]) + "\n")
                elif float(score) < thresh:
                    count += 1
                    save_list.append(query)
                    new_aug_file.write(query + delimiter +
                                       str(all_label[path]) + "\n")
    return count


def check_dir(path):
    if len(os.path.dirname(path)) < 1:
        return
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    return


def concat_file(label_dir, all_file):
    filenames = os.listdir(label_dir)
    assert len(filenames) > 0, "Can not find any file in {}".format(label_dir)
    check_dir(all_file)
    f = open(all_file, 'w', encoding="utf-8")
    for filename in filenames:
        if os.path.isfile(os.path.join(label_dir, filename)):
            logger.info("{} will be merged to {}".format(filename, all_file))
            filepath = label_dir + '/' + filename
            for line in open(filepath, encoding="utf-8"):
                if len(line) != 0:
                    f.writelines(line)
        else:
            continue
    f.close()
    return all_file
