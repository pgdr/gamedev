pdf: README.md
	pandoc README.md -o graphgames.pdf

book: README.md
	pdfbook2 graphgames.pdf
