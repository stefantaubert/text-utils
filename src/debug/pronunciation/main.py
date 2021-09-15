from text_utils.pronunciation.main import eng_to_arpa, ger_to_ipa

result = ger_to_ipa(
  eng_sentence="This is a test",
  consider_annotations=False,
)
print(result)
