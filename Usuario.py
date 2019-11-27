"""."""


class Usuario:
    """."""

    def __init__(self):
        """."""
        self.lista_usuarios = []

    def insere_usuario(self, nome):
        """."""
        self.lista_usuarios.append(nome)

    def remove_usuario(self, nome):
        """."""
        self.lista_usuarios.remove(nome)
