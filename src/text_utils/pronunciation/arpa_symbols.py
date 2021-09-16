AA = "AA"
AE = "AE"
AH = "AH"
AO = "AO"
AW = "AW"
AX = "AX"
AXR = "AXR"
AY = "AY"
EH = "EH"
ER = "ER"
EY = "EY"
IH = "IH"
IX = "IX"
IY = "IY"
OW = "OW"
OY = "OY"
UH = "UH"
UW = "UW"
UX = "UX"

B = "B"
CH = "CH"
D = "D"
DH = "DH"
DX = "DX"
EL = "EL"
EM = "EM"
EN = "EN"
F = "F"
G = "G"
HH = "HH"
H = "H"
JH = "JH"
K = "K"
L = "L"
M = "M"
N = "N"
NG = "NG"
NX = "NX"
P = "P"
Q = "Q"
R = "R"
S = "S"
SH = "SH"
T = "T"
TH = "TH"
V = "V"
W = "W"
WH = "WH"
Y = "Y"
Z = "Z"
ZH = "ZH"


VOWELS = {
  AA,
  AE,
  AH,
  AO,
  AW,
  AX,
  AXR,
  AY,
  EH,
  ER,
  EY,
  IH,
  IX,
  IY,
  OW,
  OY,
  UH,
  UW,
  UX,
}

STRESS_NONE = "0"
STRESS_NONE_ALT = ""
STRESS_PRIMARY = "1"
STRESS_SECONDARY = "2"

STRESS_MARKERS = {STRESS_NONE, STRESS_NONE_ALT, STRESS_PRIMARY, STRESS_SECONDARY}

VOWELS_WITH_STRESSES = {
    f"{vowel}{stress_nr}" for vowel in VOWELS for stress_nr in STRESS_MARKERS}

CONSONANTS = {
  B,
  CH,
  D,
  DH,
  DX,
  EL,
  EM,
  EN,
  F,
  G,
  HH,
  H,
  JH,
  K,
  L,
  M,
  N,
  NG,
  NX,
  P,
  Q,
  R,
  S,
  SH,
  T,
  TH,
  V,
  W,
  WH,
  Y,
  Z,
  ZH,
}

ALL_ARPA_EXCL_STRESSES = VOWELS | CONSONANTS
ALL_ARPA_INCL_STRESSES = VOWELS_WITH_STRESSES | CONSONANTS
