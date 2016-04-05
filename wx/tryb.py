# coding: utf-8
import re

import sys
aa = "@832b05dcd10ec39f819e67ad87dd479898f8beafc9e4513fae1ddaaf7bfaaeee:<br/>呆呆熊是什么<br/>"
aa = re.sub(r"@[\d\w]+:<br/>","", aa)
aa = re.sub(r"<br/>","", aa)
print aa

