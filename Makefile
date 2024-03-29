# Makefile for the PMIx Standard document in LaTex format.
# For more information, see the master document, pmix-standard.tex.

LATEX_C=pdflatex -shell-escape -file-line-error

version=v5.0
OPENPMIX_BRANCH ?= "master"

all: pmix-standard.pdf check

CHAPTERS= \
	TitlePage.tex \
	Chap_Introduction.tex \
	Chap_Revisions.tex \
	Chap_Terms.tex \
	Chap_API_Struct.tex \
	Chap_API_Init.tex \
	Chap_API_Sync.tex \
	Chap_API_Sharing_Basics.tex \
	Chap_API_Reserved_Keys.tex \
	Chap_API_Query.tex \
	Chap_API_Publish.tex \
	Chap_API_Proc_Mgmt.tex \
	Chap_API_Job_Mgmt.tex \
	Chap_API_Event.tex \
	Chap_API_Data_Mgmt.tex \
	Chap_API_Security.tex \
	Chap_API_Server.tex \
	Chap_API_Fabric.tex \
	Chap_API_Sets_Groups.tex \
	Chap_API_Tools.tex \
	Chap_API_Storage.tex \
	App_Python.tex \
	App_Use_Cases.tex \
	Acknowledgements.tex

SOURCES=sources/*.c \
	sources/*.py \

INTERMEDIATE_FILES=pmix-standard.pdf \
		pmix-standard.toc \
		pmix-standard.idx \
		pmix-standard.ilg \
		pmix-standard.ind \
		pmix-standard.aux \
		pmix-standard.out \
		pmix-standard.log \
		pmix-standard.bbl \
		pmix-standard.blg \
		pmix-standard.synctex.gz \
		pmix-standard.xwm \
		pmix-standard.mw \
		pmix-standard.loc \
		pmix-standard.soc \
		*.idx *.ilg *.ind \
		_minted-* \
		sources/_autogen_ \
		debug-files

pmix-standard.pdf: $(CHAPTERS) $(SOURCES) pmix.sty pmix-standard.tex figs/pmix-logo.png
	@echo "Hi"
	rm -rf $(INTERMEDIATE_FILES)
	@echo "-------------------------------------------------------------"
	@echo "If error occurs check pmix-standard.log and pmix-standard.ind"
	@echo "-------------------------------------------------------------"
	@echo "====> Preprocess Examples"
	@./bin/process-example.py $(SOURCES)
	@echo "====> Building 1/4"
	$(LATEX_C) -interaction=batchmode pmix-standard.tex || \
		$(LATEX_C) -interaction=errorstopmode pmix-standard.tex < /dev/null
	@echo "====> Building 2/4 (bibtex)"
	bibtex pmix-standard < /dev/null
	@echo "====> Building 3/4"
	$(LATEX_C) -interaction=batchmode pmix-standard.tex || \
		$(LATEX_C) -interaction=errorstopmode pmix-standard.tex  < /dev/null
	@echo "====> Building 4/4"
	$(LATEX_C) -interaction=batchmode pmix-standard.tex || \
		$(LATEX_C) -interaction=errorstopmode pmix-standard.tex  < /dev/null
	$(LATEX_C) -interaction=batchmode pmix-standard.tex
	@cp pmix-standard.pdf pmix-standard-${version}.pdf

check: check-doc display-stats

# Includes
#  - make check-decl
#  - make check-attr-ref
check-doc: pmix-standard.pdf
	@./bin/check-doc.sh
	@echo "========> Success <========"

check-attr-ref: pmix-standard.pdf
	@echo "====> Checking for Attributes Declared, but not referenced"
	@./bin/check-attr-refs.py

check-decl: pmix-standard.pdf
	@echo "====> Checking for Multi-declared items"
	@./bin/check-multi-declare.py

# The default is defined near the top of the Makefile
# To change the default at runtime you can manually set the envar:
#   OPENPMIX_BRANCH=master make check-openpmix
check-openpmix: pmix-standard.pdf
	@echo "====> Checking cross-reference with OpenPMIx"
	@./bin/check-openpmix.py -b ${OPENPMIX_BRANCH}

display-stats: pmix-standard.pdf
	@echo "====> Display Stats"
	@mkdir -p debug-files
	@./bin/display-stats.py -f debug-files/std

clean:
	rm -rf $(INTERMEDIATE_FILES) pmix-standard-*.pdf
