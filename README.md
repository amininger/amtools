# amtools project
* **Author:** Aaron Mininger
* **Github:** `https://github.com/amininger/amtools`
* **Year:** 2022

A python package containing various general tools for 
some of my projects. 

## `amtools.LineReader`

An abstract interface for reading text line-by-line. 
There are two implementations you can create: `ListReader` and `FileReader`. 
These read from a list of strings or a text file respectively. 

## `amtools.markdown`

Contains a simple markdown parser, as well as a tools for rendering markdown as html. 

## `amtools.filesystem`

Contains objects that wrap files and directories. These are indended to provide
ways to navigate a filesystem with additional metadata to specify home files, menus, etc. 

