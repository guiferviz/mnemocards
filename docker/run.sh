
# If you want to use github, pull and push commands you need to set the
# directory in which you want to clone your repos in the next line:
CARDS_DIR=$HOME/learning

# Ensures that the config file exists.
# If it does not exists docker is going to mount a directory instead of a file
# and the program is going to fail.
# Also, creating the file here it's going to be owned by the current user.
if [ ! -f ~/.mnemocards ]; then
    # Create a file with a valid JSON.
    echo {} > ~/.mnemocards
fi

# Run the docker image using the following volumes:
# * ~/.ssh to clone your GitHub repositories. No needed for generating apkgs.
# * ~/.gitconfig to use your username and email. No needed for generating apkgs.
# * ~/.gh_key to use the GitHub API. No needed for generating apkgs.
# * $CARDS_DIR is the path you want to use for cloning the git repositories.
#   I have all my cards inside the learning dir in my home path. The commands
#   github, pull and push use this path.
# * ~/.local/share/Anki2 if you want to import your apkg files. No needed for
#   generating apkgs.
# * ~/.mnemocards config file. Necessary.
# * $PWD current dir with all the text files used to generate cards. Necessary.
sudo docker run \
    -v ~/.ssh:/root/.ssh:ro \
    -v ~/.gitconfig:/root/.gitconfig:ro \
    -v ~/.gh_key:/root/.gh_key:ro \
    -v $CARDS_DIR:$CARDS_DIR \
    -v ~/.local/share/Anki2:/root/.local/share/Anki2 \
    -v ~/.mnemocards:/root/.mnemocards \
    -v $PWD:/workspace \
    -it \
    guiferviz/mnemocards \
    "$@"

# Change ownership of the generated files as we are using root user in docker.
# CAUTION 1! We are assuming that the default group of the user is the same as
# the username.
# CAUTION 2! The next line changes the ownership of ALL the files under current
# directory, not only the generated files. Make sure that's not a problem for
# you.
sudo chown -R $USER:$USER $PWD

