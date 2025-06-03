from .add_file import router as add_file_router
from .get_file_info import router as get_file_info_router
from .metrics import router as metrics_router
from .root import router as root_router
from .status import router as status_router
from .version import router as version_router

api_routers = [
    add_file_router,
    get_file_info_router,
    metrics_router,
    root_router,
    status_router,
    version_router
]