
################
#  Base image  #
################

# Let's start with a basic python image.
# This is the same version I'm using in my local computer, it probably works
# with a higher version.
FROM python:3.6.9


#########################
# Define env variables. #
#########################

# Define environment variables.
ENV WORKDIR /workspace


#####################
# Install programs. #
#####################

# Install Anki dependencies.
# In order to compile the pyaudio dependency we need portaudio19-dev.
# The rest of Anki dependencies are included in the requirements.txt.
RUN apt-get update
RUN apt-get install -y portaudio19-dev=19.6.0-1

# Install requirements.
COPY requirements.txt /root/mnemocards/requirements.txt
RUN cd /root/mnemocards && pip install -r requirements.txt

# Install mnemocards module.
COPY . /root/mnemocards
RUN cd /root/mnemocards && python setup.py install


#########
# Setup #
#########

# Set default working directory.
WORKDIR $WORKDIR

ENTRYPOINT ["python", "-m", "mnemocards"]
# Default command, generate cards recursively in $WORKDIR.
CMD ["-r", "."]

