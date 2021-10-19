from logging import getLogger

from text_utils.text import EngToIpaMode, en_to_ipa

text = "This is /ð/ a test."
res = en_to_ipa(text, EngToIpaMode.EPITRAN,
                replace_unknown_with=None, use_cache=False, logger=getLogger())
print(res)