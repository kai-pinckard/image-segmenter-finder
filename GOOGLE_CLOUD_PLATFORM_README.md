## Set up Kubernetes on Google Cloud Platform:
Follow the tutorial until you get to the part labeled:
"Deploying an application to the cluster"

when asked for a Region in the tutorial you can find them here:
https://cloud.google.com/compute/docs/regions-zones

Main Tutorial:
https://cloud.google.com/kubernetes-engine/docs/quickstart

Note: that the command to create the cluster typically takes around 15 minutes to complete.

In the following command, from the tutorial, you can modify
the number of "vm"s that will be dedicated to running your cluster. Simply increase --num-nodes=1 to have the number of "vm"s you want.

`gcloud container clusters create cluster-name --num-nodes=1`


## Run See Segment with Kubernetes
These commands must be executed in the kube_commands folder
`kubectl apply -f server_service.yaml`
`kubectl apply -f server.yaml`
`kubectl apply -f segmentation_job.yaml.yaml`


Everything should now be up and running.

## Access the Service
To access the service run:
`kubectl get services`
It takes a minute to get set up but eventually there will be an external ip for the server_service. By copying this ip into a browser you will be able to access the server. 



Known Potential Issues:
ERROR: (gcloud.components.install) You cannot perform this action because this Cloud SDK installation is managed by an external package manager.
Please consider using a separate installation of the Cloud SDK created through the default mechanism described at: 

If you have a very old version of gcloud it may be necessary to delete it. You can then restart the above steps.
https://cloud.google.com/sdk/docs/uninstall-cloud-sdk
install-google-cloud-components-error-from-gcloud-command

