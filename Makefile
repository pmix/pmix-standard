# Makefile for the PMIx Standard document in LaTex format. 
# For more information, see the master document, pmix-standard.tex.

version=2.0
default: pmix-standard.pdf

CHAPTERS= \
	TitlePage.tex \
	Chap_Introduction.tex \
	Chap_Terms.tex \
	Chap_API_Struct.tex \
	Chap_API_Key_Value_Mgmt.tex \
	Chap_API_Proc_Mgmt.tex \
	Chap_API_Job_Mgmt.tex \
	Chap_API_Event.tex \
	Chap_API_Data_Mgmt.tex \
	Chap_API_Server.tex \
	History.tex \
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
		pmix-standard.blg

all: pmix-standard.pdf

pmix-standard.pdf: $(CHAPTERS) $(SOURCES) pmix.sty pmix-standard.tex figs/pmix-logo.png
	rm -f $(INTERMEDIATE_FILES)
	@echo "-------------------------------------------------------------"
	@echo "If error occurs check pmix-standard.log and pmix-standard.ind"
	@echo "-------------------------------------------------------------"
	@echo "====> Building 1/4"
	pdflatex -interaction=batchmode -file-line-error pmix-standard.tex
	@echo "====> Building 2/4 (bibtex)"
	bibtex pmix-standard
	@echo "====> Building 3/4"
	pdflatex -interaction=batchmode -file-line-error pmix-standard.tex
	@echo "====> Building 4/4"
	pdflatex -interaction=batchmode -file-line-error pmix-standard.tex
	@echo "====> Success"
	cp pmix-standard.pdf pmix-standard-${version}.pdf

clean:
	rm -f $(INTERMEDIATE_FILES)
