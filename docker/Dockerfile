
################
#  Base image  #
################

# Let's start with a basic python image.
# This is the same version I'm using in my local computer, it probably works
# with a higher version.
FROM python:3.8


#########################
# Define env variables. #
#########################

# Define environment variables.
ENV WORKDIR /workspace


#####################
# Install programs. #
#####################

# Install requirements.
COPY requirements.txt /root/mnemocards/requirements.txt
RUN cd /root/mnemocards && pip install -r requirements.txt

# Install mnemocards module.
COPY README.md /root/mnemocards/README.md
COPY setup.py /root/mnemocards/setup.py
COPY mnemocards/ /root/mnemocards/mnemocards/
COPY requirements.in /root/mnemocards/requirements.in
RUN cd /root/mnemocards && python setup.py install


#########
# Setup #
#########

# Set default working directory.
WORKDIR $WORKDIR

ENTRYPOINT ["python", "-m", "mnemocards"]
# Default command, generate cards recursively in $WORKDIR.
CMD ["generate", "-r", "."]

