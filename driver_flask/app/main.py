from flask import Flask, render_template, redirect
from kubernetes import client, config


app = Flask(__name__)

service_account_name = None

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/hadoop")
def enable_hadoop():
    resize_hadoop(1, 2)
    url = get_url("namenode-public-service")
    name = "Apache Hadoop"
    return render_template('service.html', url=url, name=name)

@app.route("/hadoopdisable")
def disable_hadoop():
    resize_hadoop(0, 0)
    return render_template('redirect_home.html', name="Hadoop")

def resize_hadoop(nn_size: int, dn_size: int):
    config.load_incluster_config()
    appsv1 = client.AppsV1Api()
    namenode_deployment = appsv1.read_namespaced_deployment("hdfs-namenode-deployment", "default")
    namenode_deployment.spec.replicas = nn_size
    appsv1.patch_namespaced_deployment("hdfs-namenode-deployment", "default", body = namenode_deployment)
    datanode_deployment = appsv1.read_namespaced_deployment("hdfs-datanode-deployment", "default")
    datanode_deployment.spec.replicas = dn_size
    appsv1.patch_namespaced_deployment("hdfs-datanode-deployment", "default", body = datanode_deployment)

@app.route("/spark")
def enable_spark():
    resize_deployment("spark-deployment", 1)
    url = get_url("spark-service")
    
    name = "Apache Spark"
    return render_template('service.html', url=url, name=name)

@app.route("/sparkdisable")
def disable_spark():
    resize_deployment("spark-deployment", 0)
    return render_template('redirect_home.html', name="Spark")

@app.route("/notebook")
def enable_notebook():
    resize_deployment("notebook-deployment", 1)
    url = get_url("notebook-service")

    name = "Jupyter Notebook"
    return render_template('service.html', url=url, name=name)

@app.route("/notebookdisable")
def disable_notebook():
    resize_deployment("notebook-deployment", 0)
    return render_template('redirect_home.html', name="Jupyter Notebook")

@app.route("/sonar")
def enable_sonar():
    resize_deployment("sonar-deployment", 1)

    url = get_url("sonar-service")

    name = "SonarQube and SonarScanner"
    return render_template('service.html', url=url, name=name)

@app.route("/sonardisable")
def disable_sonar():
    resize_deployment("sonar-deployment", 0)
    return render_template('redirect_home.html', name="SonarQube and SonarScanner")

def resize_deployment(deployment_name: str, new_size: int):
    config.load_incluster_config()
    appsv1 = client.AppsV1Api()

    deployment = appsv1.read_namespaced_deployment(deployment_name, "default")
    deployment.spec.replicas = new_size
    appsv1.patch_namespaced_deployment(deployment_name, "default", body = deployment)

def get_url(service_name: str):
    url = 'http://'

    corev1 = client.CoreV1Api()
    current_node_list = corev1.list_node()
    ip_address_list = current_node_list.items[0].status.addresses
    for ip_address in ip_address_list:
        if (ip_address.type == 'ExternalIP'):
            url += ip_address.address
            break
    service = corev1.read_namespaced_service(service_name, "default")
    port = service.spec.ports[0].node_port
    url += ':' + str(port)
    return url

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)