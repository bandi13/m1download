from dotenv import get_key
from pyotp import *

class account_info:
  def __init__(self,config_file):
    self.config_file = config_file
    self.username = get_key(config_file,'USERNAME')
    self.password = get_key(config_file,'PASSWORD')
    self.otp = TOTP(get_key(config_file, 'OTP_SECRET'))

  def get_username(self):
      return self.username

  def get_password(self):
      return self.password

  def get_otp(self):
      return self.otp.now()
