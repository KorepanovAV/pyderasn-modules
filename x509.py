from pyderasn import (
    Sequence, SequenceOf, ObjectIdentifier, Boolean, OctetString, Integer, tag_ctxc, Choice, SetOf, Any, IA5String,
    TeletexString, PrintableString, UniversalString, UTF8String, BMPString, UTCTime, BitString, tag_ctxp, GeneralizedTime
)

from ANY import ANY
from OCTETSTRING import OCTETSTRING

class CertificateSerialNumber(Integer):
    pass

class Version(Integer):
    # Version  ::=  INTEGER  {  v1(0), v2(1), v3(2)  }    
    schema = (("v1", 0), ("v2", 1), ("v3", 2))

class AlgorithmIdentifier(Sequence):
    # AlgorithmIdentifier  ::=  SEQUENCE  {
    #     algorithm               OBJECT IDENTIFIER,
    #     parameters              ANY DEFINED BY algorithm OPTIONAL  }
    #                                 -- contains a value of the type
    #                                 -- registered for use with the
    #                                 -- algorithm object identifier value
    schema = (
        ("algorithm", ObjectIdentifier()),
        ("parameters", Any(optional=True)),
    )

class AttributeType(ObjectIdentifier):
    # AttributeType           ::= OBJECT IDENTIFIER
    pass

class AttributeValue(ANY):
    # AttributeValue          ::= ANY -- DEFINED BY AttributeType
    pass

class Attribute(Sequence):
    schema = (
        ("type", AttributeType()),
        ("values", SetOf(schema=AttributeValue, bounds=(1, float("+inf")))),
    )

def DirectoryString(className, bounds):
    # -- Directory string type --

    # DirectoryString{INTEGER:maxSize} ::= CHOICE {
    #     teletexString    TeletexString(SIZE (1..maxSize)),
    #     printableString  PrintableString(SIZE (1..maxSize)),
    #     bmpString        BMPString(SIZE (1..maxSize)),
    #     universalString  UniversalString(SIZE (1..maxSize)),
    #     uTF8String       UTF8String(SIZE (1..maxSize))
    # }    
	return type(className, (Choice,), dict(
        schema = (
            ("teletexString", TeletexString(bounds=bounds)),
            ("printableString", PrintableString(bounds=bounds)),
            ("universalString", UniversalString(bounds=bounds)),
            ("utf8String", UTF8String(bounds=bounds)),
            ("bmpString", BMPString(bounds=bounds)),
        ))
    )

# -- Upper Bounds
ub_state_name = 128
ub_organization_name = 64
ub_organizational_name = 64
ub_title = 64
ub_serial_number = 64
ub_pseudonym = 128
ub_emailaddress_length = 255
ub_locality_name = 128
ub_common_name = 64
ub_name = 32768

# id-at OBJECT IDENTIFIER ::= { joint-iso-ccitt(2) ds(5) 4 }
id_at = ObjectIdentifier((2, 5, 4))

# -- Naming attributes of type X520name
# id-at-name                AttributeType ::= { id-at 41 }
# id-at-surname             AttributeType ::= { id-at  4 }
# id-at-givenName           AttributeType ::= { id-at 42 }
# id-at-initials            AttributeType ::= { id-at 43 }
# id-at-generationQualifier AttributeType ::= { id-at 44 }

id_at_name = AttributeType(id_at + (41, ))
id_at_surname = AttributeType(id_at + (4, ))
id_at_givenName = AttributeType(id_at + (42, ))
id_at_initials = AttributeType(id_at + (43, ))
id_at_generationQualifier = AttributeType(id_at + (44, ))

# -- Naming attributes of type X520Name:
# --   X520name ::= DirectoryString (SIZE (1..ub-name))
X520Name = DirectoryString("X520Name", bounds=(1, ub_name))

# -- Naming attributes of type X520CommonName
# id-at-commonName        AttributeType ::= { id-at 3 }
id_at_commonName = AttributeType(id_at + (3, ))

# -- Naming attributes of type X520CommonName:
# --   X520CommonName ::= DirectoryName (SIZE (1..ub-common-name))
X520CommonName = DirectoryString("X520CommonName", bounds=(1, ub_common_name))

# -- Naming attributes of type X520countryName (digraph from IS 3166)
# id-at-countryName       AttributeType ::= { id-at 6 }
id_at_countryName = AttributeType(id_at + (6,))

# X520countryName ::=     PrintableString (SIZE (2))
class X520CountryName(PrintableString):
    bounds = (2, 2)

# -- Naming attributes of type X520LocalityName
# id-at-localityName      AttributeType ::= { id-at 7 }
id_at_localityName = AttributeType(id_at + (7, ))

