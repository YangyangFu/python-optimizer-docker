FROM continuumio/miniconda3:latest
LABEL maintainer Yangyang Fu(yangyang.fu@tamu.edu)

### ====================================================================================
### install env for OPC: optimizer, nonlinear system identifier
RUN conda update conda && \
    conda config --add channels conda-forge && \
    conda install casadi matplotlib

# Avoid warning that Matplotlib is building the font cache using fc-list. This may take a moment.
# This needs to be towards the end of the script as the command writes data to
# /home/developer/.cache
RUN python -c "import matplotlib.pyplot"