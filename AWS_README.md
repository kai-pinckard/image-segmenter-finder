## Create an AWS Account
https://portal.aws.amazon.com/billing/signup#/start

## Create an Access Key:
Part way through the tutorial you will needan "AWS Access Key ID" and "AWS Secret Access Key". 

Open [AWS console](https://aws.amazon.com/console/) in a browser. In the top right of the screen click my account and then security credentials. On the security credentials page, click "Access Keys". Then click create a new access key. Select Download Access key. Then open the file so that when the time comes you can put use the access key in the tutorial.

## Pick a Region
If you are fine hosting your cluster in your default region you can proceed to the next step. Otherwise find your region code here:

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-available-regions

## Main Tutorial
Follow the tutorial until you get to the part that tells you to run `kubectl get svc`. Run that command and ensure everything is working as expected. Note that in the tutorial you will need to use some of the information you obtained in the previous parts of this document. Furthermore, when the time comes select "AWS for linux-only workloads". Basic Steps include:

- Downloading the AWS Kuberneties installer



Note that running the command that creates a kubernetes cluster typically takes about 15 minutes.

https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html

## Running See Segment
Once this has successfully finished you can start the application using kubectl

Navigate to ./image-segmenter-finder/src/see_server/kube_commands in your cloned local version of this repository. 

Then run:

`kubectl apply -f server_service.yaml`

`kubectl apply -f server.yaml`

`kubectl apply -f segmentation_job.yaml.yaml`


Everything should now be up and running. You can access the server by typing:

`kubectl get services`

It takes a minute to get set up but eventually there will be an external ip for the server_service
By copying this ip into a browser you will be able to access the server. 

You should be able to delete your cluster with a command similar to

`eksctl delete cluster --region=us-west-2 --name=prod`

## Known Issues:
When creating the kubernetes cluster it may state that the creation of the cluster failed because your account is not authorized to use the required compute resources. In this case retrying the command ended up fixing the issue. 