# -- Naming attributes of type X520LocalityName:
# --   X520LocalityName ::= DirectoryName (SIZE (1..ub-locality-name))
X520LocalityName = DirectoryString("X520LocalityName", bounds=(1, ub_locality_name))

# -- Naming attributes of type X520StateOrProvinceName
# id-at-stateOrProvinceName AttributeType ::= { id-at 8 }
id_at_stateOrProvinceName = AttributeType(id_at + (8,))

# -- Naming attributes of type X520StateOrProvinceName:
# --   X520StateOrProvinceName ::= DirectoryName (SIZE (1..ub-state-name))
X520StateOrProvinceName = DirectoryString("X520StateOrProvinceName", bounds=(1, ub_state_name))

# -- Naming attributes of type X520OrganizationName
# id-at-organizationName  AttributeType ::= { id-at 10 }
id_at_organizationName = AttributeType(id_at + (10,))

# -- Naming attributes of type X520OrganizationName:
# --   X520OrganizationName ::= DirectoryName (SIZE (1..ub-organization-name))
X520OrganizationName = DirectoryString("X520OrganizationName", bounds=(1, ub_organization_name))

# -- Naming attributes of type DomainComponent (from RFC 4519)
# id-domainComponent   AttributeType ::= { 0 9 2342 19200300 100 1 25 }
id_domainComponent = AttributeType((0, 9, 2342, 19200300, 100, 1, 25,))

# DomainComponent ::=  IA5String
class DomainComponent(IA5String):
    pass

class AttributeTypeAndValue(Sequence):
    # AttributeTypeAndValue   ::= SEQUENCE {
    #         type    AttributeType,
    #         value   AttributeValue }    
    schema = (
        ("type", AttributeType(defines=((("value",), {
            id_at_name: X520Name(),
            id_at_surname: X520Name(),
            id_at_givenName: X520Name(),
            id_at_initials: X520Name(),
            id_at_generationQualifier: X520Name(),
            id_at_commonName: X520CommonName(),
            id_at_countryName: X520CountryName(),
            id_at_localityName: X520LocalityName(),
            id_at_stateOrProvinceName: X520StateOrProvinceName(),
            id_at_organizationName: X520OrganizationName(),
            id_domainComponent: DomainComponent(),
        }),))),
        ("value", AttributeValue()),
    )

class RelativeDistinguishedName(SetOf):
    # RelativeDistinguishedName ::= SET SIZE (1..MAX) OF AttributeTypeAndValue    
    schema = AttributeTypeAndValue()
    bounds = (1, float("+inf"))

class RDNSequence(SequenceOf):
    # RDNSequence ::= SEQUENCE OF RelativeDistinguishedName    
    schema = RelativeDistinguishedName()

class Time(Choice):
    schema = (
        ("utcTime", UTCTime()),
        ("generalTime", GeneralizedTime()),
    )

class Validity(Sequence):
    schema = (
        ("notBefore", Time()),
        ("notAfter", Time()),
    )

class SubjectPublicKeyInfo(Sequence):
    schema = (
        ("algorithm", AlgorithmIdentifier()),
        ("subjectPublicKey", BitString()),
    )

class UniqueIdentifier(BitString):
    pass

class Name(Choice):
    # Name ::= CHOICE { -- only one possibility for now --
    #     rdnSequence  RDNSequence }    
    schema = (
        ("rdnSequence", RDNSequence()),)

class EDIPartyName(Sequence):
# EDIPartyName ::= SEQUENCE {
#     nameAssigner            [0]     DirectoryString OPTIONAL,
#     partyName               [1]     DirectoryString }
    pass

class ORAddress(Sequence):
# ORAddress ::= SEQUENCE {
#    built-in-standard-attributes BuiltInStandardAttributes,
#    built-in-domain-defined-attributes
#                    BuiltInDomainDefinedAttributes OPTIONAL,
#    -- see also teletex-domain-defined-attributes
#    extension-attributes ExtensionAttributes OPTIONAL }
    pass

class OtherName(Sequence):
    #    OtherName ::= SEQUENCE {
    #         type-id    OBJECT IDENTIFIER,
    #         value      [0] EXPLICIT ANY DEFINED BY type-id }
    schema = (
        ("type-id", ObjectIdentifier()),
        ("value", Any(expl=tag_ctxc(0))),
    )

