
# Experts Vision Odoo Basic  
  
A basic Odoo configuration for basic requirements customers.

---

## Key files

### Odoo Files

- `custom-addons`
  - It contains the custom Odoo modules.
  - It will be copied to the Docker image.

### License Verification Files

- `license/`
  - It contains the license key `signed_key.json`.
  - It will be mounted to the Docker container.
- `deploy/license-verification`
  - It contains the python project that has the license verification and its job.
- `deploy/license-verification/resources/host_id`
  - The host_id for the customer.
  - It must much the host_id in the license `signed_key.json`, or license becomes invalid.
- `deploy/license-verification/resources/public_key.pem`
  - The public key used to verify the license `signed_key.json`.

### Building Files

- `Dockerfile`
  - It configures the Docker image building.
  - Do not use it directly, instead use `deploy/docker/build-image`.
- `deploy/docker/entrypoint.sh`
  - It contains the Docker container entrypoint script, which
    - Runs license verification script.
    - Runs license verification job script.
    - Runs Odoo.
  - It will be copied to the Docker image.
- `deploy/docker/build-image`
  - It contains the Docker image build command.
  - Use it instead of `Dockerfile`.

### Running Files

- `run-profiles/`
  - It contains runner scripts based on the profile.
- `run-profiles/dev-ubuntu`
  - A profile to run the project in local ubuntu during development.
  - It runs postgres Docker container.
  - Do not run `compose.yaml` file directly, instead run `run-postgres` script.
- `run-profiles/dev-ubuntu/env.conf`
  - It contains the Odoo configurations used by dev-ubuntu run profile.
  - It will be copied to the Docker image.
- `run-profiles/dev-windows`
  - A profile to run the project in local Windows during development.
  - It runs postgres Docker container.
  - Do not run `compose.yaml` file directly, instead run `run-postgres` script.
- `run-profiles/dev-windows/env.conf`
  - It contains the Odoo configurations used by dev-windows run profile.
  - It will be copied to the Docker image.
- `run-profiles/local-ubuntu`
  - A profile to run the project in local ubuntu in customer machine.
  - It runs postgres & ev-odoo Docker containers.
  - Do not run `compose.yaml` file directly, instead run `run` script.
- `run-profiles/local-ubuntu/env.conf`
  - It contains the Odoo configurations usde by local-ubuntu run profile.
  - It will be copied to the Docker image.
- `run-profiles/local-windows`
  - A profile to run the project in local windows in customer machine.
  - It runs postgres & ev-odoo Docker containers.
  - Do not run `compose.yaml` file directly, instead run `run` script.
- `run-profiles/local-windows/env.conf`
  - It contains the Odoo configurations used by local-windows run profile.
  - It will be copied to the Docker image.
- `run-profiles/ansible`
  - It contains cloud deploying ansible project.

---

## Running Process

### dev-ubuntu Run Profile

- A profile to run the project in local ubuntu from source code during development.
- Steps  
  1. Clone the repository  
    ```git clone https://github.com/Experts-Vision/ev-odoo-basic .```
  2. Download Odoo sourcecode  
    ```git clone https://www.github.com/odoo/odoo --branch 18.0 --depth 1 /opt/odoo18```
  3. Install Docker
  4. Run postgres Docker container  
   ```./run-profiles/dev-ubuntu/run-postgres```
  5. Install system packages  
   ```sudo apt update && sudo apt upgrade```
   ```sudo apt install python3-dev python3-pip python3-wheel python3-venv build-essential libpq-dev libxslt-dev libxml2-dev  libzip-dev libldap2-dev libsasl2-dev libssl-dev```
  6. Support right-to-left languages like Arabic
    ```sudo apt install nodejs npm```
    ```sudo npm install -g rtlcss```
  7. Install Python dependencies
    ```cd run-profiles/dev-ubuntu/```
    ```virtualenv -p python3 env```
    ```source env/bin/activate```
    ```pip install -r /opt/odoo18/requirements.txt```
    ```pip install /opt/odoo18```
  8. Match DB configurations (host, port, username, password) in `./run-profiles/dev-ubuntu/env.conf` and `./run-profiles/dev-ubuntu/compose.yaml`
  9. Run Odoo
    ```/opt/odoo18/odoo-bin -c /run-profiles/dev-ubuntu/env.conf -i ev-odoo-basic --without-demo all```
  10. Open http://localhost:8069

### dev-windows Run Profile

- A profile to run the project in local windows from source code during development.
- Steps  
  1. Clone the repository  
    ```git clone https://github.com/Experts-Vision/ev-odoo-basic .```
  2. Download Odoo sourcecode  
    ```git clone https://www.github.com/odoo/odoo --branch 18.0 --depth 1 D:\odoo18```
     - Ensure odoo source code files have open permissions
  3. Install Docker
  4. Run postgres Docker container  
   ```./run-profiles/dev-windows/run-postgres```
  5. Install system packages
     - Python 3.10    -> python --version
     - pip            -> pip --version
     - Node.js        -> node -v
     - npm            -> npm -v
     - wkhtmltopdf (for PDF reports)  from  https://wkhtmltopdf.org/downloads.html
  6. Support right-to-left languages like Arabic
    ```npm install -g rtlcss```
  7. Install Python dependencies
    ```cd run-profiles\dev-windows\```
    ```python -m venv venv```
    ```venv\Scripts\activate```
    ```pip install wheel qifparse Wkhtmltopdf```
    ```pip install -r D:\odoo18\requirements.txt```
    ```pip install D"\odoo18```
  8. Match DB configurations (host, port, username, password) in `./run-profiles/dev-windows/env.conf` and `./run-profiles/dev-windows/compose.yaml`
  9. Run Odoo
    ```python "D:\odoo18\odoo-bin" -c .\env.conf -i ev-odoo-basic --without-demo all```
  10. Open http://localhost:8069

### local-ubuntu Run Profile

- A profile to run the project in local ubuntu in customer machine.
- Steps  
  1. Clone the repository  
    ```git clone https://github.com/Mahmoud-Shosha/ev-odoo-basic.git .```
  2. Install Docker
  3. Build the Docker image `ev-odoo:latest`  
    ```./deploy/docker/build-image```
  4. Run postgres & ev-odoo Docker container  
   ```./run-profiles/local-ubuntu/run```

### local-windows Run Profile

- A profile to run the project in local Windows in customer machine.
- Steps  
  1. Clone the repository  
    ```git clone https://github.com/Mahmoud-Shosha/ev-odoo-basic.git .```
  2. Install Docker
  3. Build the Docker image `ev-odoo:latest`  
    ```./deploy/docker/build-image```
  4. Run postgres & ev-odoo Docker container  
   ```./run-profiles/local-windows/run```
