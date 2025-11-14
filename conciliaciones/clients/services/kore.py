# pylint: disable=unused-argument
# reason: The following class defines API endpoints without method bodies,
# as they are dynamically handled by decorators. Thus, method arguments
# are intentionally unused.
from typing import Annotated, Any

import httpx
from k_link.tools import env
from k_link.utils.service.core.decorators import post
from k_link.utils.service.core.resource import BaseApiResource
from k_link.utils.service.params import (
    Authorization,
    FormBodyParam,
    HeaderParam,
    JsonBodyParam,
    QueryParam,
)

from conciliaciones.models.services.kore_models import KoreResponse


class KoreService(BaseApiResource):
    _base_url: str = env.KORE_URL
    _path: str = "/"

    @post(
        path="/metadata/filter/",
        response_model=KoreResponse,
    )
    async def get_comprobantes(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization()],
        skip: Annotated[int, QueryParam] = 0,
        limit: Annotated[int, QueryParam] = 0,
        filters: Annotated[dict[str, Any], JsonBodyParam],
    ) -> KoreResponse: ...

    @post(
        path="/metadata/filter/aggregate/",
        response_model=dict,
    )
    async def aggregate(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization()],
        skip: Annotated[int, QueryParam] = 0,
        limit: Annotated[int, QueryParam] = 1000000,
        filters: Annotated[list[dict[str, Any]], JsonBodyParam],
    ) -> dict: ...

    @post(
        path="/comprobante/uploadComprobanteZip/",
    )
    async def process_cfdis_zip(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization()],
        path: Annotated[str, FormBodyParam],
    ) -> httpx.Response: ...
