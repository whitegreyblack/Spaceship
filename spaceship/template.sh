if [ "$#" -eq 3 ]
then	
cat << EOF >> $1.py
import tdl
from imports import *

def build():
    pass

if __name__ == '__main__':
    W, H = $2, $3
    tdl.setFont('fonts/4x6.png')
    cli = tdl.init(W,H,'$1')
    while True:
        cli.clear()
        tdl.flush()
        for e in tdl.event.get():
            if e.type=='QUIT' or (e.type=='KEYDOWN' and e.keychar=='q'):
                raise SystemExit('Exit Program')
EOF
else
echo "Incorrect Arguments"
exit 1
fi
