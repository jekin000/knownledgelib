#!/bin/bash

echo > knownledgelib/spider.log 
echo > knownledgelib/parser.log 
echo > knownledgelib/output.txt
rm -Rf knownledgelib/*.html
cp knownledgelib/begin.txt knownledgelib/urls.txt
 
