#!/bin/bash

find . | grep -E "(__pycache__|\.pyc|\.pyo$|pytest_cache)" | xargs rm -rf