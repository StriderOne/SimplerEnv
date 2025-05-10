# Use a base image with CUDA and cuDNN pre-installed.  Pick a specific
# version that matches your host CUDA version, if necessary, for best
# compatibility.  This example uses CUDA 11.8, matching the instructions.
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Set noninteractive to avoid prompts during package installation
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies (curl and ffmpeg)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ffmpeg \
    git \
    libvulkan1 \
    vulkan-tools \
    && \
    rm -rf /var/lib/apt/lists/*

# Install conda.  We'll use a Miniconda installer for a smaller footprint.
RUN curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    mkdir /root/.conda && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh

# Add conda to PATH
ENV PATH="/opt/conda/bin:$PATH"

# Initialize conda
RUN /opt/conda/bin/conda init

# Create the conda environment.
RUN /opt/conda/bin/conda create -n simpler_env python=3.10

# Clone the SimplerEnv repository.
RUN git clone https://github.com/simpler-env/SimplerEnv --recurse-submodules

# Install numpy (version 1.24.4)
RUN /opt/conda/envs/simpler_env/bin/pip install numpy==1.24.4

# Install ManiSkill2 real-to-sim environments and their dependencies.
RUN cd /SimplerEnv/ManiSkill2_real2sim && \
    /opt/conda/envs/simpler_env/bin/pip install -e .

# Install the SimplerEnv package itself.
RUN cd /SimplerEnv && \
    /opt/conda/envs/simpler_env/bin/pip install -e .

# Install TensorFlow with GPU support.
RUN /opt/conda/envs/simpler_env/bin/pip install tensorflow==2.15.0 && \
    /opt/conda/envs/simpler_env/bin/pip install tensorflow[and-cuda]==2.15.1

RUN /opt/conda/envs/simpler_env/bin/pip install tensorflow_datasets==4.9.4

# Install the full requirements.
RUN /opt/conda/envs/simpler_env/bin/pip install -r /SimplerEnv/requirements_full_install.txt

# Install server dependencies.
RUN /opt/conda/envs/simpler_env/bin/pip install uvicorn \
    fastapi \
    json-numpy \
    draccus

RUN mkdir /SimplerEnv/checkpoints

# Set the working directory.
WORKDIR /SimplerEnv

COPY simpler_env/deploy.py deploy.py

EXPOSE 8000

# Optionally, specify a command to run when the container starts.
CMD ["/bin/bash"]
