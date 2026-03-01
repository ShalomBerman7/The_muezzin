from pathlib import Path
from tinytag import TinyTag
from datetime import datetime

PATH = r'C:\github\The_muezzin\podcasts'


class GetMetadata:
    def __init__(self, path):
        self.path = Path(path)

    def get_metadata(self):
        if not self.path.exists():
            print(f"Error: The file '{self.path}' does not exist.")
            return []

        result = []
        for file in self.path.glob('*.wav'):
            data = {}
            try:
                tag = TinyTag.get(file)

                stats = file.stat()
                creation_time = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')

                data['file_name'] = file.name
                data['file_size_bytes'] = tag.filesize
                data['created_at'] = creation_time

                result.append(data)

            except Exception as e:
                print(f'error reading metadata {e}')

        return result


c = GetMetadata(PATH)
print(c.get_metadata())
