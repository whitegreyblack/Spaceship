# main implementation of core mechanics
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.start import start

# Start initializations
if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(sys.argv)
    print("script check")
    start()
# End Initiailiation
