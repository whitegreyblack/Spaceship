if [ "$#" -eq 3 ]
then	
cat << EOF >> $1.py
import tdl
from imports import *

px, py = 0, 0
W, H = $2, $3

def keyhandler():
    global px, py
    ui = tdl.event.key_wait()
    if ui.key=='ESCAPE':
        raise SystemExit('Exitting')
    if ui.key=='UP':
        py = min(py-1,0)
    elif ui.key=='DOWN':
	py = max(py+1,H-1)
    elif ui.key=='LEFT':
        px = min(px-1,0)
    elif ui.key=='RIGHT':
        px = max(px+1,W-1)

if __name__ == '__main__':
    tdl.setFont('fonts/4x6.png')
    cli = tdl.init(W,H,'$1')
    while tdl.event.is_window_closed():
        cli.clear()
        # print stuff
        tdl.flush()
EOF
else
echo "Incorrect Arguments"
exit 1
fi
