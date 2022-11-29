class Message:
    def __init__(self):
        self.tags = "alert alert-primary"
        self.text = "サンプルの通知"

    def __init__(self, tag, text):
        self.tags = tag
        self.text = text