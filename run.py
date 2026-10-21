from pathlib import Path
import uvicorn
from app.config import settings

if __name__ == "__main__":
    ssl_certfile = None
    ssl_keyfile = None
    port = settings.app_port

    if settings.https_enabled:
        if not settings.ssl_certfile:
            raise RuntimeError("SSL_CERTFILE is not configured")
        if not settings.ssl_keyfile:
            raise RuntimeError("SSL_KEYFILE is not configured")

        cert_path = Path(settings.ssl_certfile)
        key_path = Path(settings.ssl_keyfile)

        if not cert_path.exists():
            raise RuntimeError(f"Certificate not found: {cert_path}")
        if not key_path.exists():
            raise RuntimeError(f"Private key not found: {key_path}")

        ssl_certfile = str(cert_path)
        ssl_keyfile = str(key_path)
        port = settings.https_port

    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=port,
        reload=settings.debug,
        ssl_certfile=ssl_certfile,
        ssl_keyfile=ssl_keyfile
    )
