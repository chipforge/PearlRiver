# PearlRiver (珠江芯片一号)

This projects covers the 1st LibreSilicon Test Chip.

There is a tradition in the Silicon Foundry business to code name Process Control / Process Evaluation Modules (PCM/PEM) with big rivers. Following that tradition, we like to call the 1st LibreSilicon Test / Evaluation Wafer "Pearl River". The Pearl River (珠江) flows close to LibreSilicons rented 1st Clean Room Facility.

## Layout

Currently we are using a patched version of [Magic 8.2](https://github.com/libresilicon/magic-8.2).

For the technology representing we patched the SCMOS technology file from [Mosis](https://mosis.com).
Our technology file is stored in the PearlRiver Repository.

All Layout files are stored inside

* Library/magic Folder, and
* Layout/magic Folder.

For evaluating relevant parameters, we are using test structures which are placed in form of a triangle; representing the bottom, left, upper and right side of the die.

View Layout files with

```
magic -T scmos.tech Layout/magic/PearlRiver_quarter.mag
```

for the quarters, or

```
magic -T scmos.tech Layout/magic/PearlRiver_die.mag
```

for the whole die.

## Documentation

For documentation we are using LaTeX.

All original LaTeX files are stored inside

* Documentation/LaTeX Folder

You can build the documentation out of the LaTeX sources just by using the Makefile

```
make doc
```

on top of the project directory.
Please read the documentation with the PDF Viewer of your choise

```
$PDFVIEWER Documentation/PearlRiver.pdf
```
carefully.

If you do not understand, what the hack we are doing here, please sit back with a good textbook about CMOS or ASIC technology development and learn. Please come back later.

