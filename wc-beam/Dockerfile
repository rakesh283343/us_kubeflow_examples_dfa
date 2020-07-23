FROM python:3.7

LABEL maintainer="Danilo Bustos"

COPY src/wc.py wc.py
COPY data/input/words.txt /tests/input/words.txt

RUN export http_proxy=http://199.19.250.205:80 && \
    export https_proxy=$http_proxy && \
    export HTTP_PROXY=$http_proxy && \
    export HTTPS_PROXY=$http_proxy && \
    pip \
        --trusted pypi.python.org \
        --trusted-host pypi.org \
        --trusted-host files.pythonhosted.org \
        --trusted-host test.pypi.org \
        install \
        avro-python3==1.9.1 \
        pyarrow==0.16.0 \
        apache-beam

ENTRYPOINT ["python", "wc.py"]