# pipetex
Python CLI application which supports the workflow with LaTeX documents

# Example
`pipetex -b main` uses the main.tex file to create a PDF document containing a
bibliography. The compilation is done using LaTeX.

To get more information on how to use the tool, run `pipetex -h`

# Installation
Using pip, you can install directly from this repository. The main branch
conains the last stable version of the application. 

```shell
pip install git+https://github.com/MaxWeise/pipetex
```

The pipetex application is compatible with Python 3.10 and higher.

# Features
The main feature of the tool is to create LaTeX documents. It takes a source
file (which may contain a "draft" option) and converts creates finalised PDF
documents from them. The sourcefile is not modified in this proccess and no
data is lost.

Some additional features:
* Create a bibliography from a given bib database
* Create a glossary

# Documentation
To get a full overview of the classes and functions used in the project, please
reffer to the [official
documentation](https://maxweise.github.io/pipetex/operations.html) of this
project.

This repo also contains a basic set of requirements and a styleguide to which
the code should adhere. For any further questions don't hesitate to write me an
e-mail.

# Contributing
If you want to contribute to the project, feel free to contact me under
maxfencing@web.de or open an issue.
