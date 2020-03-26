class oraDB:
    user_name = 'quincya'
    password = 'Welcome1'
    db = '(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = 172.16.92.22 )(PORT = 1521)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = nib_v3prod)))'
    #db = '(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = 172.16.0.34 )(PORT = 1526)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = v3preprod)))'

class jwt:
    secret = 'jwt_secret'

class flask:
    host = '192.168.100.110'
    port = 3001