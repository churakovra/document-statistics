import os
import pytest

from tests.conftest import client


@pytest.mark.asyncio
async def test_upload_file_words_correct(client) -> int:
    file_content = "Hello  world! This is? TeSt senTence"
    file_name = "test-file1.txt"

    with open(file_name, "w") as f:
        f.write(file_content)

    with open(file_name, "rb") as f:
        response = await client.post(
            "/file/new",
            files={"file": (file_name, f, "text/plain")}
        )

    os.remove(file_name)

    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert data["file_name"] == file_name

    return data["file_id"]