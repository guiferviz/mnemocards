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

# Install mnemocards module.
COPY dist/mnemocards-*.whl /root/mnemocards/
RUN pip install /root/mnemocards/mnemocards-*.whl


#########
# Setup #
#########

# Set default working directory.
WORKDIR $WORKDIR

ENTRYPOINT ["python", "-m", "mnemocards"]
# Default command, generate cards recursively in $WORKDIR.
CMD ["generate", "-r", "."]
