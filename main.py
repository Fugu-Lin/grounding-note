from service.user_service import UserService
from utils.file_utils import FileUtils

if __name__ == '__main__':
    # 創建實例
    user_service = UserService()
    file_utils   = FileUtils
    # 取得使用者資料並印出
    user1 = user_service.get_user_by_id(1)
    print(user1)

    # 獲取使用者資料並保存到文件
    user2 = user_service.get_user_by_id(2)
    if user2:
        user2_str = f"user2: {user2}"
        file_utils.write_file("user2.txt", user2_str)