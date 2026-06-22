import uuid
import os
from fastapi import APIRouter, Security, UploadFile, File
from src.core.config import settings
from src.storage import get_storage_backend
from src.core.dependencies import require_admin
from src.core.errors import bad_request, ErrorCode

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".mp4", ".webm"}
ALLOWED_FOLDERS = {"exercises", "instructions"}
MAX_SIZE = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

router = APIRouter(prefix="/media", tags=["Media Upload"])


def _validate_file(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise bad_request(
            f"File type '{ext}' not allowed. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )
    return f"{uuid.uuid4()}{ext}"


@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    folder: str = "exercises",
    _: dict = Security(require_admin),
):
    if folder not in ALLOWED_FOLDERS:
        raise bad_request(
            f"Folder must be one of: {', '.join(sorted(ALLOWED_FOLDERS))}"
        )

    if not file.filename:
        raise bad_request("Filename is required")

    stored_name = _validate_file(file.filename)
    data = await file.read()

    if len(data) > MAX_SIZE:
        from src.core.errors import error_response, ErrorCode
        from fastapi import HTTPException, status
        content = error_response(413, f"File too large. Max size: {settings.MAX_UPLOAD_SIZE_MB}MB", ErrorCode.FILE_TOO_LARGE)
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=content)

    path = f"{folder}/{stored_name}"
    backend = get_storage_backend()
    url = await backend.upload(path, data, file.content_type or "application/octet-stream")

    return {"url": url, "path": path, "filename": stored_name}


@router.delete("/{folder}/{filename}")
async def delete_media(
    folder: str,
    filename: str,
    _: dict = Security(require_admin),
):
    if folder not in ALLOWED_FOLDERS:
        raise bad_request(f"Invalid folder: {folder}")

    path = f"{folder}/{filename}"
    backend = get_storage_backend()
    await backend.delete(path)

    return {"deleted": True}
