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


SQL = f"""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS {FirstOrSecondTypesSchema.TABLE_NAME} (
    {FirstOrSecondTypesSchema.Columns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,
    {FirstOrSecondTypesSchema.Columns.CODE} TEXT UNIQUE NOT NULL CHECK (
        {FirstOrSecondTypesSchema.Columns.CODE} <> ''
    ),
    {FirstOrSecondTypesSchema.Columns.NAME} TEXT UNIQUE NOT NULL CHECK (
        {FirstOrSecondTypesSchema.Columns.NAME} <> ''
    ),
    {FirstOrSecondTypesSchema.Columns.NAME_JP} TEXT UNIQUE NOT NULL CHECK (
        {FirstOrSecondTypesSchema.Columns.NAME_JP} <> ''
    )
);
INSERT INTO {FirstOrSecondTypesSchema.TABLE_NAME} (
    {FirstOrSecondTypesSchema.Columns.CODE},
    {FirstOrSecondTypesSchema.Columns.NAME},
    {FirstOrSecondTypesSchema.Columns.NAME_JP}
) VALUES (
    'F', 'First', '先攻'
), (
    'S', 'Second', '後攻'
);

CREATE TABLE IF NOT EXISTS {ResultTypesSchema.TABLE_NAME} (
    {ResultTypesSchema.Columns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,
    {ResultTypesSchema.Columns.CODE} TEXT UNIQUE NOT NULL CHECK (
        {ResultTypesSchema.Columns.CODE} <> ''
    ),
    {ResultTypesSchema.Columns.NAME} TEXT UNIQUE NOT NULL CHECK (
        {ResultTypesSchema.Columns.NAME} <> ''
    ),
    {ResultTypesSchema.Columns.NAME_JP} TEXT UNIQUE NOT NULL CHECK (
        {ResultTypesSchema.Columns.NAME_JP} <> ''
    )
);
INSERT INTO {ResultTypesSchema.TABLE_NAME} (
    {ResultTypesSchema.Columns.CODE},
    {ResultTypesSchema.Columns.NAME},
    {ResultTypesSchema.Columns.NAME_JP}
) VALUES (
    'W', 'Win', '勝利'
), (
    'L', 'Loss', '敗北'
), (
    'D', 'Draw', '引分'
);

CREATE TABLE IF NOT EXISTS {ResultSchema.TABLE_NAME} (
    {ResultSchema.Columns.ID} TEXT PRIMARY KEY CHECK (
        length({ResultSchema.Columns.ID}) = 36
        AND {ResultSchema.Columns.ID}
        GLOB '????????-????-????-????-????????????'
    ),
    {ResultSchema.Columns.REGISTERED_AT} TEXT NOT NULL CHECK (
        strftime(
            '%Y-%m-%dT%H:%M:%S', {ResultSchema.Columns.REGISTERED_AT}
        ) = {ResultSchema.Columns.REGISTERED_AT}
    ),
    {ResultSchema.Columns.FIRST_OR_SECOND_TYPE_ID} INTEGER NOT NULL
    REFERENCES {FirstOrSecondTypesSchema.TABLE_NAME} (
        {FirstOrSecondTypesSchema.Columns.ID}
    ),
    {ResultSchema.Columns.RESULT_TYPE_ID} INTEGER NOT NULL
    REFERENCES {ResultTypesSchema.TABLE_NAME} (
        {ResultTypesSchema.Columns.ID}
    ),
    {ResultSchema.Columns.MY_DECK_NAME} TEXT NOT NULL CHECK (
        {ResultSchema.Columns.MY_DECK_NAME} <> ''
    ),
    {ResultSchema.Columns.OPPONENT_DECK_NAME} TEXT NOT NULL CHECK (
        {ResultSchema.Columns.OPPONENT_DECK_NAME} <> ''
    )
);

CREATE INDEX IF NOT EXISTS {ResultSchema.Indexes.REGISTERED_AT}
ON {ResultSchema.TABLE_NAME} ({ResultSchema.Columns.REGISTERED_AT} DESC);

CREATE TABLE IF NOT EXISTS {MemoSchema.TABLE_NAME} (
    {MemoSchema.Columns.RESULT_ID} TEXT PRIMARY KEY
    REFERENCES {ResultSchema.TABLE_NAME} (
        {ResultSchema.Columns.ID}
    ) ON DELETE CASCADE,
    {MemoSchema.Columns.CONTENT} TEXT NOT NULL CHECK (
        {MemoSchema.Columns.CONTENT} <> ''
    )
);
"""
