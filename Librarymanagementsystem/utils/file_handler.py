import json
import os

class FileHandler:
    @staticmethod
    def read_json(file_path):
        """
        Đọc file JSON và trả về dữ liệu (List/Dict).
        Nếu file không tồn tại hoặc lỗi, trả về danh sách rỗng [].
        """
        if not os.path.exists(file_path):
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:  # File có tồn tại nhưng rỗng
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, IOError) as e:
            print(f"[Error] Lỗi đọc file {file_path}: {e}")
            return []

    @staticmethod
    def write_json(file_path, data):
        """
        Ghi dữ liệu xuống file JSON.
        Tự động tạo thư mục nếu chưa có.
        """
        try:
            # Tạo thư mục chứa file nếu chưa tồn tại (VD: data/)
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"[Error] Lỗi ghi file {file_path}: {e}")
            return False