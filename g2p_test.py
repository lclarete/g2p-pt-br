#!/usr/bin/env python
"""Unit tests for Portuguese G2P."""

import unittest
import g2p


class G2PTest(unittest.TestCase):
    def rewrites(self, istring: str, expected_ostring: str) -> None:
        """Asserts that the g2p rule produces the correct output.

        Note that this itself is not a unit test because its name does not
        begin with `test_`; but it can be used to implement other unit tests.

        Args:
            istring: the input string
            expected_ostring: the expected output string.
        """
        ostring = g2p.g2p(istring)
        self.assertEqual(ostring, expected_ostring)

    def test_vez(self):
        self.rewrites("vez", "ves")
    
    def test_cases(self):
        self.rewrites("cases", "kazis")

    def test_cimento(self):
        self.rewrites("cimento", "simentu")

    def test_chato(self):
        self.rewrites("chato", "ʃatu")

    def test_casa(self):
        self.rewrites("casa", "kaza")

    def test_luz(self):
        self.rewrites("luz", "lus")

    def test_nasco(self):
        self.rewrites("nasço", "nasu")

    def test_filho(self):
        self.rewrites("filho", "fiʎu")

    def test_homem(self):
        self.rewrites("homem", "omem")

    def test_ninho(self):
        self.rewrites("ninho", "niɲu")

    # stretch goal
    def test_braco(self):
        self.rewrites("braço", "bɾasu")

    def test_carro(self):
        self.rewrites("carro", "kaʁu")

    def test_interesse(self):
        self.rewrites("interesse", "inteɾesi")

    def test_partes(self):
        self.rewrites("partes", "paɾtʃis")

    def test_rapido(self):
        self.rewrites("rápido", "ʁapidu")

    def test_verdade(self):
        self.rewrites("verdade", "veɾdadʒi")

    # nasal vowels
    def test_nao(self):
        self.rewrites("não", "nɐ̃w̃")
    
    def test_maca(self):
        self.rewrites("maçã", "masɐ̃")
        
    def test_anta(self):
        self.rewrites("anta", "ɐ̃ta")

if __name__ == "__main__":
    unittest.main()
