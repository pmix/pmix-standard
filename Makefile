# Makefile for the PMIx Standard document in LaTex format. 
# For more information, see the master document, pmix-standard.tex.

version=2.0
default: pmix-standard.pdf

CHAPTERS= \
	TitlePage.tex \
	Chap_Introduction.tex \
	Chap_Terms.tex \
	Chap_Overview.tex \
	Chap_API_Struct.tex \
	Chap_API_Client.tex \
	Chap_API_Server.tex \
	Chap_API_Tool.tex \
	History.tex

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
		pmix-standard.log

all: pmix-standard.pdf

pmix-standard.pdf: $(CHAPTERS) $(SOURCES) pmix.sty pmix-standard.tex figs/pmix-logo.png
	rm -f $(INTERMEDIATE_FILES)
	@echo "-------------------------------------------------------------"
	@echo "If error occurs check pmix-standard.log and pmix-standard.ind"
	@echo "-------------------------------------------------------------"
	@echo "====> Building 1/3"
	pdflatex -interaction=batchmode -file-line-error pmix-standard.tex
	@echo "====> Building 2/3"
	pdflatex -interaction=batchmode -file-line-error pmix-standard.tex
	@echo "====> Building 3/3"
	pdflatex -interaction=batchmode -file-line-error pmix-standard.tex
	@echo "====> Success"
	cp pmix-standard.pdf pmix-standard-${version}.pdf

clean:
	rm -f $(INTERMEDIATE_FILES)
