
docker run \
    -v $PWD:/workspace:ro \
    -v /usr/share/anki:/usr/share/anki:ro \
    -v ~/.ssh:/root/.ssh:ro \
    -v ~/.gitconfig:/root/.gitconfig:ro \
    -v ~/.gh_key:/root/.gh_key:ro \
    -v ~/.local/share/Anki2:/root/.local/share/Anki2 \
    -v ~/.mnemocards:/root/.mnemocards \
    -v ~/learning:$HOME/learning \
    --user $(id -u):$(id -g) \
    -it \
    guiferviz/mnemocards \
    "$@"

