
CLASS = codehilite

STYLES = autumn
STYLES += borland
STYLES += bw
STYLES += colorful
STYLES += default
STYLES += emacs
STYLES += friendly
STYLES += fruity
STYLES += manni
STYLES += monokai
STYLES += murphy
STYLES += native
STYLES += pastie
STYLES += perldoc
STYLES += tango
STYLES += trac
STYLES += vim
STYLES += vs

# a recursively-expanding variable re-expanded under the control of foreach
gen_html = pygmentize -S $(style) -f html -a .$(CLASS) > $(style).css;

all:
	@$(foreach style, $(STYLES), $(gen_html))

