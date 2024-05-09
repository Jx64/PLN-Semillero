class ValueNotFound(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class ValueTooLong(Exception):
    def __init__(self):
        super().__init__()
