import unittest
from logging import getLogger

from text_utils.ipa2symb import IPAExtractionSettings, extract_from_sentence
from text_utils.language import Language
from text_utils.text import (EngToIpaMode, text_normalize, text_to_ipa,
                             text_to_symbols)


class UnitTests(unittest.TestCase):
  def test_unprocessable_ipa(self):
    x = "ɡɹât͡ʃi"
    settings = IPAExtractionSettings(
      ignore_tones=True,
      ignore_arcs=True,
      replace_unknown_ipa_by='_'
    )

    res = extract_from_sentence(x, settings, getLogger())

    self.assertEqual(['_', '_', '_', '_', '_', '_', '_'], res)

    #y = u"ˈprɪnɪŋ, ɪn ðə ˈoʊnli sɛns wɪθ wɪʧ wi ər æt ˈprɛzənt kənˈsərnd, ˈdɪfərz frəm moʊst ɪf nɑt frəm ɔl ðə ɑrts ənd kræfts ˌrɛprɪˈzɛnɪd ɪn ðə ˌɛksəˈbɪʃən."
    #y = u"naw, æz ɔl bʊks nɑt pɹajmɛɹəli ɪntɛndəd æz pɪkt͡ʃɹ̩-bʊks kənsɪst pɹɪnsɪpli ʌv tajps kəmpowzd tə fɔɹm lɛtɹ̩pɹɛs"
    #y = u"ɪʧ kt͡ʃɹ̩?"
    #y = u"tɕy˥˩ɕi˥ meɪ˧˩˧kwɔ˧˥ tsʰan˥i˥˩ɥœn˥˩ i˧˩˧ tsʰɑʊ˧˩˧ni˧˩˧ i˥ fən˥˩ ʈʂɨ˥ʈʂʰɨ˧˥ kʰɤ˥˩lin˧˥twən˥˩ ɕjɑŋ˥˩ pwɔ˥xeɪ˥ pʰaɪ˥˩piŋ˥ tɤ tɕɥœ˧˥i˥˩an˥˩ ʈʂwən˧˩˧peɪ˥˩ tsaɪ˥˩ pən˧˩˧ɥœ˥˩ ʂɑŋ˥˩ɕyn˧˥ tɕin˥˩ɕiŋ˧˥ pjɑʊ˧˩˧tɕɥœ˧˥ t˥˩ʃ˥˩"
    #y = "t˥˩ʃ˥˩?"
    #y = u"wɪʧ"
    #y = "ɪʃn̩'"

    #res = extract_from_sentence(y, ignore_tones=False, ignore_arcs=False)
    # print(''.join(res))
    #res = extract_from_sentence(y, ignore_tones=True, ignore_arcs=False)
    # print(''.join(res))
    #res = extract_from_sentence(y, ignore_tones=False, ignore_arcs=True)
    # print(''.join(res))
    # print(res)
    # print(set(res))
    # print(len(set(res)))a
if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
