#ARG BASE_IMAGE=tensorflow/tensorflow:latest-gpu
ARG BASE_IMAGE=nvidia/cuda:12.0.1-devel-ubuntu22.04
FROM ${BASE_IMAGE} as dev-base

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND noninteractive

ENV SHELL=/bin/bash

ENV HF_DATASETS_CACHE=/workspace/.cache/huggingface
ENV XDG_CACHE_HOME=/workspace/.cache


RUN apt-get update &&  apt-get -y install python3-pip git sudo curl nvidia-cuda-toolkit nvidia-cuda-toolkit-gcc  &&  apt-get clean
RUN mkdir /workspace   &&  chown 1000 /workspace
RUN useradd -u 1000 -ms /bin/bash ubuntu
WORKDIR /home/ubuntu
RUN echo "ubuntu ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER 1000
ENV PATH=/home/ubuntu/.local/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV HOME=/home/ubuntu
ENV PYDEVD_DISABLE_FILE_VALIDATION=1
RUN sudo apt-get install -y cuda-nvcc-12-0
RUN git clone https://github.com/TimDettmers/bitsandbytes.git \
   &&  cd bitsandbytes \
   &&  export CUDA_HOME=/usr/local/cuda-12.0 \
   &&  make cuda12x CUDA_VERSION=120 \
   &&  export CUDA_HOME=/usr/local/cuda-12.0 \
   &&  make cuda12x_nomatmul CUDA_VERSION=120 \
   &&  CUDA_VERSION=120 \
   &&  sudo python3 setup.py install \
   &&  cd .. \
   &&  sudo rm -rf bitsandbytes

RUN mkdir -p /home/ubuntu/.ssh \
   &&  echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC8EPxrWEBui9FnQWlxVWbClA6Fi20zHDwfLcSvVcl4MQBcWc+obTQwIdQ3NGtOfdOFrmEZJtZZo7tuaDXEqbRXiGAvuJpaNYEzFSC9MQfA3Zvv3LaMyfXYgpm9/tG63+iST7inIxnvuwwu3lQK9dlMl4mL5e7onA3dbfIMtfSLKk065qsUqo7Se33IrGT7+2iJZajPWWTS5tE53MlVQ/d8i/xSW4ADkJQb/beLo8C53ZPXN4YdGcqiPjdVpK45IqfraXGK3QgQjy1Gq2BI22A3t4mFG2K4lHMxowFkZyNoHWNI/ADtlY2qUdOELEcXoZfp3OR99EFJxka7j/GKDqzxfoE7tbBe8aNJwYIZACV3PnIj/OZBaEMndj1/PUPXaLLXw+pcnDpK9PgcRvN5+79koMcv8czJODUFe60lZzJB3BjPqtQ3UqtLH9NcMKYGgEQezkt66MZcON6vH8XTbxNJPAO32sI3fgflojiysylhaK1UDVe0MOzfIFseA2/rM9JFZpK5Z+55QagqXBSpbSlrOyE5gxvtOEk8qmP2Uxb3bkfIY8FGUp0GMU/XLd37wAGFdG8Atsz57WvYWSGwvrvXXmLyLxr925rjzS468B9ernMZHbXTzI01T9m+W6XzsuS9nBUJMNfhRcbMfGdye5MBs6w7MzxZr9h5OTHvntom3w== fishdaemon@fishdaemon" >/home/ubuntu/.ssh/authorized_keys
RUN sudo apt-get install -y openssh-server vim-tiny
RUN sudo sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN sudo mkdir /var/run/sshd
RUN sudo bash -c 'install -m755 <(printf "#!/bin/sh\nexit 0") /usr/sbin/policy-rc.d'
RUN sudo ex +'%s/^#\zeListenAddress/\1/g' -scwq /etc/ssh/sshd_config
RUN sudo ex +'%s/^#\zeHostKey .*ssh_host_.*_key/\1/g' -scwq /etc/ssh/sshd_config
RUN RUNLEVEL=1 sudo dpkg-reconfigure openssh-server
RUN sudo ssh-keygen -A -v
RUN sudo update-rc.d ssh defaults
RUN sudo mkdir -p /workspace \
   &&  sudo chown ubuntu /workspace \
   &&  sudo ln -s /workspace /content
ENV HF_DATASETS_CACHE=/workspace/.cache/huggingface
ENV XDG_CACHE_HOME=/workspace/.cache
WORKDIR /workspace
RUN curl -sL "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" > "Miniconda3.sh"
RUN bash Miniconda3.sh -b
RUN sudo apt-get -y remove pipenv \
   &&  pip install pipenv
RUN echo "export PIPENV_VENV_IN_PROJECT=1" >> /home/ubuntu/.bashrc
#CMD ["/bin/sh" "-c" "/usr/bin/sudo /usr/sbin/sshd -D -o ListenAddress=0.0.0.0 & jupyter notebook --NotebookApp.allow_origin='https://colab.research.google.com' --ip=0.0.0.0 --port=8888 --NotebookApp.port_retries=0 --NotebookApp.disable_check_xsrf=True --no-browser"]
COPY ./start.sh /start.sh
RUN sudo chmod +x /start.sh
CMD /start.sh



#RUN apt-key del 7fa2af80
#RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
#RUN apt-get update --yes && \
#    # - apt-get upgrade is run to patch known vulnerabilities in apt-get packages as
#    #   the ubuntu base image is rebuilt too seldom sometimes (less than once a month)
#    apt-get upgrade --yes && \
#    apt install --yes --no-install-recommends\
#    wget\
#    bash\
#    openssh-server &&\
#    apt-get clean && rm -rf /var/lib/apt/lists/* && \
#    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
#
#
#RUN /usr/bin/python3 -m pip install --upgrade pip
#RUN pip install jupyterlab
#RUN pip install ipywidgets
#RUN pip install pipenv