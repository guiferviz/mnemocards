
CARDS_DIR=$HOME/learning

# Ensures that the config file exists.
# If it does not exists docker is going to mount a directory instead of a file
# and the program is going to fail.
# Also, creating the file here it's going to be owned by the current user.
if [ ! -f ~/.mnemocards ]; then
    # Create a file with a valid JSON.
    echo {} > ~/.mnemocards
fi

sudo docker run \
    -v /usr/share/anki:/usr/share/anki:ro \
    -v ~/.ssh:/root/.ssh:ro \
    -v ~/.gitconfig:/root/.gitconfig:ro \
    -v ~/.gh_key:/root/.gh_key:ro \
    -v $PWD:/workspace \
    -v ~/.local/share/Anki2:/root/.local/share/Anki2 \
    -v ~/.mnemocards:/root/.mnemocards \
    -v $CARDS_DIR:$CARDS_DIR \
    -it \
    guiferviz/mnemocards \
    "$@"

# Change ownership of the generated files (assuming that the defaul group of
# the user is the same as the username)
sudo chown -R $USER:$USER $CARDS_DIR

