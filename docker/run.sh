
docker run \
    -v $PWD:/workspace \
    -v /usr/share/anki:/usr/share/anki \
    -v ~/.local/share/Anki2:/home/root/.local/share/Anki2 \
    --user $(id -u):$(id -g) \
    -it \
    guiferviz/mnemocards \
    "$@"

