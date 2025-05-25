from . import ApplicationError


class ApplicationOperationWarning(ApplicationError):
    """アプリ続行は可能だが、 どのようなエラーが発生しているかを
    ユーザーに通知することを期待するエラークラス。

    Attributes:
        msg (str): エラーを簡潔に表す文字列
        details (str | None): エラー詳細や対応方法を表す説明文
    """

    def __init__(self, msg: str, details: str | None = None):
        super().__init__(msg)
        self.msg = msg
        self.details = details
