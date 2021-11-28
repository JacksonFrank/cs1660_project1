FROM tiangolo/uwsgi-nginx-flask
COPY ./app /app
COPY ./start.sh /start.sh
COPY ./init_kube_objects /init_kube_objects
COPY ./init_deployments.py /init_deployments.py
RUN pip install kubernetes