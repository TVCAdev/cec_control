FROM raspiarm32-lite:latest

ENV TOP_DIR /cec_control

RUN mkdir ${TOP_DIR}

COPY cec_control.py ${TOP_DIR}

WORKDIR ${TOP_DIR}
RUN apt-get update && apt-get install -y \
    libcec6 \
    python3-cec \
    python3-flask

CMD ["/usr/bin/python3","cec_control.py"]

