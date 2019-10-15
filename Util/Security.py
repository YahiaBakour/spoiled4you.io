# ourapp/util/security.py
import sys
from itsdangerous import URLSafeTimedSerializer
from Settings.App_Settings import SECRETKEY
sys.path.append("../")
ts = URLSafeTimedSerializer(SECRETKEY)