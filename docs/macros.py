class MacroException(Exception):
    pass


def define_env(env):
    @env.macro
    def exception(message):
        raise MacroException(message)
