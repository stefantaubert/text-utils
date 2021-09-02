from g2p_en import G2p

CACHE: G2p = None


def get_eng_g2p() -> G2p:
  # pylint: disable=global-statement
  global CACHE
  if CACHE is None:
    CACHE = G2p()
  return CACHE
