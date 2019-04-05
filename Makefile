docker-build:
	docker build -t hddm-bids .

run:
	docker run -i --rm -v ${PWD}:/example hddm-bids /example/data /example/data/derivatives participant /example/models/hddm_model.json 

shell:
	docker run -v ${PWD}:/example -it --entrypoint=bash hddm-bids
