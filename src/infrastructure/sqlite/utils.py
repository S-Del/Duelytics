from typing import Literal


def escape_like_param(
    search_type: Literal["exact", "partial", "prefix", "suffix"],
    value: str
) -> str:
    """LIKE 検索時のパラメータ文字列を返す"""
    escaped = (value.replace("\\", "\\\\")
                    .replace("%", "\\%")
                    .replace("_", "\\_"))
    if search_type == "exact":
        return escaped
    if search_type == "partial":
        return f"%{escaped}%"
    if search_type == "prefix":
        return f"{escaped}%"
    if search_type == "suffix":
        return f"%{escaped}"

    raise ValueError(f"検索条件の指定が不正: {search_type}")
