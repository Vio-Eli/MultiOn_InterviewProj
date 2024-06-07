from multion.client import MultiOn
import os


# Initialize MultiOn
def init_multion():
    return MultiOn(api_key=os.getenv("MULTION_API_KEY"))