FROM continuumio/miniconda3
LABEL maintainer Yangyang Fu(yangyang.fu@tamu.edu)

#### ==================================================================================
### ====================================================================================
### install env for OPC: optimizer, nonlinear system identifier
RUN conda update conda && \
    conda config --add channels conda-forge && \
    conda install pip matplotlib

### CASADI for optimziation modeling - need add more .so files in linux
WORKDIR /opt/conda/lib/python3.8/site-packages
RUN wget --quiet https://github.com/casadi/casadi/releases/download/3.5.5/casadi-linux-py38-v3.5.5-64bit.tar.gz \
    && tar -xf *.tar.gz \
    && rm casadi-linux-py38-v3.5.5-64bit.tar.gz

### ========================================
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

