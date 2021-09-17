from text_utils.pronunciation.chinese_ipa import (__get_chn_ipa, chn_to_ipa,
                                                  get_vowel_count)
from text_utils.pronunciation.main import clear_ipa_cache


def test_get_chn_ipa():
  result = __get_chn_ipa(tuple("堡包"))

  clear_ipa_cache()
  assert result == ('p', 'ɑʊ˧˩˧', 'p', 'ɑʊ˥',)


def test_get_chn_ipa__syllable_without_vowel():
  result = __get_chn_ipa(tuple("儿"))

  clear_ipa_cache()
  assert result == ('ɻ',)


def test_get_vowel_count__two():
  result = get_vowel_count(
    symbols=("a", "b", "aa",),
  )

  assert result == 2


def test_get_vowel_count__one_diphtong():
  result = get_vowel_count(
    symbols=("aa",),
  )

  assert result == 1


def test_get_vowel_count__one():
  result = get_vowel_count(
    symbols=("a",),
  )

  assert result == 1


def test_get_vowel_count__zero():
  result = get_vowel_count(
    symbols=(),
  )

  assert result == 0


def test_chn_to_ipa():
  result = chn_to_ipa(
    chn_sentence=tuple("石头 北 冷。"),
    consider_annotations=False,
    annotation_split_symbol=None,
  )

  clear_ipa_cache()
  assert result == ('ʂ', 'ɨ˧˥', 'tʰ', 'oʊ', ' ', 'p', 'eɪ˧˩˧', ' ', 'l', 'ɤ˧˩˧', 'ŋ', '.',)


def test_chn_to_ipa__with_multiple_same_words():
  result = chn_to_ipa(
    chn_sentence=tuple("！石 石？ 石。"),
    consider_annotations=False,
    annotation_split_symbol=None,
  )

  clear_ipa_cache()
  assert result == ('!', 'ʂ', 'ɨ˧˥', ' ', 'ʂ', 'ɨ˧˥', '?', ' ', 'ʂ', 'ɨ˧˥', '.')


def test_chn_to_ipa__replaces_punctuation():
  result = chn_to_ipa(
    chn_sentence=tuple("石头！ 北： 冷。 ？"),
    consider_annotations=False,
    annotation_split_symbol=None,
  )

  clear_ipa_cache()
  assert result == ('ʂ', 'ɨ˧˥', 'tʰ', 'oʊ', '!', ' ', 'p', 'eɪ˧˩˧',
                    ':', ' ', 'l', 'ɤ˧˩˧', 'ŋ', '.', ' ', '?')


def test_chn_to_ipa__sentence():
  result = chn_to_ipa(
    chn_sentence=tuple("仅 绘画 而论 齐白石 是 巍巍 昆仑 可 这位 附庸风雅 的 门外汉 连 一块 石头 都 不是"),
    consider_annotations=False,
    annotation_split_symbol=None,
  )

  clear_ipa_cache()
  assert result == ('t', 'ɕ', 'i˧˩˧', 'n', ' ', 'x', 'w', 'eɪ˥˩', 'x', 'w', 'a˥˩', ' ', 'ɑ˧˥', 'ɻ', 'l', 'w', 'ə˥˩', 'n', ' ', 't', 'ɕʰ', 'i˧˥', 'p', 'aɪ˧˥', 'ʂ', 'ɨ˧˥', ' ', 'ʂ', 'ɨ˥˩', ' ', 'w', 'eɪ˥', 'w', 'eɪ˥', ' ', 'kʰ', 'w', 'ə˥', 'n', 'l', 'w', 'ə˧˥', 'n', ' ', 'kʰ', 'ɤ˧˩˧', ' ',
                    'ʈ', 'ʂ', 'ɤ˥˩', 'w', 'eɪ˥˩', ' ', 'f', 'u˥˩', 'yʊ˥', 'ŋ', 'f', 'ɤ˥', 'ŋ', 'j', 'a˧˩˧', ' ', 't', 'ɤ', ' ', 'm', 'ə˧˥', 'n', 'w', 'aɪ˥˩', 'x', 'a˥˩', 'n', ' ', 'l', 'j', 'ɛ˧˥', 'n', ' ', 'i˥', 'kʰ', 'w', 'aɪ˥˩', ' ', 'ʂ', 'ɨ˧˥', 'tʰ', 'oʊ', ' ', 't', 'oʊ˥', ' ', 'p', 'u˥˩', 'ʂ', 'ɨ˥˩')
