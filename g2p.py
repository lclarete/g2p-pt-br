#!/usr/bin/env python
"""Porto Alegre Dialect - Portuguese g2p rules."""

import pynini
from pynini.lib import rewrite
import string


# Characters in International Phonetic Alphabet (IPA)
ipa = pynini.union( 'ʒ', 'ʃ', 'ç', 'á', 'ʎ', 'ʁ', 'ɾ', 'ɲ', "ɐ̃", "ã", "ɐ̃", "w̃")
alphabet = pynini.union(*string.ascii_lowercase)

SIGMA_STAR = pynini.union(ipa, alphabet).closure()

# it helps me to visualize and review the empty space
empty_str = ""

# Portugese rule set given
G2P = (
    # straighforward replacements
    # some digraphs, silent h and á 
    pynini.cdrewrite(
        pynini.union(
            pynini.cross("ch", "ʃ"), # chato, chulé, chama
            pynini.cross("lh", "ʎ"), # filho, trabalho, lhama
            pynini.cross("nh", "ɲ"), # ninho, passarinho, vinheta
            pynini.cross("h", empty_str), # silent H
            pynini.cross("á", "a"), # rápido, sabiá, átila
            ),
        empty_str,
        empty_str,
        SIGMA_STAR).optimize()

    # Nasal Vowels
    # o sounds like w̃ when preceded by ã in words such as não, irmão, são, salão
    @ pynini.cdrewrite(
        pynini.cross("o", "w̃"),
        pynini.union("ã"),
        empty_str,
        SIGMA_STAR,
    ).optimize()

    @ pynini.cdrewrite(
        pynini.union(
    # ã/ â sound like ɐ̃" such as sã, irmã, maçã, âncora
            pynini.cross("ã", "ɐ̃"),
            pynini.cross("â", "ɐ̃"),

    # vowels are transformed to nasal when followed by n
    # For example, "an" should be replaced by "ɐ̃"
            pynini.cross("an", "ɐ̃"),
            pynini.cross("on", "õ"),
            pynini.cross("un", "ũ"),
            # pynini.cross("en", "ẽ"),
            ),
        empty_str,
        empty_str,
        SIGMA_STAR).optimize()
    
      # e sounds like i in the end of the string, including plurals
      # such as in verdade, interesse, santidade
    @ pynini.cdrewrite(
        pynini.cross("e", "i"),
        empty_str,
        # strings ending in e or i
        # same rule for plurals, accepting s at the end
        pynini.union("[EOS]", "s[EOS]"),
        SIGMA_STAR,
    ).optimize()
      
    # o sounds like u in the end of the string, or before the letter r
    # unless it's preceded by ã
    # such as in cimento, chato, canto, amigo, casado
    @ pynini.cdrewrite(
        pynini.cross("o", "u"),
        empty_str,
        pynini.union("[EOS]", "s[EOS]"),
        SIGMA_STAR,
    ).optimize()

    # "c" sounds like s when followed by i and e
    # such as in cimento, cinto, centavo, cesta
    @ pynini.cdrewrite(
        pynini.cross("c", "s"), empty_str, pynini.union("i", "e"), SIGMA_STAR).optimize()

    # "c" sounds like k when followed by the vowels "a", "o", and "u", 
    # such as in casa, calúnia, cômoda, cúmulo
    @ pynini.cdrewrite(
        pynini.cross("c", "k"), empty_str, pynini.union("a", "o", "u"), SIGMA_STAR).optimize()
        
    # Word-final z sounds like s
    # such as in luz, vez, voz
    @ pynini.cdrewrite(
        pynini.cross("z", "s"), empty_str, "[EOS]", SIGMA_STAR).optimize()

    # r sound like ʁ in the beginning of the word
    # such as in rápido, rato, rio, reiterar
    @ pynini.cdrewrite(
        pynini.cross("r", "ʁ"), "[BOS]", empty_str, SIGMA_STAR).optimize()
    
    # r sound like ɾ when followed by the vowels a, e, i and consonants
    @ pynini.cdrewrite(
        pynini.cross("r", "ɾ"), 
        empty_str,
        pynini.union("a", "e", "i", "b", "c", "d", "f", "g", "l", "m", "n", "p", "q", "s", "t"), 
        SIGMA_STAR).optimize()


    # s is replaced by z when it's between vowels 
    @ pynini.cdrewrite(
        pynini.cross("s", "z"),
        pynini.union("a", "e", "i", "o", "u"),
        pynini.union("a", "e", "i", "o", "u"),
        SIGMA_STAR,
    ).optimize()

    # t and d sounds when followed by i
    @ pynini.cdrewrite(
        pynini.union(
            pynini.cross("t", "tʃ"), 
            pynini.cross("d", "dʒ")),
            empty_str,
            "i",
            SIGMA_STAR).optimize()
       
    # other sounds
    @ pynini.cdrewrite(
        pynini.union(
            pynini.cross("sç", "s"),
            pynini.cross("ss", "s"),
            pynini.cross("rr", "ʁ"),
            pynini.cross("ç", "s")
        ),
        empty_str,
        empty_str,
        SIGMA_STAR).optimize()

        # optimizing the resulting FSA
).optimize()


def g2p(istring: str) -> str:
    """Applies the G2P rule.

    Args:
      istring: the graphemic input string.

    Returns:
      The phonemic output string.

    Raises.
      rewrite.Error: composition failure.
    """
    return rewrite.one_top_rewrite(istring, G2P)
