#Service 層包含應用程序的業務邏輯。
class UserService:
    def __init__(self):
        self.user = {
            1: "Jocelyn",
            2: "winnie",
        }

    def get_user_by_id(self, user_id = 1):
        if user_id in self.user:
            return self.user[user_id]
        return 'Not found'