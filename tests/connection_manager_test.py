from connection_manager.manager import Manager


def test_singleton():

    instance1 = Manager(user="conexion", password="plsL3tM3in",
                        host="127.0.0.1", database_name="tfg_test")
    instance2 = Manager._singleton_instance

    assert(isinstance(instance1, Manager))
    assert(isinstance(instance2, Manager))
