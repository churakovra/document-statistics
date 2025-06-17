from passlib.context import CryptContext

from app.utils.binary_node import BinaryNode

pass_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)


class SecurityService:
    @staticmethod
    def validate_pass(pwd: str, pwd_hashed: str) -> bool:
        return pass_context.verify(pwd, pwd_hashed)

    @staticmethod
    def hash_pass(pwd: str) -> str:
        return pass_context.hash(pwd)

    @staticmethod
    def generate_code(node: BinaryNode, curr_code="", codes=None):
        print(f"generate_code node type {type(node)}")

        if node is None:
            return

        if codes is None:
            codes = {}

        if node.left is None and node.right is None:
            codes[node.value] = curr_code
            return

        print(f"generate code node.left {type(node.left)}")
        SecurityService.generate_code(node.left, curr_code + "0", codes)
        print(f"generate code node.right {type(node.right)}")
        SecurityService.generate_code(node.right, curr_code + "1", codes)

        return codes
