from lark import Transformer, v_args


@v_args(inline=True)
class CalculateTree(Transformer):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock

    def number(self, number):
        """
        Number is either a pitch-class, either a floating point duration.
        """
        pass
