IMAGE_NAMESPACE = guiferviz
IMAGE_NAME = mnemocards
IMAGE_VERSION = 1.0.0a0
IMAGE_LATEST = $(IMAGE_NAMESPACE)/$(IMAGE_NAME)
IMAGE_TAG = $(IMAGE_NAMESPACE)/$(IMAGE_NAME):v$(IMAGE_VERSION)
INSTALL_SCRIPT_NAME = mnemocards


all:
	cd .. && poetry build && sudo docker build -t $(IMAGE_LATEST) -t $(IMAGE_TAG) -f docker/Dockerfile .

nocache:
	cd .. && poetry build && sudo docker build --no-cache -t $(IMAGE_LATEST) -t $(IMAGE_TAG) -f docker/Dockerfile .

install:
	cp run.sh /usr/local/bin/$(INSTALL_SCRIPT_NAME)

uninstall:
	rm /usr/local/bin/$(INSTALL_SCRIPT_NAME)
