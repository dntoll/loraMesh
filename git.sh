#!/bin/bash


#this is since work client does not fully work on this and I dont know why... yet
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github

