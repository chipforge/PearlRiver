#   ************    LibreSilicon's 1st TestWafer    *******************
#
#   Organisation:   Chipforge
#                   Germany / European Union
#
#   Profile:        Chipforge focus on fine System-on-Chip Cores in
#                   Verilog HDL Code which are easy understandable and
#                   adjustable. For further information see
#                           www.chipforge.org
#                   there are projects from small cores up to PCBs, too.
#
#   File:           PearlRiver/GNUmakefile
#
#   Purpose:        Root Makefile
#
#   ************    GNU Make 3.80 Source Code       ****************
#
#   ////////////////////////////////////////////////////////////////
#
#   Copyright (c) 2018 by chipforge <hsank@nospam.chipforge.org>
#   All rights reserved.
#
#       This Standard Cell Library is licensed under the Libre Silicon
#       public license; you can redistribute it and/or modify it under
#       the terms of the Libre Silicon public license as published by
#       the Libre Silicon alliance, either version 1 of the License, or
#       (at your option) any later version.
#
#       This design is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#       See the Libre Silicon Public License for more details.
#
#   ////////////////////////////////////////////////////////////////////

#   project name

PROJECT =       PearlRiver

#   directory pathes

DOCUMENTSDIR =  Documents
LIBRARYDIR =    Library
LAYOUTDIR =     Layout
TOOLSDIR =      Tools

#   tool variables

CAT ?=          @cat
ECHO ?=         @echo # -e
MV ?=           mv
TAR ?=          tar -zh
DATE :=         $(shell date +%Y%m%d)

#   project tools

LATEX ?=        pdflatex -output-directory $(DOCUMENTSDIR) $(OUTPUTDIR)

#   default

DISTRIBUTION =  ./GNUmakefile \
                $(DOCUMENTSDIR) \
                $(LIBRARYDIR) \
                $(LAYOUTDIR) \
                $(TOOLSDIR)

#   ----------------------------------------------------------------
#               DEFAULT TARGETS
#   ----------------------------------------------------------------

#   display help screen if no target is specified

.PHONY: help
help:
	$(ECHO) "-------------------------------------------------------------------"
	$(ECHO) "    available targets:"
	$(ECHO) "-------------------------------------------------------------------"
	$(ECHO) ""
	$(ECHO) "    help       - print this help screen"
	$(ECHO) "    dist       - build a tarball with all important files"
	$(ECHO) "    clean      - clean up all intermediate files"
	$(ECHO) ""
	$(ECHO) "    doc        - compile documentation"
	$(ECHO) ""


#   make archiv by building a tarball with all important files

.PHONY: dist
dist: clean
	$(ECHO) "---- build a tarball with all important files ----"
	$(TAR) -cvf $(PROJECT)_$(DATE).tgz $(DISTRIBUTION)

#   well, 'clean' directories before distributing

.PHONY: clean
clean:
	$(ECHO) "---- clean up all intermediate files ----"
	$(MAKE) -C $(DOCUMENTSDIR)/LaTeX -f build.mk $@

#   ----------------------------------------------------------------
#               DOCUMENTATION TARGETS
#   ----------------------------------------------------------------

.PHONY: doc
doc:    $(DOCUMENTSDIR)/LaTeX/$(PROJECT).tex $(DOCUMENTSDIR)/LaTeX/revision.tex
	TEXINPUTS=$$TEXINPUT:./$(DOCUMENTSDIR)/LaTeX $(LATEX) $(<F)
#	TEXINPUTS=::../../circdia xelatex PearlRiver.tex
