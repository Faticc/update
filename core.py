from pathlib import Path
from mcproto import UPDATE_STUB, proto
from tqdm import tqdm
import grpc


def get_java_file_tree(java_version: str, platform: int, session_id: str):
    request = proto.update_pb2.JavaFileTreeRequest( # pyright: ignore[reportAttributeAccessIssue]
        java_version=java_version,
        platform=platform
    )

    try:
        response = UPDATE_STUB.GetJavaFileTree(
            request,
            metadata=[("session", session_id)]
        )

        files = [
            {
                "path": f.path,
                "size": f.size,
                "hash": f.hash.hex(),
                "is_directory": f.is_directory
            }
            for f in response.files
        ]

        return files, response.base_url, response.node_id

    except grpc.RpcError as e:
        raise RuntimeError(f"gRPC error: {e.details()} ({e.code().name})")
    

def get_file_tree(client_id: int, session_id: str):
    request = proto.update_pb2.FileTreeRequest(client_id=client_id) # pyright: ignore[reportAttributeAccessIssue]

    try:
        response = UPDATE_STUB.GetFileTree(
            request,
            metadata=[("session", session_id)]
        )

        files = [
            {
                "path": f.path,
                "size": f.size,
                "hash": f.hash.hex(),
                "is_directory": f.is_directory
            }
            for f in response.files
        ]

        return files, response.base_url, response.node_id

    except grpc.RpcError as e:
        raise RuntimeError(f"gRPC error: {e.details()} ({e.code().name})")


def get_asset_file_tree(asset_dir: str, session_id: str):
    request = proto.update_pb2.AssetFileTreeRequest(asset_dir=asset_dir) # pyright: ignore[reportAttributeAccessIssue]

    try:
        response = UPDATE_STUB.GetAssetFileTree(
            request,
            metadata=[("session", session_id)]
        )

        files = [
            {
                "path": f.path,
                "size": f.size,
                "hash": f.hash.hex(),
                "is_directory": f.is_directory
            }
            for f in response.files
        ]

        return files, response.base_url, response.node_id

    except grpc.RpcError as e:
        raise RuntimeError(f"gRPC error: {e.details()} ({e.code().name})")


def download_full_client(client_id: int, output_dir: str, session_id: str):
    path_output_dir = Path(output_dir)
    files, base_url, node_id = get_file_tree(client_id, session_id)

    paths = [f["path"] for f in files if not f["is_directory"]]
    print(f"Клиент файлов: {len(paths)}")

    progress = tqdm(total=len(paths), desc="Client", unit="file")

    request = proto.update_pb2.DownloadRequest(client_id=client_id, paths=paths) # pyright: ignore[reportAttributeAccessIssue]

    try:
        chunks = UPDATE_STUB.DownloadFiles(request, metadata=[("session", session_id)])

        for chunk in chunks:
            file_path = path_output_dir / chunk.path
            file_path.parent.mkdir(parents=True, exist_ok=True)

            mode = "ab" if file_path.exists() else "wb"
            with open(file_path, mode) as f:
                f.write(chunk.data)

            if chunk.is_last:
                progress.update(1)
                progress.set_postfix({"file": chunk.path})

    except grpc.RpcError as e:
        raise RuntimeError(f"gRPC error: {e.details()} ({e.code().name})")

    progress.close()
    print("Клиент готов!")


def download_full_assets(asset_dir: str, output_dir: str, session_id: str):
    path_output_dir = Path(output_dir)
    files, base_url, node_id = get_asset_file_tree(asset_dir, session_id)

    paths = [f["path"] for f in files if not f["is_directory"]]
    print(f"Ассетов: {len(paths)}")

    progress = tqdm(total=len(paths), desc="Assets", unit="file")

    request = proto.update_pb2.AssetDownloadRequest(asset_dir=asset_dir, paths=paths) # pyright: ignore[reportAttributeAccessIssue]

    try:
        chunks = UPDATE_STUB.DownloadAssetFiles(request, metadata=[("session", session_id)])

        for chunk in chunks:
            file_path = path_output_dir / chunk.path
            file_path.parent.mkdir(parents=True, exist_ok=True)

            mode = "ab" if file_path.exists() else "wb"
            with open(file_path, mode) as f:
                f.write(chunk.data)

            if chunk.is_last:
                progress.update(1)
                progress.set_postfix({"file": chunk.path})

    except grpc.RpcError as e:
        raise RuntimeError(f"gRPC error: {e.details()} ({e.code().name})")

    progress.close()
    print("Ассеты готовы!")


def download_full_java(java_version: str, platform: int, output_dir: str, session_id: str):
    path_output_dir = Path(output_dir)
    files, base_url, node_id = get_java_file_tree(java_version, platform, session_id)

    paths = [f["path"] for f in files if not f["is_directory"]]
    print(f"Java файлов: {len(paths)}")

    progress = tqdm(total=len(paths), desc="Java", unit="file")

    request = proto.update_pb2.JavaDownloadRequest( # pyright: ignore[reportAttributeAccessIssue]
        java_version=java_version,
        platform=platform,
        paths=paths
    )

    try:
        chunks = UPDATE_STUB.DownloadJavaFiles(request, metadata=[("session", session_id)])

        for chunk in chunks:
            file_path = path_output_dir / chunk.path
            file_path.parent.mkdir(parents=True, exist_ok=True)

            mode = "ab" if file_path.exists() else "wb"
            with open(file_path, mode) as f:
                f.write(chunk.data)

            if chunk.is_last:
                progress.update(1)
                progress.set_postfix({"file": chunk.path})

    except grpc.RpcError as e:
        raise RuntimeError(f"gRPC error: {e.details()} ({e.code().name})")

    progress.close()
    print("Java готов!")
