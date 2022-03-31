#! /bin/sh

autoflake --remove-all-unused-imports --remove-unused-variables --remove-duplicate-keys \
  --recursive --in-place .

isort .

flake8  .
 
black --line-length=119 .
