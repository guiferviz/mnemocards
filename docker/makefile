
IMAGE_NAMESPACE = guiferviz
IMAGE_NAME = mnemocards
IMAGE = $(IMAGE_NAMESPACE)/$(IMAGE_NAME)
INSTALL_SCRIPT_NAME = mnemocards


all:
	cd .. && docker build -t $(IMAGE) -f docker/Dockerfile .

nocache:
	cd .. && docker build --no-cache -t $(IMAGE) -f docker/Dockerfile .

install:
	cp run.sh /usr/local/bin/$(INSTALL_SCRIPT_NAME) 

