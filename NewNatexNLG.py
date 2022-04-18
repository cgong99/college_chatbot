from emora_stdm import NatexNLG
import regex

class NewNatexNLG(NatexNLG):
    def is_complete(self, string=None):
        if string is None:
            string = self._expression
        return bool(regex.fullmatch(r'[^$]*', string))