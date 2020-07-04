# Step 1:
Create an AWS account

# Step 2:
https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html


When running aws configure you will need an aws access key. 
Open AWS in a browser.
In the top right of the screen click my account and then security credentials.

On the security credentials page, click Access Keys. Then click create a new access key. Select Download Access key. Then open the file
put the corresponding access key lines into the aws configure terminal. For default region, either leave it blank or put the region you want.
For default output select json. 

Select AWS for linux-only workloads


eksctl create cluster \
--name prod \
--version 1.16 \
--region us-west-2 \
--nodegroup-name standard-workers \
--node-type t3.medium \
--nodes 3 \
--nodes-min 1 \
--nodes-max 4 \
--managed


Once this has successfully finished you can start the application using kubectl

navigate to ./image-segmenter-finder/src/see_server/kube_commands

Then run:
kubectl apply -f server_service.yaml
kubectl apply -f server.yaml
kubectl apply -f segmentation_job.yaml.yaml

Everything should now be up and running.

You can access the server by typing
kubectl get services
It takes a minute to get set up but eventually there will be an external ip for the server_service
By copying this ip into a browser you will be able to access the server. 


You should be able to delete your cluster with a command similar to

eksctl delete cluster --region=us-west-2 --name=prod