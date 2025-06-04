class ResultSchema:
    TABLE_NAME = "results"

    class Columns:
        ID = "id"
        REGISTERED_AT = "registered_at"
        FIRST_OR_SECOND = "first_or_second"
        RESULT = "result"
        MY_DECK_NAME = "my_deck_name"
        OPPONENT_DECK_NAME = "opponent_deck_name"

    class Indexes:
        REGISTERED_AT = "registered_at_idx"


class MemoSchema:
    TABLE_NAME = "memos"

    class Columns:
        RESULT_ID = "result_id"
        CONTENT = "content"
