#!/bin/bash


while read p; do
  wget "https://ninlive.com/artists/nin/concerts/$p" -O ./gigs/$p.html -T 20
done <links.txt