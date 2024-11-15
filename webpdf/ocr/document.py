import subprocess
import json
from datetime import datetime
from pathlib import Path
from uuid import UUID
from django.conf import settings

class Document:
    def __init__(self, pid: UUID, lang: set, status: str, input: Path, output: Path, 
                 output_json: Path, output_txt: Path, created: datetime, expire: datetime):
        self.pid = pid
        self.lang = lang
        self.status = status
        self.input = input
        self.output = output
        self.output_json = output_json
        self.output_txt = output_txt
        self.created = created
        self.expire = expire
        self.finished = None
        self.result = None
        self.code = None

    def ocr(self, output_format="pdf"):
        # Cập nhật trạng thái thành 'processing'
        self.status = "processing"
        self.save_state()
        
        # Thiết lập lệnh OCR dựa trên định dạng đầu ra
        command = [
            settings.OCR_COMMAND,
            "-l", '+'.join(self.lang),
            "--sidecar", str(self.output_txt),
            str(self.input),
            str(self.output),
        ]
        if output_format == "word":
            command.append("--output-format word")

        try:
            output = subprocess.check_output(" ".join(command), stderr=subprocess.STDOUT, shell=True)
            self.status = "done"
            self.result = output.decode('utf-8', errors="ignore").strip()  # Bỏ qua lỗi UTF-8
            self.code = 0
        except subprocess.CalledProcessError as e:
            self.status = "error"
            self.code = e.returncode
            self.result = e.output.decode('utf-8', errors="ignore").strip()  # Bỏ qua lỗi UTF-8 khi giải mã
        finally:
            self.finished = datetime.now()
            self.save_state()


    def save_state(self):
        # Chuyển các thuộc tính thành dictionary để lưu JSON
        document_data = {
            "pid": str(self.pid),
            "lang": list(self.lang),
            "status": self.status,
            "input": str(self.input),
            "output": str(self.output),
            "output_json": str(self.output_json),
            "output_txt": str(self.output_txt),
            "result": self.result,
            "code": self.code,
            "created": self.created.isoformat(),
            "expire": self.expire.isoformat(),
            "finished": self.finished.isoformat() if self.finished else None
        }

        # Lưu dữ liệu vào file JSON
        with open(self.output_json, "w") as ff:
            json.dump(document_data, ff, indent=4)  # Ghi dữ liệu dưới dạng JSON
