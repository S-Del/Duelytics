# ドメイン層にイベントを設ける場合は以下の様になる。
# class ApplicationEvent(BaseEvent):
# 現状はドメインイベントの定義が不要のため、このクラスをベースとしている。
class ApplicationEvent:
    """ベースとなるイベントオブジェクト"""
    pass
