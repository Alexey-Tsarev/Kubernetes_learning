FROM alexeytsarev/centos7-base

LABEL maintainer="Alexey Tsarev <tsarev.alexey@gmail.com>"

ARG APP_DIR="/opt/redis_communicator"

WORKDIR "${APP_DIR}"

COPY redis_communicator.py requirements.txt ${APP_DIR}/

RUN echo "=> Install packages" && \
        yum -y install python3 && \
    echo "=> Install Python packages" && \
        pip3 install -r requirements.txt && \
    echo "=> Clean" && \
        yum clean all

ENTRYPOINT ["python3", "redis_communicator.py"]
