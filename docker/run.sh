sudo docker run \
    -v $PWD:/workspace \
    -it \
    guiferviz/mnemocards \
    "$@"

# Consider changing the ownership of the generated files (if any) as we are
# using root user in docker. Use chown:
#sudo chown -R $USER:$USER $PWD
