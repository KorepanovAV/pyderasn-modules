import pyderasn
from pyderasn import (
    ObjectIdentifier, Integer, SetOf, Sequence, OctetString, tag_ctxc, Any, Choice
)
from x509 import (
    Certificate, AlgorithmIdentifier, AttributeTypeAndValue
)

from ANY import ANY

class ContentType(ObjectIdentifier):
    pass

# CMSVersion ::= INTEGER  { v0(0), v1(1), v2(2), v3(3), v4(4), v5(5) }
class CMSVersion(Integer):
    schema = (
        ("v0", 0), 
        ("v1", 1), 
        ("v2", 2), 
        ("v3", 3), 
        ("v4", 4), 
        ("v5", 5),
    )

class DigestAlgorithmIdentifier(AlgorithmIdentifier):
    pass

class DigestAlgorithmIdentifiers(SetOf):
    schema = DigestAlgorithmIdentifier()

class EncapsulatedContentInfo(Sequence):
#   EncapsulatedContentInfo ::= SEQUENCE {
#     eContentType ContentType,
#     eContent [0] EXPLICIT OCTET STRING OPTIONAL }
    schema = (
        ("eContentType", ContentType()),
        ("eContent", OctetString(expl=tag_ctxc(0), optional=True)),
    )

class CertificateChoices(Choice):
#   CertificateChoices ::= CHOICE {
#     certificate Certificate,
#     extendedCertificate [0] IMPLICIT ExtendedCertificate,  -- Obsolete
#     v1AttrCert [1] IMPLICIT AttributeCertificateV1,        -- Obsolete
#     v2AttrCert [2] IMPLICIT AttributeCertificateV2,
#     other [3] IMPLICIT OtherCertificateFormat }    
    schema = (
        ("certificate", Certificate()),
    )

class CertificateSet(SetOf):
#CertificateSet ::= SET OF CertificateChoices
    schema = CertificateChoices()

class RevocationInfoChoice(Any):
#   RevocationInfoChoice ::= CHOICE {
#     crl CertificateList,
#     other [1] IMPLICIT OtherRevocationInfoFormat }
    pass

class RevocationInfoChoices(SetOf):
#   RevocationInfoChoices ::= SET OF RevocationInfoChoice
    schema = RevocationInfoChoice()

class SignedAttributes(SetOf):
    schema = AttributeTypeAndValue()
    bounds = (1, float("+inf"))

class UnsignedAttributes(SetOf):
    schema = AttributeTypeAndValue()
    bounds = (1, float("+inf"))

class SignatureAlgorithmIdentifier(AlgorithmIdentifier):
    pass

class SignatureValue(OctetString):
    pass

class SignerInfo(Sequence):
    # SignerInfo ::= SEQUENCE {
    #     version CMSVersion,
    #     sid SignerIdentifier,
    #     digestAlgorithm DigestAlgorithmIdentifier,
    #     signedAttrs [0] IMPLICIT SignedAttributes OPTIONAL,
    #     signatureAlgorithm SignatureAlgorithmIdentifier,
    #     signature SignatureValue,
    #     unsignedAttrs [1] IMPLICIT UnsignedAttributes OPTIONAL }
    schema =(
        ("version", CMSVersion()),
        ("sid", Any()),
        ("digestAlgorithm", DigestAlgorithmIdentifier()),
        ("signedAttrs", SignedAttributes(impl=tag_ctxc(0), optional=True)),
        ("signatureAlgorithm", SignatureAlgorithmIdentifier()),
        ("signature", SignatureValue()),
        ("unsignedAttrs", UnsignedAttributes(impl=tag_ctxc(1), optional=True)),
    )

class SignerInfos(SetOf):
    # SignerInfos ::= SET OF SignerInfo     
    schema = SignerInfo()

class SignedData(Sequence):
#   SignedData ::= SEQUENCE {
#     version CMSVersion,
#     digestAlgorithms DigestAlgorithmIdentifiers,
#     encapContentInfo EncapsulatedContentInfo,
#     certificates [0] IMPLICIT CertificateSet OPTIONAL,
#     crls [1] IMPLICIT RevocationInfoChoices OPTIONAL,
#     signerInfos SignerInfos }
    schema = (
        ("version", CMSVersion()),
        ("digestAlgorithms", DigestAlgorithmIdentifiers()),
        ("encapContentInfo", EncapsulatedContentInfo()),
        ("certificates", CertificateSet(impl=tag_ctxc(0), optional=True)),
        ("crls", RevocationInfoChoices(impl=tag_ctxc(1), optional=True)),
        ("signerInfos", SignerInfos()),
    )

class ContentInfo(Sequence):
    # ContentInfo ::= SEQUENCE {
    #     contentType ContentType,
    #     content [0] EXPLICIT ANY DEFINED BY contentType }
    schema = (
        ("contentType", ContentType(defines=((("content",), {
            ObjectIdentifier("1.2.840.113549.1.7.2"): SignedData(),
        }),))),
        ("content", ANY(expl=tag_ctxc(0))),
    )

if __name__ == "__main__":
    pyderasn.main()