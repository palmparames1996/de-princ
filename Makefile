include .env

create-eks:
	eksctl create cluster --name ${EKS_CLUSTER_NAME} --region ${EKS_REGION} --nodegroup-name ${EKS_NODEGROUP_NAME} --spot --node-type ${EKS_NODETYPE} --nodes ${EKS_NODE_NUMBER} --nodes-min ${EKS_NODE_MIN} --nodes-max ${EKS_NODE_MAX}

delete-eks:
	eksctl delete cluster --name ${EKS_CLUSTER_NAME} --region ${EKS_REGION}

create-vol:
	kubectl apply -f ./1.provision

delete-vol:
	kubectl delete -f ./1.provision

create-pg:
	kubectl apply -f ./1.provision/pg-pv.yaml
	helm install my-postgres bitnami/postgresql --set volumePermissions.enabled=true
	export POSTGRES_PASSWORD=$$(kubectl get secret --namespace default my-postgres-postgresql -o jsonpath="{.data.postgresql-password}" | base64 --decode)
	echo ${POSTGRES_PASSWORD}

forword-pg:
	export AWS_PROFILE=parames_root
	kubectl port-forward --namespace default svc/my-postgres-postgresql 5432:5432

connect-pg:
	PGPASSWORD=${POSTGRES_PASSWORD} psql --host 127.0.0.1 -U postgres -d postgres -p 5432

delete-pg:
	helm delete my-postgres
	kubectl delete -f ./1.provision/pg-pv.yaml

create-mage:
	kubectl apply -f ./1.provision/deploy

delete-mage:
	kubectl delete -f ./1.provision/deploy

forword-mage:
	export AWS_PROFILE=parames_root
	kubectl port-forward --namespace default svc/mage-ai-service 6789:6789

ci-up:
	cd ./2.cicd && docker-compose up -d

ci-down:
	cd ./2.cicd && docker-compose down

ci-local-start:
	cd ./2.cicd && docker build -t myjenkins-blueocean:latest .
	docker network create jenkins
	docker run -u 0 --name jenkins-blueocean --restart=on-failure --detach \
	--network jenkins --env DOCKER_HOST=tcp://docker:2376 \
	--env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 \
	--publish 8080:8080 --publish 50000:50000 \
	--volume ./2.cicd/jenkins-data:/var/jenkins_home \
	--volume ./2.cicd/jenkins-docker-certs:/certs/client:ro \
	myjenkins-blueocean:latest

ci-local-password:
	docker exec jenkins-blueocean cat /var/jenkins_home/secrets/initialAdminPassword

ci-local-stop:
	docker rm $$(docker stop $$(docker ps -a -q --filter ancestor=myjenkins-blueocean --format="{{.ID}}"))
	docker network rm jenkins