class GeneralName(Choice): 
#    GeneralName ::= CHOICE {
#         otherName                       [0]     OtherName,
#         rfc822Name                      [1]     IA5String,
#         dNSName                         [2]     IA5String,
#         x400Address                     [3]     ORAddress,
#         directoryName                   [4]     Name,
#         ediPartyName                    [5]     EDIPartyName,
#         uniformResourceIdentifier       [6]     IA5String,
#         iPAddress                       [7]     OCTET STRING,
#         registeredID                    [8]     OBJECT IDENTIFIER }
    schema = (
        ("otherName", OtherName(impl=tag_ctxp(0))),
        ("rfc822Name", IA5String(impl=tag_ctxp(1))),
        ("dNSName", IA5String(impl=tag_ctxp(2))),
        ("x400Address", ORAddress(impl=tag_ctxp(3))),
        ("directoryName", Name(expl=tag_ctxp(4))),
        ("ediPartyName", EDIPartyName(impl=tag_ctxp(5))),
        ("uniformResourceIdentifier", IA5String(impl=tag_ctxp(6))),
        ("iPAddress", OctetString(impl=tag_ctxp(7))),
        ("registeredID", ObjectIdentifier(impl=tag_ctxp(8))),
    )

class GeneralNames(SequenceOf):
    #    GeneralNames ::= SEQUENCE SIZE (1..MAX) OF GeneralName
    schema = GeneralName()
    bounds = (1, float("+inf"))

# id-ce   OBJECT IDENTIFIER ::=  { joint-iso-ccitt(2) ds(5) 29 }
id_ce = ObjectIdentifier((2, 5, 29))

# id-ce-authorityKeyIdentifier OBJECT IDENTIFIER ::=  { id-ce 35 }
id_ce_authorityKeyIdentifier = ObjectIdentifier(id_ce + (35,))

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
        ("authorityCertIssuer", GeneralNames(impl=tag_ctxc(1), optional=True)),
        ("authorityCertSerialNumber", CertificateSerialNumber(impl=tag_ctxc(2), optional=True)),
    )

# id-ce-keyUsage OBJECT IDENTIFIER ::=  { id-ce 15 }
id_ce_keyUsage = ObjectIdentifier(id_ce + (15,))

class KeyUsage(BitString):
# KeyUsage ::= BIT STRING {
#     digitalSignature        (0),
#     nonRepudiation          (1), -- recent editions of X.509 have
#                         -- renamed this bit to contentCommitment
#     keyEncipherment         (2),
#     dataEncipherment        (3),
#     keyAgreement            (4),
#     keyCertSign             (5),
#     cRLSign                 (6),
#     encipherOnly            (7),
#     decipherOnly            (8) } 
    schema = (
        ("digitalSignature", 0),
        ("nonRepudiation", 1),
        ("keyEncipherment", 2),
        ("dataEncipherment", 3),
        ("keyAgreement", 4),
        ("keyCertSign", 5),
        ("cRLSign", 6),
        ("encipherOnly", 7),
        ("decipherOnly", 8),
    )

# id-ce-extKeyUsage OBJECT IDENTIFIER ::= { id-ce 37 }
id_ce_extKeyUsage = ObjectIdentifier(id_ce + (37,))

class KeyPurposeId(ObjectIdentifier):
# KeyPurposeId ::= OBJECT IDENTIFIER 
    pass

class ExtKeyUsage(SequenceOf):
    # ExtKeyUsageSyntax ::= SEQUENCE SIZE (1..MAX) OF KeyPurposeId
    bounds = (1, float("+inf"))
    schema = KeyPurposeId()

# id-ce-cRLDistributionPoints OBJECT IDENTIFIER ::=  { id-ce 31 }
id_ce_cRLDistributionPoints = ObjectIdentifier(id_ce + (31,))

class ReasonFlags(BitString):
    # ReasonFlags ::= BIT STRING {
    #     unused                  (0),
    #     keyCompromise           (1),
    #     cACompromise            (2),
    #     affiliationChanged      (3),
    #     superseded              (4),
    #     cessationOfOperation    (5),
    #     certificateHold         (6),
    #     privilegeWithdrawn      (7),
    #     aACompromise            (8) }
    schema = (
        ("unused", 0),
        ("keyCompromise", 1),
        ("cACompromise", 2),
        ("affiliationChanged", 3),
        ("superseded", 4),
        ("cessationOfOperation", 5),
        ("certificateHold", 6),
        ("privilegeWithdrawn", 7),
        ("aACompromise", 8),         
    )

class DistributionPointName(Choice):
    # DistributionPointName ::= CHOICE {
    #     fullName                [0]     GeneralNames,
    #     nameRelativeToCRLIssuer [1]     RelativeDistinguishedName }
    schema = (
        ("fullName", GeneralNames(impl=tag_ctxc(0))),
        ("nameRelativeToCRLIssuer", RelativeDistinguishedName(impl=tag_ctxc(1))),
    )

