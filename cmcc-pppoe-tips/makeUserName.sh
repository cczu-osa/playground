#!/bin/bash

uuid=`uuidgen -t`
text1=`echo $uuid | sed "s/-//g"`
text2="YourPhoneNumberHere"
number=0

for ((i=0;i<3;++i)); do;
  number=$((number + $(printf '%d ' "'${text1:$i:1}")))
done

for ((i=0;i<3;++i)); do;
  number=$((number + $(printf '%d ' "'${text2:$i:1}")))
done

echo $text1$(printf "%04d" $(((177 * number + 5166) % 10000)))"01"$text2"@internet"
