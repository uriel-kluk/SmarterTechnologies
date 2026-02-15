.PHONY: build run test shell clean

IMAGE_NAME := smarter-packaging:dev

build:
	docker build -t $(IMAGE_NAME) .

run: build
	docker run --rm -p 8000:8000 -e API_TEST_TOKEN=test-token $(IMAGE_NAME)

test: build
	docker run --rm $(IMAGE_NAME) pytest -q

shell: build
	docker run --rm -it -e API_TEST_TOKEN=test-token $(IMAGE_NAME) /bin/bash

clean:
	-@docker rmi $(IMAGE_NAME) || true
