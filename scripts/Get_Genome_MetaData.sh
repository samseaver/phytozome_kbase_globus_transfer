#!/bin/bash
file=$1
proteome_string=`cut -f2 $file | grep -v Proteome | sort -n | perl -lne 'chomp;push(@temp,$_);END{print join("%2C",@temp)}'`
url_string="https://phytozome-next.jgi.doe.gov/api/db/properties/proteome/"
curl -X GET "${url_string}${proteome_string}" -H "accept: application/json" | python -m json.tool
# perl -MJSON -lne 'use JSON;print to_json(from_json($_),{pretty=>1})'
