# Makefile for the PMIx Standard document in LaTex format.
# For more information, see the master document, pmix-standard.tex.

version=4.0
default: pmix-standard.pdf

CHAPTERS= \
	TitlePage.tex \
	Chap_Introduction.tex \
	Chap_Terms.tex \
	Chap_API_Init.tex \
	Chap_API_Struct.tex \
	Chap_API_Key_Value_Mgmt.tex \
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
	Acknowledgements.tex

SOURCES=
# SOURCES=sources/*.c \
# 	sources/*.cpp \
# 	sources/*.f90 \
# 	sources/*.f

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
		*.idx *.ilg *.ind

all: pmix-standard.pdf

pmix-standard.pdf: $(CHAPTERS) $(SOURCES) pmix.sty pmix-standard.tex figs/pmix-logo.png
	rm -f $(INTERMEDIATE_FILES)
	@echo "-------------------------------------------------------------"
	@echo "If error occurs check pmix-standard.log and pmix-standard.ind"
	@echo "-------------------------------------------------------------"
	@echo "====> Building 1/4"
	pdflatex -interaction=batchmode -file-line-error pmix-standard.tex || \
		pdflatex -interaction=errorstopmode -file-line-error pmix-standard.tex < /dev/null
	@echo "====> Building 2/4 (bibtex)"
	bibtex pmix-standard < /dev/null
	@echo "====> Building 3/4"
	pdflatex -interaction=batchmode -file-line-error pmix-standard.tex || \
		pdflatex -interaction=errorstopmode -file-line-error pmix-standard.tex  < /dev/null
	@echo "====> Building 4/4"
	pdflatex -interaction=batchmode -file-line-error pmix-standard.tex || \
		pdflatex -interaction=errorstopmode -file-line-error pmix-standard.tex  < /dev/null
	pdflatex -interaction=batchmode -file-line-error pmix-standard.tex
	@echo "====> Checking References (pmix-standard.log)"
	@grep "Hyper reference" pmix-standard.log | grep Warning \
	&& { echo "====> Error check references (above)" ; exit 1; } || { exit 0; }
	@echo "====> Success"
	@cp pmix-standard.pdf pmix-standard-${version}.pdf

FORCECHECK:

check: check-attr-ref check-openpmix check-decl

check-attr-ref: pmix-standard.pdf FORCECHECK
	@echo "====> Checking for Attributes Declared, but not referenced"
	@./bin/check-attr-refs.py

check-openpmix: pmix-standard.pdf FORCECHECK
	@echo "====> Checking cross-reference with OpenPMIx"
	@./bin/check-openpmix.py

check-decl: pmix-standard.pdf FORCECHECK
	@echo "====> Checking for Multi-declared items"
	@./bin/check-multi-declare.py

clean:
	rm -f $(INTERMEDIATE_FILES) pmix-standard-*.pdf
