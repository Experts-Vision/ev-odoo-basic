FROM odoo:18

USER root

RUN apt update && \
    apt install -y pkg-config libcairo-dev lsof && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --break-system-packages rlPyCairo schedule

WORKDIR /ev-odoo

COPY ./custom-addons ./custom-addons
COPY ./deploy/docker/entrypoint.sh ./deploy/docker/entrypoint.sh
COPY ./deploy/license-verification ./deploy/license-verification
COPY ./run-profiles/cloud-ubuntu/env.conf ./run-profiles/cloud-ubuntu/env.conf

RUN chmod +x ./deploy/docker/entrypoint.sh

EXPOSE 8069

ENTRYPOINT ["./deploy/docker/entrypoint.sh"]
