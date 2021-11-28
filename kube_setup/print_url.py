from kubernetes import client, config

config.load_kube_config()

url = 'http://'

corev1 = client.CoreV1Api()
current_node_list = corev1.list_node()
ip_address_list = current_node_list.items[0].status.addresses
for ip_address in ip_address_list:
    if (ip_address.type == 'ExternalIP'):
        url += ip_address.address
        break
service = corev1.read_namespaced_service("flask-driver-service", "default")
port = service.spec.ports[0].node_port
url += ':' + str(port)
print("URL to access driver web app:")
print(url)