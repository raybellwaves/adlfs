import pytest

from azure.storage.blob import BlobServiceClient, ContainerClient


URL = "127.0.0.1:10000"
ACCOUNT_NAME = "devstoreaccount1"
ACCOUNT_KEY = "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName={ACCOUNT_NAME};AccountKey={ACCOUNT_KEY};EndpointSuffix=core.windows.net"
data = b"0123456789"


def pytest_addoption(parser):
    parser.addoption(
        "--host",
        action="store",
        default="127.0.0.1:10000",
        help="Host running azurite.",
    )


@pytest.fixture(scope="function")
def host(request):
    print("host:", request.config.getoption("--host"))
    return request.config.getoption("--host")


@pytest.fixture(scope="function")
def storage(host):
    """
    Create blob using azurite.
    """
    account_url = f"https://{ACCOUNT_NAME}.blob.core.windows.net"
    container_name = "data"
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_service_client.create_container(container_name, timeout=1)

    container_client = ContainerClient(account_url=account_url,
                                       container_name=container_name,
                                       credential=ACCOUNT_KEY)

    container_client.upload_blob("top_file.txt", data)
    container_client.upload_blob("data", "root/rfile.txt", data)
    container_client.upload_blob("data", "root/a/file.txt", data)
    container_client.upload_blob("data", "root/b/file.txt", data)
    container_client.upload_blob("data", "root/c/file1.txt", data)
    container_client.upload_blob("data", "root/c/file2.txt", data)
    yield container_client
