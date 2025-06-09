class FirstOrSecondTypesSchema:
    TABLE_NAME = "first_or_second_types"
    class Columns:
        ID = "id"
        CODE = "code"
        NAME = "name"
        NAME_JP = "name_jp"


class ResultTypesSchema:
    TABLE_NAME = "result_types"
    class Columns:
        ID = "id"
        CODE = "code"
        NAME = "name"
        NAME_JP = "name_jp"


class ResultSchema:
    TABLE_NAME = "results"

    class Columns:
        ID = "id"
        REGISTERED_AT = "registered_at"
        FIRST_OR_SECOND_TYPE_ID = "first_or_second_type_id"
        RESULT_TYPE_ID = "result_type_id"
        MY_DECK_NAME = "my_deck_name"
        OPPONENT_DECK_NAME = "opponent_deck_name"

    class Indexes:
        REGISTERED_AT = "registered_at_idx"


class MemoSchema:
    TABLE_NAME = "memos"

    class Columns:
        RESULT_ID = "result_id"
        CONTENT = "content"
