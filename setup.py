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

from io import open
from setuptools import setup

def get_requirements():
    with open('requirements.txt', encoding="utf-8-sig") as f:
        requirements = f.readlines()
    return requirements

def get_readme():
    with open('./README.md', encoding="utf-8-sig") as f:
        readme = f.read()
    return readme


setup(
    name='easydata',
    packages=['easydata', 'easydata.deploy'],
    package_dir={'easydata': 'python_whl', 'easydata.deploy': 'deploy'},
    include_package_data=True,
    entry_points={"console_scripts": ["easydata=easydata.easydata:main"]},
    version='0.0.0',
    install_requires=get_requirements(),
    license='Apache License 2.0',
    description='A tool for improving data quality powered by PaddlePaddle.',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/PaddlePaddle/EasyData',
    download_url='https://github.com/PaddlePaddle/EasyData.git',
    # TODO(gaotingquan)
    keywords=[
        'PP-OCR',
        'PP-ShiTu',
        'PP-Human',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7', 'Topic :: Utilities'
    ],
)
