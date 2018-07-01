class Config:
    DEBUG = True
    PORT=9000
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@localhost:3306/test?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = "J\xc2\x9e\xca\x0e\x8e\x89\x89M\xeb(\xbf\xceM$\x91\xa6\xd9$N\xfc\x98\xb0o"