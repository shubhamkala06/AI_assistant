from app.core.exceptions.exceptions import ResourceNotFoundError
from app.core.exceptions.http_exception_mapper import get_http_status


class DummyNotFound(ResourceNotFoundError):
    ERROR_CODE = "DUMMY_NOT_FOUND"


def test_resource_not_found_subclass_maps_to_404():
    exc = DummyNotFound(
        public_message="Dummy resource was not found",
    )

    assert get_http_status(exc) == 404
