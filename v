#!/bin/bash
if [ "$1" == "" ]
  then
    file="."
  else
    file=$1
fi
ft=`file -b "$file"`
ext=${file##*.}
echo $ft

case $ft in
*image*)
  eog "$file"
  ;;
*directory*)
  ls -al "$file"
  ;;
PDF*)
#  acroread "$file"
  evince "$file"
  ;;
CDF*|OpenDocument*)
  soffice "$file"
  ;;
Zip*)
  case $ext in
    docx|xlsx|pptx)
      soffice "$file"
    ;;
    zip|ZIP)
      unzip -v "$file"
    ;;
  esac
  ;;
gzip*)
  case $file in
    *.tar.gz|*.tgz|*.TGZ)
      tar tvfz "$file" | more
    ;;
    *)
    gzip -l "$file"
    ;;
  esac
  ;;
*text*)
  less "$file"
  ;;
esac
