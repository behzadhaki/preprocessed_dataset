# preprocessed_dataset

## Overview

This repository contains a set of datasets in HVO_Sequence format as well as tools to use these datasets.  

--------

### Datasets

- This repository contains a number of datasets preprocessed into HVO_Sequence format. These datasets can be found in <b> ./datasets_zipped </b> subdirectory. Moreover, some analysis of the datasets can be found in <b> ./datasets_analyzed/hvo_0.2.0/GrooveMIDI </b>

Currently, the following sets are available:

  1. GrooveMIDI Preprocessed into HVO_Sequences (versions upto 0.3.0) 
  
    Found in  ./datasets_zipped/GrooveMidi/ 
    
  2. ...

--------

### Tools

  1. A python script is also available for unzipping the datasets locally. After cloning the repository, run this script to extract datasets locally
    
    Found in ./extract_locally.py

  2. A set of python classes to create multiple subsets of the complete sets with specific requirements for each subset. 

    Code and Documentations can be found in ./preprocessed_dataset/Subset_Creators/

--------

### Visual Guide 


![Preprocessed Dataset   Subset Creators-1](https://user-images.githubusercontent.com/35939495/118397108-bf6b8400-b652-11eb-81aa-2af970c4ed0e.jpg)
