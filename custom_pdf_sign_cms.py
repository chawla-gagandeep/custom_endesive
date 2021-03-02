# *-* coding: utf-8 *-*
import sys
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

from endesive.pdf import cms

# from endesive.pdf import cmsn as cms

# import logging
# logging.basicConfig(level=logging.DEBUG)


def main():
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        # "aligned": 0,
        "sigflags": 3,
        # "sigflagsft": 132,
        # "sigpage": 0,
        "sigbutton": False,
        "sigfield": "Signature1",
        "sigandcertify": True,
        "signaturebox": (470, 840, 570, 640),
        "signature": "Dokument podpisany cyfrowo ąćęłńóśżź",
#        "signature_img": "signature_test.png",
        "contact": "mak@trisoft.com.pl",
        "location": "Szczecin",
        "signingdate": date,
        "reason": "Dokument podpisany cyfrowo aą cć eę lł nń oó sś zż zź",
        "password": "1234",
    }
    with open("pdf-signer.p12", "rb") as fp:
        p12 = pkcs12.load_key_and_certificates(
            fp.read(), b"pdfsigner", backends.default_backend()
        )
    fname = "pdf.pdf"
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    datau = open(fname, "rb").read()
    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
    fname = fname.replace(".pdf", "-signed-cms.pdf")
    with open(fname, "wb") as fp:
        fp.write(datau)
        fp.write(datas)


main()