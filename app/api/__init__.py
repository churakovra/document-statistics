from .add_collection import router as add_collection_router
from .add_collection_document import router as add_collection_document_router
from .change_password import router as change_password_router
from .collections import router as collections_router
from .delete_document import router as delete_document_router
from .delete_document_collection import router as delete_document_collection_router
from .delete_user import router as delete_user_router
from .documents import router as documents_router
from .get_collection_documents import router as get_collection_router
from .get_collection_statistics import router as get_collection_statistics_router
from .get_document_content import router as get_document_content_router
from .get_document_content_huffman import router as get_document_content_huffman_router
from .get_document_statistics import router as get_document_statistics_router
from .login import router as login_router
from .logout import router as logout_router
from .metrics import router as metrics_router
from .register import router as register_router
from .root import router as root_router
from .status import router as status_router
from .upload_document import router as upload_document_router
from .version import router as version_router

api_routers = [
    add_collection_router,
    add_collection_document_router,
    change_password_router,
    collections_router,
    delete_document_router,
    delete_document_collection_router,
    delete_user_router,
    documents_router,
    get_collection_router,
    get_collection_statistics_router,
    get_document_content_router,
    get_document_content_huffman_router,
    get_document_statistics_router,
    login_router,
    logout_router,
    metrics_router,
    register_router,
    root_router,
    status_router,
    upload_document_router,
    version_router,
]
