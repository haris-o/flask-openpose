# python3 as runtime image
FROM python:3.6-slim-stretch
WORKDIR /app
ADD . /app

# set noninteractive mode to fix errors related to apt-get
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# add non-free packages
RUN echo "deb http://http.us.debian.org/debian stretch main non-free contrib" >> /etc/apt/sources.list && \
echo "deb-src http://http.us.debian.org/debian stretch main non-free contrib" >> /etc/apt/sources.list

# distro packages
RUN apt-get update && \
apt-get install -y cmake libopencv-dev apt-utils libatlas-base-dev wget

# caffe dependencies
RUN apt-get update && \
apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler

RUN apt-get update && \
apt-get install -y libboost-all-dev

RUN apt-get update && \
apt-get install -y libatlas-base-dev

RUN apt-get update && \
apt-get install -y libprotobuf-dev libgoogle-glog-dev libgflags-dev protobuf-compiler

RUN apt-get update && \
apt-get install -y libhdf5-serial-dev libleveldb-dev libsnappy-dev liblmdb-dev

# install requirements
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# openpose
RUN cd ./algorithms_files/openpose && \
bash ./scripts/ubuntu/install_deps_no_sudo.sh && \
cd ./build && \
cmake ../ -DBUILD_PYTHON=ON -DGPU_MODE=CPU_ONLY -DOPT_ARCH_FLAGS="" -DUSE_CUDNN=OFF -DUSE_MKL=OFF && \
make -j`nproc` && \
make install

# tf-openpose
RUN cd ./algorithms_files/tf-pose-estimation && \
python setup.py install && \
cd ./models/graph/cmu && \
bash download.sh

# expose the port used
EXPOSE 5001

# start the app
CMD ["python", "main.py"]