# Supported Runtimes: Python3.8 to Python3.11
# OS: Amazon Linux 2
# https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html

ARG PYTHON_VERSION=3.8

FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

# install dev tools
RUN yum install -y zip

# PYTHON LAYER --------------------------------------------------------------------------------
WORKDIR /tmp
COPY /tmp/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-deps -t /tmp/python
RUN find /tmp/python -type d -name "__pycache__" -exec rm -rf {} +
RUN find /tmp/python -type d -name "*.dist-info" -exec rm -rf {} +

# create layer
RUN mkdir /layers
RUN zip -r /layers/python-layer.zip ./python

# clear up
RUN rm -rf /tmp/*

# set entrypoint for debugging
ENTRYPOINT [ "tail" ]
CMD [ "-f", "/dev/null" ]
