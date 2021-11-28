from kubernetes import client, config, utils

config.load_incluster_config()
k8s_client = client.ApiClient()
utils.create_from_yaml(k8s_client, '/init_kube_objects/hdfs-deploy.yaml')
utils.create_from_yaml(k8s_client, '/init_kube_objects/notebook-deploy.yaml')
utils.create_from_yaml(k8s_client, '/init_kube_objects/sonar-deploy.yaml')
utils.create_from_yaml(k8s_client, '/init_kube_objects/spark-deploy.yaml')