class DistributionPoint(Sequence):
    # DistributionPoint ::= SEQUENCE {
    #     distributionPoint       [0]     DistributionPointName OPTIONAL,
    #     reasons                 [1]     ReasonFlags OPTIONAL,
    #     cRLIssuer               [2]     GeneralNames OPTIONAL }
    schema = (
        ("distributionPoint", DistributionPointName(expl=tag_ctxc(0), optional=True)),
        ("reasons", ReasonFlags(impl=tag_ctxc(1), optional=True)),
        ("cRLIssuer", GeneralNames(impl=tag_ctxc(2), optional=True))
    )

class CRLDistributionPoints(SequenceOf):
    # CRLDistributionPoints ::= SEQUENCE SIZE (1..MAX) OF DistributionPoint
    schema = DistributionPoint()
    bounds = (1, float("+inf"))

# id-pkix  OBJECT IDENTIFIER  ::=
#     { iso(1) identified-organization(3) dod(6) internet(1) security(5) mechanisms(5) pkix(7) }
id_pkix = ObjectIdentifier((1, 3, 6, 1, 5, 5, 7))
id_pe = ObjectIdentifier(id_pkix + (1,))

# id-pe-authorityInfoAccess OBJECT IDENTIFIER ::= { id-pe 1 }
id_pe_authorityInfoAccess = ObjectIdentifier(id_pe + (1,))

class AccessDescription(Sequence):
    # AccessDescription  ::=  SEQUENCE {
    #     accessMethod          OBJECT IDENTIFIER,
    #     accessLocation        GeneralName  }
    schema = (
        ("accessMethod", ObjectIdentifier()),
        ("accessLocation", GeneralName()),
    )

class AuthorityInfoAccess(SequenceOf):
# AuthorityInfoAccessSyntax  ::=
#     SEQUENCE SIZE (1..MAX) OF AccessDescription
    schema = AccessDescription()
    bounds = (1, float("+inf"))

class Extension(Sequence):
    # Extension  ::=  SEQUENCE  {
    #     extnID      OBJECT IDENTIFIER,
    #     critical    BOOLEAN DEFAULT FALSE,
    #     extnValue   OCTET STRING
    #     }
    schema = (
        ("extnID", ObjectIdentifier(defines=((("extnValue",), {
            id_ce_authorityKeyIdentifier: AuthorityKeyIdentifier(),
            id_ce_keyUsage: KeyUsage(),
            id_ce_extKeyUsage: ExtKeyUsage(),
            id_ce_cRLDistributionPoints: CRLDistributionPoints(),
            id_pe_authorityInfoAccess: AuthorityInfoAccess(),
        }),))),
        ("critical", Boolean(default=False)),
        ("extnValue", OCTETSTRING()), # OctetString()),
    )

class Extensions(SequenceOf):
    schema = Extension()
    bounds = (1, float("+inf"))

class TBSCertificate(Sequence):
    # TBSCertificate  ::=  SEQUENCE  {
    #     version         [0]  Version DEFAULT v1,
    #     serialNumber         CertificateSerialNumber,
    #     signature            AlgorithmIdentifier,
    #     issuer               Name,
    #     validity             Validity,
    #     subject              Name,
    #     subjectPublicKeyInfo SubjectPublicKeyInfo,
    #     issuerUniqueID  [1]  IMPLICIT UniqueIdentifier OPTIONAL,
    #                         -- If present, version MUST be v2 or v3
    #     subjectUniqueID [2]  IMPLICIT UniqueIdentifier OPTIONAL,
    #                         -- If present, version MUST be v2 or v3
    #     extensions      [3]  Extensions OPTIONAL
    #                         -- If present, version MUST be v3 --  }    
    schema = (
        ("version", Version(expl=tag_ctxc(0), default="v1")),
        ("serialNumber", CertificateSerialNumber()),
        ("signature", AlgorithmIdentifier()),
        ("issuer", Name()),
        ("validity", Validity()),
        ("subject", Name()),
        ("subjectPublicKeyInfo", SubjectPublicKeyInfo()),
        ("issuerUniqueID", UniqueIdentifier(impl=tag_ctxp(1), optional=True)),
        ("subjectUniqueID", UniqueIdentifier(impl=tag_ctxp(2), optional=True)),
        ("extensions", Extensions(expl=tag_ctxc(3), optional=True)),
    )

class Certificate(Sequence):
    # Certificate  ::=  SEQUENCE  {
    #     tbsCertificate       TBSCertificate,
    #     signatureAlgorithm   AlgorithmIdentifier,
    #     signature            BIT STRING  }    
    schema = (
        ("tbsCertificate", TBSCertificate()),
        ("signatureAlgorithm", AlgorithmIdentifier()),
        ("signatureValue", BitString()),
    )
