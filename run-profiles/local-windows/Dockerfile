FROM odoo:18

USER root

RUN apt update && \
    apt install -y pkg-config libcairo-dev libcairo-dev lsof sed && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --break-system-packages rlPyCairo schedule openpyxl ofxparse qifparse

WORKDIR /ev-odoo

COPY ./license ./license
COPY ./dependencies ./dependencies
COPY ./ev_addons ./ev_addons
COPY ./deploy/docker/entrypoint.sh ./deploy/docker/entrypoint.sh
COPY ./deploy/license-verification ./deploy/license-verification
COPY ./run-profiles/local-windows/env.conf ./run-profiles/local-windows/env.conf

RUN sed -i 's/\r$//' /ev-odoo/deploy/docker/entrypoint.sh && \
    chmod +x /ev-odoo/deploy/docker/entrypoint.sh

EXPOSE 8069

ENTRYPOINT ["/ev-odoo/deploy/docker/entrypoint.sh"]