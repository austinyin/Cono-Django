import os
if os.environ.get("PROJECT_ENV") != 'production':
    import pymysql
    pymysql.install_as_MySQLdb()
