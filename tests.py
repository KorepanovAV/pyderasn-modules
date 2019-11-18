from pyderasn import (
    OctetString, Sequence, tag_ctxp, hexdec
)

class KeyIdentifier(OctetString):
    # KeyIdentifier ::= OCTET STRING
    pass

class AuthorityKeyIdentifier(Sequence):
    # AuthorityKeyIdentifier ::= SEQUENCE {
    #     keyIdentifier             [0] KeyIdentifier           OPTIONAL,
    #     authorityCertIssuer       [1] GeneralNames            OPTIONAL,
    #     authorityCertSerialNumber [2] CertificateSerialNumber OPTIONAL  }
    schema = (
        ("keyIdentifier", KeyIdentifier(impl=tag_ctxp(0), optional=True)),
        # ("authorityCertIssuer", GeneralNames(impl=tag_ctxc(1), optional=True)),
        # ("authorityCertSerialNumber", CertificateSerialNumber(impl=tag_ctxc(2), optional=True)),
    )

aki = AuthorityKeyIdentifier()
data = hexdec("30168014908405070B39992EDAFEA1F549E948189B2F0DF3")
aki.decode(data)