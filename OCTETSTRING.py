from pyderasn import (
    OctetString, _pp, tag_decode, DecodePathDefBy
)

class OCTETSTRING(OctetString):
    def pps(self, decode_path=()):
        defined_by, defined = self.defined or (None, None)
        yield _pp(
            obj=self,
            asn1_type_name=self.asn1_type_name,
            obj_name=self.__class__.__name__,
            decode_path=decode_path,
            value=("%d bytes" % len(self._value)) if self.ready else None,
            blob=self._value if (defined_by is None) and (self.ready) else None, # self._value if self.ready else None,
            optional=self.optional,
            default=self == self.default,
            impl=None if self.tag == self.tag_default else tag_decode(self.tag),
            expl=None if self._expl is None else tag_decode(self._expl),
            offset=self.offset,
            tlen=self.tlen,
            llen=self.llen,
            vlen=self.vlen,
            expl_offset=self.expl_offset if self.expled else None,
            expl_tlen=self.expl_tlen if self.expled else None,
            expl_llen=self.expl_llen if self.expled else None,
            expl_vlen=self.expl_vlen if self.expled else None,
            expl_lenindef=self.expl_lenindef,
            lenindef=self.lenindef,
            ber_encoded=self.ber_encoded,
            bered=self.bered,
        )
        if defined_by is not None:
            yield defined.pps(
                decode_path=decode_path + (DecodePathDefBy(defined_by),)
            )
        for pp in self.pps_lenindef(decode_path):
            yield pp
