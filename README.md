# Project Cardiff

## What is Project Cardiff ?

Project Cardiff want to create a version control tool for binary format files.

This tool can be used to diff difference between file versions, to check what have been modified, save versions and manage versions. Binary format always contains more complex information and hard to be parsed and modified, not like text format can be easy to read, modify, diff and merge. Not all binary formats have the meaning of diffing and controlling the version. So we only want to support homogeneous formats which the content can be visualized or parameterized, such as PNG, PSD, DWG, etc.

![How It Works](How_It_Works.png)

## Already Supported
* Single Image Format
    - .BMP
    - .PNG
    - .JPG
    - .GIF

## Plan to Support
* Complex Document/Project Format
    - .PDF
    - .DWG
    - .PSD
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
