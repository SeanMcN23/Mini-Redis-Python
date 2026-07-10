from server import Server
import time

def test_set_get():
    server = Server()

    assert server.get_response(["SET", "name", "Sean"]) == "OK"
    assert server.get_response(["GET", "name"]) == "Sean"

def test_del():
    server = Server()

    server.get_response(["SET", "name", "Sean"])

    assert server.get_response(["DEL", "name"]) == 1
    assert server.get_response(["GET", "name"]) is None

def test_exists():
    server = Server()

    server.get_response(["SET", "age", "25"])

    assert server.get_response(["EXISTS", "age"]) == 1
    assert server.get_response(["EXISTS", "salary"]) == 0

def test_incr():
    server = Server()

    assert server.get_response(["INCR", "counter"]) == 1
    assert server.get_response(["INCR", "counter"]) == 2

def test_decr():
    server = Server()

    assert server.get_response(["DECR", "counter"]) == -1
    assert server.get_response(["DECR", "counter"]) == -2


def test_save_load():
    server = Server()

    server.get_response(["SET", "name", "Sean"])
    server.get_response(["SAVE"])

    new_server = Server()
    new_server.get_response(["LOAD"])

    assert new_server.get_response(["GET", "name"]) == "Sean"
def test_set_ex():
    server = Server()

    assert server.get_response(["SET", "name", "Sean","EX",3]) == "OK"
    time.sleep(3)
    assert server.get_response(["GET", "name"]) == None
def test_expire():

    server = Server()

    server.get_response(["SET", "name", "Sean"])
    assert server.get_response(["EXPIRE","name","3"]) == 1
    time.sleep(3)
    assert server.get_response(["GET", "name"]) == None


def test_ttl():
    server = Server()

    server.get_response(["SET", "name", "Sean"])
    server.get_response(["SET", "job", "looking"])
    assert server.get_response(["EXPIRE","name","100"]) == 1
    assert server.get_response(["TTL", "job"]) == -1
    assert server.get_response(["TTL", "country"]) == -2
    assert server.get_response(["TTL", "name"]) > 0

def test_keys():
    server = Server()

    server.get_response(["SET", "name", "Sean"])
    server.get_response(["SET", "job", "engineer"])
    server.get_response(["SET", "country", "USA"])

    assert server.get_response(['KEYS']) == ['name','job','country']

def test_mset():
    server = Server()

    assert server.get_response(["MSET", "name", "Sean",'age',"25","job", "none"]) == "OK"
    assert server.get_response(["GET", "name"]) == "Sean"
    assert server.get_response(["GET", "age"]) == "25"
    assert server.get_response(["GET", "job"]) == "none"

    
def test_mget():
    server = Server()

    assert server.get_response(["MSET", "name", "Sean",'age',"25","job", "none"]) == "OK"
    assert server.get_response(["MGET",'name','age','job']) == ['Sean','25','none']

def test_rename():

    server= Server()

    server.get_response(["SET", "job", "engineer"])
    assert server.get_response(["RENAME", "job", "curr_job"])== "OK"

def test_dbsize():
    server = Server()

    assert server.get_response(["MSET", "name", "Sean",'age',"25","job", "none"]) == "OK"

    assert server.get_response(["DBSIZE"])== 3

    assert server.get_response(["EXPIRE","name","3"]) == 1
    time.sleep(3)

    assert server.get_response(["DBSIZE"])== 2


def test_flushdb():
    server = Server()
    assert server.get_response(["MSET", "name", "Sean",'age',"25","job", "none"]) == "OK"

    assert server.get_response(["DBSIZE"])== 3

    assert server.get_response(["FLUSHDB"]) == "OK"
    assert server.get_response(["DBSIZE"])== 0

def test_type():
    server=Server()

    assert server.get_response(["MSET", "name", "Sean",'age',"25","job", "none"]) == "OK"
    assert server.get_response(["TYPE", 'name']) == 'string'
    assert server.get_response(["TYPE", 'age']) == 'string'
    assert server.get_response(["TYPE", 'job']) == 'string'
    assert server.get_response(["TYPE", 'country']) == 'None'






    








