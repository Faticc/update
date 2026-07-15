import os
import glob
import requests
from tqdm import tqdm
from urllib.parse import unquote

def download_file(url: str, target_dir: str) -> bool:
    try:
        target_dir = os.path.abspath(target_dir)
        os.makedirs(target_dir, exist_ok=True)
        filename = unquote(url.split("/")[-1])
        filepath = os.path.join(target_dir, filename)
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print(f"Ошибка HTTP: {response.status_code}")
            return False

        total_size = int(response.headers.get("content-length", 0))

        progress = tqdm(
            total=total_size,
            unit="iB",
            unit_scale=True,
            desc=f"{filename}"
        )

        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    progress.update(len(chunk))

        progress.close()

        if total_size != 0 and progress.n != total_size:
            print("Ошибка: файл скачан не полностью")
            return False

        print(f"Файл успешно скачан: {filepath}")
        return True

    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def delete_file_mask(mask: str, target_dir: str) -> bool:
    try:
        target_dir = os.path.abspath(target_dir)
        full_mask = os.path.join(target_dir, mask)
        matched_files = glob.glob(full_mask)
        if not matched_files:
            print(f"Файлы по маске не найдены: {full_mask}")
            return False
        for file in matched_files:
            try:
                os.remove(file)
                print(f"Файл удалён: {file}")
            except Exception as e:
                print(f"Ошибка удаления {file}: {e}")
                return False
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False