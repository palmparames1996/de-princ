include .env

test:
	cd 1.provision && pwd

create-eks:
	eksctl create cluster --name ${EKS_CLUSTER_NAME} --region ${EKS_REGION} --nodegroup-name ${EKS_NODEGROUP_NAME} --spot --node-type ${EKS_NODETYPE} --nodes ${EKS_NODE_NUMBER} --nodes-min ${EKS_NODE_MIN} --nodes-max ${EKS_NODE_MAX}

delete-eks:
	eksctl delete cluster --name ${EKS_CLUSTER_NAME} --region ${EKS_REGION}

local-env:
	cd 3.data-pipeline && cp local.env .env

local-start:
	cd 3.data-pipeline && docker-compose -f local-docker-compose.yml up -d

local-build:
	cd 3.data-pipeline && docker-compose -f local-docker-compose.yml up -d --build

local-stop:
	cd 3.data-pipeline && docker-compose -f local-docker-compose.yml down

deploy-mage:
	kubectl apply -f ./1.provision

forword-mage:
	export AWS_PROFILE=parames_root
	kubectl port-forward --namespace default svc/mage-ai-service 6789:6789

delete-mage:
	kubectl delete -f ./1.provision

forword-mage:
	export AWS_PROFILE=parames_root
	kubectl port-forward --namespace default svc/mage-ai-service 6789:6789

ci-up:
	cd ./2.cicd && docker-compose up -d --build

ci-down:
	cd ./2.cicd && docker-compose down

ci-local-password:
	docker exec jenkins-blueocean cat /var/jenkins_home/secrets/initialAdminPassword