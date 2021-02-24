FROM ubuntu:18.04
#FROM yangyangfu/jmodelica_py2
LABEL maintainer Yangyang Fu(yangyang.fu@tamu.edu)


# Avoid warnings
# debconf: unable to initialize frontend: Dialog
# debconf: (TERM is not set, so the dialog frontend is not usable.)
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install required packages
RUN apt-get update && \
    apt-get install -y \
    ant=1.10.5-3~18.04 \
    autoconf=2.69-11 \
    cmake=3.10.2-1ubuntu2.18.04.1 \
    cython=0.26.1-0.4 \
    g++=4:7.4.* \
    gfortran=4:7.4.0-1ubuntu2.3 \
    libgfortran3 \
    libboost-dev=1.65.1.0ubuntu1 \
    pkg-config=0.29.1-0ubuntu2 \
    python-dev=2.7.15~rc1-1 \
    python-jpype=0.6.2+dfsg-2 \
    python-lxml \
    python-matplotlib \
    python-nose \
    python-numpy=1:1.13.3-2ubuntu1 \
    python-pip=9.0.* \
    python-scipy=0.19.1-2ubuntu1 \
    subversion=1.9.7-4ubuntu1 \
    swig=3.0.12-1 \
    wget=1.19.4-1ubuntu2.2 \
    zlib1g-dev=1:1.2.11.dfsg-0ubuntu2 && \
    rm -rf /var/lib/apt/lists/*

### Add an optimization package pyomo - a wrapper for ipopt
# Get Install Ipopt and delete source code after installation
# IPOPT have different folder structures after 3.13. 
#RUN mkdir /usr/local/src
ENV SRC_DIR /usr/local/src
ENV IPOPT_3_12_13_HOME /usr/local/Ipopt-3.12.13

RUN cd $SRC_DIR && \
    wget wget -O - http://www.coin-or.org/download/source/Ipopt/Ipopt-3.12.13.tgz | tar xzf - && \
    cd $SRC_DIR/Ipopt-3.12.13/ThirdParty/Blas && \
    ./get.Blas && \
    cd $SRC_DIR/Ipopt-3.12.13/ThirdParty/Lapack && \
    ./get.Lapack && \
    cd $SRC_DIR/Ipopt-3.12.13/ThirdParty/ASL && \
    ./get.ASL && \    
    cd $SRC_DIR/Ipopt-3.12.13/ThirdParty/Mumps && \
    ./get.Mumps && \
    cd $SRC_DIR/Ipopt-3.12.13/ThirdParty/Metis && \
    ./get.Metis && \
    mkdir $SRC_DIR/Ipopt-3.12.13/build && \
    cd $SRC_DIR/Ipopt-3.12.13/build && \
    cd $SRC_DIR/Ipopt-3.12.13 && \
    ./configure --prefix=$IPOPT_3_12_13_HOME && \
    make &&\
    make install && \
    rm -rf $SRC_DIR

# specify link file location in linux
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$IPOPT_3_12_13_HOME:$IPOPT_3_12_13_HOME/lib:$IPOPT_3_12_13_HOME/bin
ENV PATH $PATH:$LD_LIBRARY_PATH

# install ipopt interface
RUN pip install pyomo

### Finish installation
# add plotting library
RUN pip install matplotlib

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/developer && \
    mkdir -p /etc/sudoers.d && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer

USER developer
ENV HOME /home/developer

# Avoid warning that Matplotlib is building the font cache using fc-list. This may take a moment.
# This needs to be towards the end of the script as the command writes data to
# /home/developer/.cache
RUN python -c "import matplotlib.pyplot"
