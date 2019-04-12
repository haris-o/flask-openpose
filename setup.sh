#!/usr/bin/env bash

# clone the tf-openpose repository
cd ./algorithms_files
git clone https://www.github.com/ildoonet/tf-pose-estimation

# clone the openpose repository
git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose

# avoid the compilation error by manually cloning the caffe repo
cd ./openpose/3rdparty
git clone https://github.com/CMU-Perceptual-Computing-Lab/caffe.git
