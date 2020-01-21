
from mnemocards import greet
from mnemocards._argument_parser import parse_args
from mnemocards.github import github
from mnemocards.generate import generate
from mnemocards.pull import pull
from mnemocards.push import push
from mnemocards.clean import clean
from mnemocards.import_command import import_command


def main():
    args = parse_args()

    if args.command == "generate":
        generate(args)
    elif args.command == "import":
        # TODO: refactor this.
        c = args.collection_path
        p = args.profile_name
        if c is None and p is None:
            raise Exception("Specify at least the collection or the profile")
        import_command(args.apkgs, c, p)
    elif args.command == "push":
        push()
    elif args.command == "pull":
        pull()
    elif args.command == "github":
        github(args.api_key, args.dir, args.include, args.exclude, args.gists)
    elif args.command == "clean":
        # TODO: refactor this.
        c = args.collection_path
        p = args.profile_name
        if c is None and p is None:
            raise Exception("Specify at least the collection or the profile")
        clean(c, p)
    elif args.command == "hi":
        greet()


if __name__ == "__main__":
    main()

