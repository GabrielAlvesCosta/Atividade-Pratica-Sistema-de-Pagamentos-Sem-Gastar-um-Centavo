import sys
import os

raiz = os.path.abspath(os.path.dirname(__file__))
if raiz not in sys.path:
    sys.path.insert(0, raiz)