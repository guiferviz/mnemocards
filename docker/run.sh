
docker run \
    -v $PWD:/workspace \
    --user $(id -u):$(id -g) \
    -it \
    guiferviz/mnemocards \
    "$@"

