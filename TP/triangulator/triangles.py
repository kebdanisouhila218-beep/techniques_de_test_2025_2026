class Triangle:
    """
    Représente un triangle obtenu par triangulation.
    """

    def __init__(self, vertices):
        self.vertices = vertices

    def to_binary(self):
        raise NotImplementedError("Conversion binaire non implémentée.")
