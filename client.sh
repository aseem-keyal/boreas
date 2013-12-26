#!/bin/zsh
python zephyrus.py -a $2 -c $3 > a && python boreas.py $1 -c $3 -a $2 -t $4 -u -x | xargs -i egrep --color=always {} a | less -R && rm a
