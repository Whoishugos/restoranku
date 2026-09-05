"""Terapkan revisi catatan pembimbing (5 September 2026) pada proposal.

Pemakaian:
    python3 revise.py <proposal_sumber.docx> <proposal_hasil.docx>
"""

import sys

from docx import Document

import bab1
import bab2
import bab3a
import bab3b
from docxtools import Doc

DEFAULT_SRC = "proposal_fixed5.docx"
DEFAULT_OUT = "proposal_revisi6.docx"

src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
out = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT

document = Document(src)
TBL = list(document.tables)
D = Doc(document)

bab1.apply(D)
bab2.apply(D, TBL)
bab3a.apply(D, TBL)
bab3b.apply(D, TBL)

document.save(out)
print(f"saved {out} with {len(D.changes)} edit operations")
for c in D.changes:
    print("  -", c)
