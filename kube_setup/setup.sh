kubectl apply -f kube-auth.yaml
kubectl apply -f flask-driver.yaml

gcloud compute firewall-rules create jacksonfrank-cs1660-allow-public-traffic --allow tcp:30001-3006

pip install kubernetes
python print_url.py