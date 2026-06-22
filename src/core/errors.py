from fastapi import HTTPException, status


class ErrorCode:
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    BAD_REQUEST = "BAD_REQUEST"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    INTERNAL_ERROR = "INTERNAL_ERROR"


def error_response(
    status_code: int,
    message: str,
    error_code: str = "INTERNAL_ERROR",
) -> dict:
    return {
        "error": {
            "code": error_code,
            "message": message,
        }
    }


def not_found(detail: str = "Resource not found") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=error_response(404, detail, ErrorCode.NOT_FOUND),
    )


def conflict(detail: str = "Resource already exists") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=error_response(409, detail, ErrorCode.CONFLICT),
    )


def unauthorized(detail: str = "Not authenticated") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=error_response(401, detail, ErrorCode.UNAUTHORIZED),
    )


def forbidden(detail: str = "Insufficient permissions") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=error_response(403, detail, ErrorCode.FORBIDDEN),
    )


def bad_request(detail: str = "Bad request") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=error_response(400, detail, ErrorCode.BAD_REQUEST),
    )
