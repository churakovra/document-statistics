import asyncio

import pytest
from starlette.status import HTTP_200_OK

from tests.integration.test_upload_file_works_correct import test_upload_file_words_correct


@pytest.mark.asyncio
async def test_get_file_works_correct(client):
    response = await client.get("/file?file_id=24")

    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 50
