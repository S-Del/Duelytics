from dataclasses import dataclass, field


@dataclass(frozen=True)
class ReferenceData:
    """
    参照テーブルから読み込んだマッピングデータを保持する不変のデータクラス。
    """
    # FirstOrSecond のマッピング
    # 例: {'F': 1, 'S': 2}
    first_or_second_code_to_id: dict[str, int] = field(default_factory=dict)
    # 例: {1: 'F', 2: 'S'}
    first_or_second_id_to_code: dict[int, str] = field(default_factory=dict)

    # ResultChar のマッピング
    # 例: {'W': 1, 'L': 2, 'D': 3}
    result_char_code_to_id: dict[str, int] = field(default_factory=dict)
    # 例: {1: 'W', 2: 'L', 3: 'D'}
    result_char_id_to_code: dict[int, str] = field(default_factory=dict)
