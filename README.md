# Project Cardiff

[![Build Status](https://travis-ci.org/peitaosu/Cardiff.svg?branch=master)](https://travis-ci.org/peitaosu/Cardiff)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/peitaosu/Cardiff/master/LICENSE)

## What is Project Cardiff ?

Project Cardiff want to create a version control tool for binary format files.

This tool can be used to diff difference between file versions, to check what have been modified, save versions and manage versions. Binary format always contains more complex information and hard to be parsed and modified, not like text format can be easy to read, modify, diff and merge. Not all binary formats have the meaning of diffing and controlling the version. So we only want to support homogeneous formats which the content can be visualized or parameterized, such as PNG, PSD, DWG, etc.

![How It Works](docs/How_It_Works.png)

## Already Supported
* Single Image Format
    - .BMP
    - .PNG
    - .JPG
    - .GIF
* Composite Data Format
    - .WAV
    - .AIF
* Complex Document/Project Format
    - .PSD (WIP)

## Plan to Support
* Complex Document/Project Format
    - .PDF
    - .DWG
    - .DOCX
    - .PPTX
    - .XLSX
    - ....
* Composite Data Format
    - ....

## Key Features
* Version Diff
* Diff Visualization
* Diff Parameterization
* Version Merge
* Version Rollback
* Version Branch

## Requirements
* python 2.x
* ```pip install -r requirements.txt```

## Usage
1. Command Line
   ```
   > python Cardiff.py help

   Usage:
     Cardiff.py init <repo_name>
     Cardiff.py repo <repo>
     Cardiff.py branch <branch>
     Cardiff.py commit <file> <message>
     Cardiff.py checkout <file> <version>
     Cardiff.py diff <file> <version_1> [<version_2>]
     Cardiff.py cdiff <file1> <file2> [<output>]
     Cardiff.py merge <file> <version_1> [<version_2>]
     Cardiff.py log [<filter>]
     Cardiff.py clean [<filter>]
     Cardiff.py conf <config_name> [<config_value>]
     Cardiff.py info [<information>]
     Cardiff.py help [<command>]

   ```

2. Python Module
   ```
   from Cardiff import Cardiff

   # new a cardiff object
   cardiff = Cardiff()

   # load settings
   settings_path = "./settings.json"
   cardiff.load_settings(settings_path)

   # execute command
   cardiff.exec_cmd(["help"])
   # or
   cardiff.cmd_help([])
   ```
