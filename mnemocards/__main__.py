
from mnemocards import greet
from mnemocards._argument_parser import parse_args
from mnemocards.github import github
from mnemocards.generate import generate
from mnemocards.pull import pull
from mnemocards.push import push
from mnemocards.clean import clean
from mnemocards.import_command import import_command


def main():
    """Check arguments and execute the indicated task. """

    args = parse_args()

    if args.command == "generate":
        generate(args)
    elif args.command == "import":
        import_command(args.apkgs, args.collection_path, args.profile_name)
    elif args.command == "push":
        push()
    elif args.command == "pull":
        pull()
    elif args.command == "github":
        github(args.api_key, args.dir, args.include, args.exclude, args.gists)
    elif args.command == "clean":
        clean(args.collection_path, args.profile_name)
    elif args.command == "hi":
        greet()


if __name__ == "__main__":
    main()

