#!/usr/bin/env bash

# clone the tf-openpose repository
cd ./algorithms_files
git clone https://www.github.com/ildoonet/tf-pose-estimation

# clone the openpose repository
git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose
cd ./openpose
git submodule update --init --recursive

# avoid the compilation error by manually cloning the caffe repo
cd ./3rdparty
git clone https://github.com/CMU-Perceptual-Computing-Lab/caffe.git
