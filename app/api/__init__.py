from .documents import router as documents_router
from .login import router as login_router
from .logout import router as logout_router
from .metrics import router as metrics_router
from .register import router as register_router
from .root import router as root_router
from .status import router as status_router
from .version import router as version_router

api_routers = [
    documents_router,
    login_router,
    logout_router,
    metrics_router,
    register_router,
    root_router,
    status_router,
    version_router,
]
