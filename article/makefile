#Programs used by make
TPUT = tput
SED = sed

# Terminal color definitions
black	:= $(shell $(TPUT) setaf 0)
red		:= $(shell $(TPUT) setaf 1)
green	:= $(shell $(TPUT) setaf 2)
yellow	:= $(shell $(TPUT) setaf 3)
blue	:= $(shell $(TPUT) setaf 4)
magenta	:= $(shell $(TPUT) setaf 5)
cyan	:= $(shell $(TPUT) setaf 6)
white	:= $(shell $(TPUT) setaf 7)
bold	:= $(shell $(TPUT) bold)
uline	:= $(shell $(TPUT) smul)
reset	:= $(shell $(TPUT) sgr0)

# Warning colors
C_WARNING	:= $(magenta)
C_ERROR		:= $(red)
C_INFO		:= $(green)
C_UNDERFULL	:= $(magenta)
C_OVERFULL	:= $(red)$(bold)
C_PAGES		:= $(bold)
C_BUILD		:= $(cyan)
C_GRAPHIC	:= $(yellow)
C_DEP		:= $(green)
C_SUCCESS	:= $(green)$(bold)
C_FAILURE	:= $(red)$(bold)
C_RESET		:= $(reset)

#Script for coloring tex log
color_tex	:= \
	$(SED) \
	-e '$${' \
	-e '  /^$$/!{' \
	-e '    H' \
	-e '    s/.*//' \
	-e '  }' \
	-e '}' \
	-e '/^$$/!{' \
	-e '  H' \
	-e '  d' \
	-e '}' \
	-e '/^$$/{' \
	-e '  x' \
	-e '  s/^\n//' \
	-e '  /Output written on /{' \
	-e '    s/.*Output written on \([^(]*\) (\([^)]\{1,\}\)).*/Success!  Wrote \2 to \1/' \
	-e '    s/[[:digit:]]\{1,\}/$(C_PAGES)&$(C_RESET)/g' \
	-e '    s/Success!/$(C_SUCCESS)&$(C_RESET)/g' \
	-e '    s/to \(.*\)$$/to $(C_SUCCESS)\1$(C_RESET)/' \
	-e '    b end' \
	-e '  }' \
	-e '  / *LaTeX Error:.*/{' \
	-e '    s/.*\( *LaTeX Error:.*\)/$(C_ERROR)\1$(C_RESET)/' \
	-e '    b end' \
	-e '  }' \
	-e '  /.*Undefined control sequence.*/{' \
	-e '    s//$(C_ERROR)&$(C_RESET)/' \
	-e '    b end' \
	-e '  }' \
	-e '  /.*Warning:.*/{' \
	-e '    s//$(C_WARNING)&$(C_RESET)/' \
	-e '    b end' \
	-e '  }' \
	-e '  /Underfull.*/{' \
	-e '    s/.*\(Underfull.*\)/$(C_UNDERFULL)\1$(C_RESET)/' \
	-e '    b end' \
	-e '  }' \
	-e '  /Overfull.*/{' \
	-e '    s/.*\(Overfull.*\)/$(C_OVERFULL)\1$(C_RESET)/' \
	-e '    b end' \
	-e '  }' \
	$(if $(VERBOSE),,-e '  d') \
	-e '  :end' \
	-e '  G' \
	-e '}' \

#Macro for coloring tex log
latex-color-log	= $(color_tex) $1

#Find all graphviz files
DOT_FILES = $(shell find -name "*.gv")

#Find all svg files
SVG_FILES = $(shell find -name "*.svg")

#Find all dot2tex files
D2T_FILES = $(shell find -name "*.d2t")

#Index file for the entire project
INDEX_FILE = index.pdf

#Flags for runing latex
LFLAGS = --interaction=batchmode --file-line-error --output-directory ./bin/

#All image targets
IMAGE_TARGETS = ${addprefix bin/, $(DOT_FILES:.gv=.gv.pdf)} \
				${addprefix bin/, $(SVG_FILES:.svg=.svg.pdf)} \
				${addprefix bin/, $(D2T_FILES:.d2t=.d2t.pdf)}

#Declaration of phony targets
.PHONY: clean todo %.pdf

#Rule for rendering svg files
bin/%.svg.pdf: %.svg
	@mkdir -p $(@D)
	inkscape $< --without-gui --export-area-drawing --export-pdf=$@ 

#Rule for rendering graphviz files
bin/%.gv.pdf: %.gv
	@mkdir -p $(@D)
	dot -Tps2 < $< | ps2pdf - $@

#Rule for rendering dot2tex files
bin/%.d2t.pdf: %.d2t
	@mkdir -p $(@D)
	dot2tex -t math --usepdflatex -c < $< > bin/$(*F).tex
	pdflatex $(LFLAGS) bin/$(*F).tex
	@cat bin/$(*F).pdf > $@

#Rule for building a tex file, this hack will wrap it in the preamble
%.pdf: %.tex #$(IMAGE_TARGETS)
	@if test ! -d bin; then mkdir bin; fi
	@mkdir -p $(@D)
	@$(eval INPUTS = $(shell echo "../$<" | sed 's/\//\\\//g'))
	@cat preamble.tex | sed -e 's/REPLACE-WITH-CONTENTS/\\input\{$(INPUTS)\}/' > bin/$(*F).tex
	@if pdflatex $(LFLAGS) bin/$(*F).tex > /dev/null; \
		then echo "build 1: OK"; else echo "build 1: Failed"; fi
	@if grep "\\citation" ./bin/$(*F).aux > /dev/null 2> /dev/null; then \
		if bibtex -terse ./bin/$(*F).aux > /dev/null 2> /dev/null; then \
			echo "bibtex:  OK"; else echo "bibtex:  Failed"; \
		fi; \
	fi
	@if pdflatex $(LFLAGS) bin/$(*F).tex > /dev/null; \
		then echo "build 2: OK"; else echo "build 2: Failed"; fi
	@if pdflatex $(LFLAGS) bin/$(*F).tex > /dev/null; \
		then echo "build 3: OK"; else echo "build 3: Failed"; fi
	-@xdg-open ./bin/$(*F).pdf > /dev/null 2> /dev/null
	@$(call latex-color-log, ./bin/$(*F).log)

#Default target
all: index.pdf
monitor:
	@while [ 1 ]; do \
		inotifywait -q -e close_write -r src/; \
		make quick; \
	done
quick:
	@mkdir -p ./bin/
	@$(eval INPUTS = $(shell echo "../index.tex" | sed 's/\//\\\//g'))
	@cat preamble.tex | sed -e 's/REPLACE-WITH-CONTENTS/\\input\{$(INPUTS)\}/' > bin/index.tex
	@if pdflatex $(LFLAGS) bin/index.tex > /dev/null; \
		then echo "build 1: OK"; else echo "build 1: Failed"; fi
	@$(call latex-color-log, ./bin/index.log)

verbose: index.pdf
	pdflatex --output-directory ./bin/ bin/index.tex

clean:
	rm -rf bin/

# extract TODO list from all lines beginning with "%TODO"
TODO: $(shell find -name "*.tex")
	@find ./ -name "*.tex" | \
		xargs grep -n TODO | \
		sed -e 's/:\([0-9]*\):.*%TODO[: ]\?/: \1:\n\t/' -e 's/^.\///' -e 's/^src\///' | \
		fmt > TODO
#Display todo-list
todo: TODO
	@less TODO
