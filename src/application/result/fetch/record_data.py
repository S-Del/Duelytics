from dataclasses import dataclass


@dataclass(frozen=True)
class RecordData:
    game_count_str: str
    win_count_str: str
    loss_count_str: str
    draw_count_str: str

    first_count_str: str
    first_rate_percentage_str: str
    second_count_str: str
    second_rate_percentage_str: str

    win_rate_percentage_str: str
    first_win_rate_percentage_str: str
    second_win_rate_percentage_str: str
