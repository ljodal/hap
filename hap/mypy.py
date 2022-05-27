"""
A mypy plugin work around https://github.com/python/mypy/issues/12886
"""

from functools import partial
from typing import Callable

from mypy.nodes import GDEF, Block, ClassDef, SymbolTable, SymbolTableNode, TypeInfo
from mypy.plugin import DynamicClassDefContext, Plugin
from mypy.types import Instance
from mypy.typevars import fill_typevars


class BugFixPlugin(Plugin):
    def get_dynamic_class_hook(
        self, fullname: str
    ) -> Callable[[DynamicClassDefContext], None] | None:
        if fullname == "hap.tlv.tlv_int":
            return partial(define_tlv_class, generic_type="builtins.int")
        if fullname == "hap.tlv.tlv_bytes":
            return partial(define_tlv_class, generic_type="builtins.bytes")
        if fullname == "hap.tlv.tlv_str":
            return partial(define_tlv_class, generic_type="builtins.str")
        return None


def define_tlv_class(ctx: DynamicClassDefContext, *, generic_type: str) -> None:

    # The returned class should inherit from hap.tlv.TLV, so get that
    tlv_node = ctx.api.lookup_fully_qualified_or_none("hap.tlv.TLV")
    assert tlv_node
    tlv_info = tlv_node.node

    # 1) Look up the generic type (int, bytes, str)
    # 2) Get an instance with typevars from the TLV type info
    # 3) Set tye typevars on the instance to the generic type
    generic = ctx.api.named_type(generic_type)
    assert generic
    tlv_base = fill_typevars(tlv_info)  # type: ignore
    assert isinstance(tlv_base, Instance)
    tlv_base.args = (generic,)

    class_def = ClassDef(ctx.name, Block([]))
    class_def.fullname = ctx.api.qualified_name(ctx.name)

    info = TypeInfo(SymbolTable(), class_def, ctx.api.cur_mod_id)
    info.mro = [info, tlv_info, ctx.api.named_type("builtins.object").type]  # type: ignore
    info.bases = [tlv_base]

    class_def.info = info

    ctx.api.add_symbol_table_node(ctx.name, SymbolTableNode(GDEF, info))


def plugin(version: str) -> type[BugFixPlugin] | None:
    if version == "0.960":
        return BugFixPlugin
    return None
