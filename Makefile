docker-build-local:
	docker build -t hddm-bids .

docker-build-dockerhub:
	docker build -t poldrack/hddm-bids .

run:
	docker run -i --rm -v ${PWD}:/example hddm-bids /example/data /example/data/derivatives participant /example/models/hddm_model.json 

run-dockerhub:
	docker run -i --rm -v ${PWD}:/example poldrack/hddm-bids /example/data /example/data/derivatives participant /example/models/hddm_model.json 

shell:
	docker run -v ${PWD}:/example -it --entrypoint=bash hddm-bids

docker-login:
	docker login --username=$(DOCKER_USERNAME) --password=$(DOCKER_PASSWORD)

docker-upload:
	docker push poldrack/hddm-bids

