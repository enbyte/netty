import bcrypt
def salt():
  return bcrypt.gensalt()
def strHash(x):
  return bcrypt.hashpw(x.encode(), salt()).decode('utf-8')
