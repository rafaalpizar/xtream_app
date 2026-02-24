# Makefile for Xtream Client/Server project with Docker

DOCKER = docker
IMAGE = xtream-image
CONTAINER = xtream-app

.PHONY: build docker image and container

build:
	$(DOCKER) build -t $(IMAGE) -f docker/Dockerfile .

image-rm:
	$(DOCKER) image rm $(IMAGE)

run-rm:
	$(DOCKER) run --rm -it $(IMAGE) bash

run:
	$(DOCKER) run --name $(CONTAINER) $(IMAGE)

start:
	$(DOCKER) start $(CONTAINER)

stop:
	$(DOCKER) stop $(CONTAINER)

attach:
	$(DOCKER) attach $(CONTAINER)

