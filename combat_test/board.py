from combat_test.blocks import Block


class Board:
    def __init__(self):
        self.chunk_size = cs = 16

        self.chunks = []
        for i in range(cs):
            for j in range(cs):
                pass
