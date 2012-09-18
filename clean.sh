#!/bin/bash

find . -name "*.pyc" -exec rm {} \;
rm -rf build dist *.egg-info
