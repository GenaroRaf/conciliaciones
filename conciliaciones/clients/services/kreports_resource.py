# pylint: disable=unused-argument
# reason: The following class defines API endpoints without method bodies,
# as they are dynamically handled by decorators. Thus, method arguments
# are intentionally unused.

from typing import Annotated

from k_link.tools import env
from k_link.utils.service.core.decorators import delete, get, post, put
from k_link.utils.service.core.resource import BaseApiResource
from k_link.utils.service.params import (
    Authorization,
    AuthScheme,
    HeaderParam,
    JsonBodyParam,
    PathParam,
    QueryParam,
)

from conciliaciones.models.services.kreports_models import KReportsResponse
from conciliaciones.models.services.models import (
    BaseBodyExcelHeaderComprobanteRelacionadosSabana,
    BaseBodyHeaderComprobanteRelacionadosSabana,
    BaseBodyHeaderComprobanteRelacionadosTidy,
    BodyDownloadReport,
    BodyDownloadReportByPath,
    BodyReports,
    CartaPorte_cartaPorteZipperRequest,
    CartaPorte_createCartaPorteReportExcelRequest,
    CartaPorte_filterRequest,
    ComercioExterior_createComercioExteriorReportExcelRequest,
    ComercioExterior_filterRequest,
    Custom_createCustomExcelReportRequest,
    Custom_createCustomJsonRequest,
    Custom_createCustomStyleExcelReportRequest,
    Custom_createSyncCustomExcelReportRequest,
    Custom_createSyncCustomStyleExcelReportRequest,
    Directory_createDirectoryRequest,
    Directory_lastDirectoryRequest,
    General_createGeneralReportExcelRequest,
    General_filterRequest,
    Nomina_createReportNominaConceptosExcelRequest,
    Nomina_createReportNominaDetallesGeneralesExcelRequest,
    Nomina_createReportNominaSabanaExcelRequest,
    Nomina_createReportNominaSabanaRfcExcelRequest,
    Nomina_createReportNominaTidyExcelRequest,
    Nomina_getReportNominaConceptosJSONRequest,
    Nomina_getReportNominaDetallesGeneralesJSONRequest,
    Nomina_getReportNominaJSONRequest,
    Nomina_getReportNominaTidyJSONRequest,
    Pagos_cdpImpuestosRequest,
    Pagos_createPagosReportExcelRequest,
    Pagos_getPagosReportJsonRequest,
    Pagos_reportCdpPpdExcelRequest,
    Pagos_reportCdpPpdJsonRequest,
    Pagos_reportPpdGeneralExcelRequest,
    Pagos_reportPpdGeneralJsonRequest,
    QueueSchema,
    Relacionados_createPueCdpResumenGrafosReportJSONRequest,
    Relacionados_createPueCdpResumenReportExcelRequest,
    Relacionados_createPueCdpResumenReportJSONRequest,
    Relacionados_createPueCdpSabanaReportExcelRequest,
    Relacionados_createPueCdpSabanaReportJSONRequest,
    Relacionados_createPueCdpTidyReportExcelRequest,
    Relacionados_createPueCdpTidyReportJSONRequest,
    Relacionados_createPuePpdGeneralCdpSabanaReportExcelRequest,
    Relacionados_createPuePpdGeneralCdpSabanaReportJSONRequest,
    Relacionados_createPuePpdGeneralSabanaMomenReportExcelRequest,
    Relacionados_createPuePpdGeneralSabanaMomenReportJSONRequest,
    Relacionados_createPuePpdGeneralSabanaPagosGrafosExcelRequest,
    Relacionados_createPuePpdGeneralSabanaPagosGrafosReportJSONRequest,
    Relacionados_createPuePpdGeneralSabanaPagosReportExcelRequest,
    Relacionados_createPuePpdGeneralSabanaPagosReportJSONRequest,
    Relacionados_createPuePpdGeneralSabanaReportExcelRequest,
    Relacionados_createPuePpdGeneralSabanaReportJSONRequest,
    Relacionados_createPuePpdGeneralSabanaTrasladoReportExcelRequest,
    Relacionados_createPuePpdGeneralSabanaTrasladoReportJSONRequest,
    Relacionados_createPuePpdGeneralTidyReportExcelRequest,
    Relacionados_createPuePpdGeneralTidyReportJSONRequest,
    Relacionados_createPuePpdGeneralTidyTrasladoReportExcelRequest,
    Relacionados_createPuePpdGeneralTidyTrasladoReportJSONRequest,
    Relacionados_createPuePpdResumenReportExcelRequest,
    Relacionados_createRelacionadosPuePpdGrafosTidyReportJSONRequest,
    Relacionados_createRelacionadosPuePpdSabanaReportExcelRequest,
    Relacionados_createRelacionadosResumenReportJSONRequest,
    Relacionados_createRelacionadosTidyReportExcelRequest,
    Relacionados_registerNewReportHeadersOrderRequest,
    Relacionados_registerUpdateReportHeadersOrderRequest,
    Reports_blockReportRequest,
    Reprocess_reprocess_reportRequest,
)


class KreportsResource(BaseApiResource):
    _base_url = env.KREPORTS_URL
    _path = "/"

    @post(
        path="/cartaporte/get_report/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def carta_porte__create_carta_porte_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            CartaPorte_createCartaPorteReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/cartaporte/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def carta_porte__filter(
        self,
        *,
        skip: Annotated[str, QueryParam],
        limit: Annotated[str, QueryParam],
        sortKey: Annotated[str, QueryParam],
        sortDirection: Annotated[str, QueryParam],
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[CartaPorte_filterRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/cartaporte/representacion_impresa/{uuid}",
        response_model=KReportsResponse[list[dict], None],
    )
    async def carta_porte__get_representacion_impresa(
        self,
        *,
        uuid: Annotated[str, PathParam],
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/cartaporte/zipper/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def carta_porte__carta_porte_zipper(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[CartaPorte_cartaPorteZipperRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/comercioexterior/get_report/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def comercio_exterior__create_comercio_exterior_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            ComercioExterior_createComercioExteriorReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/comercioexterior/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def comercio_exterior__filter(
        self,
        *,
        skip: Annotated[str, QueryParam],
        limit: Annotated[str, QueryParam],
        sortKey: Annotated[str, QueryParam],
        sortDirection: Annotated[str, QueryParam],
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[ComercioExterior_filterRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/custom/excel",
        response_model=KReportsResponse[list[dict], None],
    )
    async def custom__create_custom_excel_report(
        self,
        *,
        orderBy: Annotated[str, QueryParam],
        direction: Annotated[int, QueryParam],
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Custom_createCustomExcelReportRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/custom/excel/style",
        response_model=KReportsResponse[list[dict], None],
    )
    async def custom__create_custom_style_excel_report(
        self,
        *,
        orderBy: Annotated[str, QueryParam],
        direction: Annotated[int, QueryParam],
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Custom_createCustomStyleExcelReportRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/custom/json",
        response_model=KReportsResponse[list[dict], None],
    )
    async def custom__create_custom_json(
        self,
        *,
        orderBy: Annotated[str, QueryParam],
        direction: Annotated[int, QueryParam],
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Custom_createCustomJsonRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/custom/syncExcel",
        response_model=KReportsResponse[list[dict], None],
    )
    async def custom__create_sync_custom_excel_report(
        self,
        *,
        orderBy: Annotated[str, QueryParam],
        direction: Annotated[int, QueryParam],
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Custom_createSyncCustomExcelReportRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/custom/syncExcel/style",
        response_model=KReportsResponse[list[dict], None],
    )
    async def custom__create_sync_custom_style_excel_report(
        self,
        *,
        orderBy: Annotated[str, QueryParam],
        direction: Annotated[int, QueryParam],
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Custom_createSyncCustomStyleExcelReportRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/directory/get_cdp_report/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def directory__last_directory(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Directory_lastDirectoryRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/directory/get_report/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def directory__create_directory(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Directory_createDirectoryRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/downloaderReport/{reportId}",
        response_model=KReportsResponse[list[dict], None],
    )
    async def template__download_report(
        self,
        reportId: Annotated[str, PathParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/general/excel",
        response_model=KReportsResponse[list[dict], None],
    )
    async def general__create_general_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[General_createGeneralReportExcelRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/generalPrefix/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def general__filter(
        self,
        *,
        skip: Annotated[str, QueryParam],
        limit: Annotated[str, QueryParam],
        sortKey: Annotated[str, QueryParam],
        sortDirection: Annotated[str, QueryParam],
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[General_filterRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/healthCheck",
        response_model=KReportsResponse[list[dict], None],
    )
    async def health_check__default(
        self,
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/logs/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def logger__get_logs(
        self,
        limit: Annotated[str, QueryParam],
        skip: Annotated[str, QueryParam],
        direction: Annotated[str, QueryParam],
        sheets: Annotated[str, QueryParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/nomina/conceptos/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def nomina__create_report_nomina_conceptos_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Nomina_createReportNominaConceptosExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/nomina/conceptos/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def nomina__get_report_nomina_conceptos_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Nomina_getReportNominaConceptosJSONRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/nomina/detalle_general/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def nomina__create_report_nomina_detalles_generales_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Nomina_createReportNominaDetallesGeneralesExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/nomina/detalle_general/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def nomina__get_report_nomina_detalles_generales_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Nomina_getReportNominaDetallesGeneralesJSONRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/nomina/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def nomina__create_report_nomina_sabana_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Nomina_createReportNominaSabanaExcelRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/nomina/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def nomina__get_report_nomina_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Nomina_getReportNominaJSONRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/nomina/rfc/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def nomina__create_report_nomina_sabana_rfc_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Nomina_createReportNominaSabanaRfcExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/nomina/tidy/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def nomina__create_report_nomina_tidy_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Nomina_createReportNominaTidyExcelRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/nomina/tidy/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def nomina__get_report_nomina_tidy_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Nomina_getReportNominaTidyJSONRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/pagos/cdp_impuestos/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def pagos__cdp_impuestos(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Pagos_cdpImpuestosRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/pagos/cdp_ppd/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def pagos__report_cdp_ppd_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Pagos_reportCdpPpdExcelRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/pagos/cdp_ppd/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def pagos__report_cdp_ppd_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Pagos_reportCdpPpdJsonRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/pagos/excel",
        response_model=KReportsResponse[list[dict], None],
    )
    async def pagos__create_pagos_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Pagos_createPagosReportExcelRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/pagos/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def pagos__get_pagos_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Pagos_getPagosReportJsonRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/pagos/ppd/excel",
        response_model=KReportsResponse[list[dict], None],
    )
    async def pagos__report_ppd_general_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Pagos_reportPpdGeneralExcelRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/pagos/ppd/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def pagos__report_ppd_general_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Pagos_reportPpdGeneralJsonRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/queue/get/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def queue__get_queue(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @put(
        path="/queue/update/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def queue__set_queue(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[QueueSchema, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/multi/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_relacionados_pue_ppd_multi_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            BaseBodyExcelHeaderComprobanteRelacionadosSabana, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_cdp/resumen/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_cdp_resumen_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPueCdpResumenReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_cdp/resumen/grafos/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_cdp_resumen_grafos_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPueCdpResumenGrafosReportJSONRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/relacionados/pue_cdp/resumen/headers/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_cdp_resumen_report_headers(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_cdp/resumen/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_cdp_resumen_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPueCdpResumenReportJSONRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_cdp/sabana/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_cdp_sabana_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPueCdpSabanaReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/relacionados/pue_cdp/sabana/headers/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_cdp_sabana_report_headers(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_cdp/sabana/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_cdp_sabana_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPueCdpSabanaReportJSONRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_cdp/tidy/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_cdp_tidy_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPueCdpTidyReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/relacionados/pue_cdp/tidy/headers/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_cdp_tidy_report_headers(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_cdp/tidy/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_cdp_tidy_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPueCdpTidyReportJSONRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/cdp/sabana/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_cdp_sabana_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        Authorization: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralCdpSabanaReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/relacionados/pue_ppd/general/cdp/sabana/headers/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_cdp_sabana_report_headers(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/cdp/sabana/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_cdp_sabana_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        Authorization: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralCdpSabanaReportJSONRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/sabana/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_sabana_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralSabanaReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/relacionados/pue_ppd/general/sabana/headers/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_sabana_report_headers(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/sabana/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_sabana_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralSabanaReportJSONRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/sabana/momentos/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_sabana_momen_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralSabanaMomenReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/relacionados/pue_ppd/general/sabana/momentos/headers/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_sabana_momentos_report_headers(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/sabana/momentos/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_sabana_momen_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralSabanaMomenReportJSONRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/sabana/pagos/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_sabana_pagos_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralSabanaPagosReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/sabana/pagos/grafos/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_sabana_pagos_grafos_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralSabanaPagosGrafosExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/sabana/pagos/grafos/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_sabana_pagos_grafos_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralSabanaPagosGrafosReportJSONRequest,
            JsonBodyParam,
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/sabana/pagos/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_sabana_pagos_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralSabanaPagosReportJSONRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/sabana/traslados/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_sabana_traslado_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralSabanaTrasladoReportExcelRequest,
            JsonBodyParam,
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/sabana/traslados/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_sabana_traslado_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralSabanaTrasladoReportJSONRequest,
            JsonBodyParam,
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/tidy/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_tidy_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralTidyReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/relacionados/pue_ppd/general/tidy/headers/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_tidy_report_headers(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/tidy/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_tidy_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralTidyReportJSONRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/tidy/traslados/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_tidy_traslado_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralTidyTrasladoReportExcelRequest,
            JsonBodyParam,
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/general/tidy/traslados/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_general_tidy_traslado_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdGeneralTidyTrasladoReportJSONRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/pue_ppd/resumen/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_pue_ppd_resumen_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createPuePpdResumenReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/relacionados/report_orders/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__find_all_report_headers_order(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @delete(
        path="/relacionados/report_orders/delete/{id}",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__register_delete_report_headers_order(
        self,
        id: Annotated[str, PathParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/report_orders/new_report/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__register_new_report_headers_order(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_registerNewReportHeadersOrderRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @put(
        path="/relacionados/report_orders/update/{id}",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__register_update_report_headers_order(
        self,
        id: Annotated[str, PathParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_registerUpdateReportHeadersOrderRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/relacionados/report_orders/{id}",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__find_by_id_report_headers_order(
        self,
        id: Annotated[str, PathParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/relacionados/resumen/headers/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__get_relacionados_resumen_report_headers(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/resumen/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_relacionados_resumen_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createRelacionadosResumenReportJSONRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/sabana/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_relacionados_pue_ppd_sabana_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createRelacionadosPuePpdSabanaReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/relacionados/sabana/headers/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__get_relacionados_pue_ppd_sabana_report_headers(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/sabana/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_relacionados_pue_ppd_sabana_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[BaseBodyHeaderComprobanteRelacionadosSabana, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/tidy/excel/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_relacionados_tidy_report_excel(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createRelacionadosTidyReportExcelRequest, JsonBodyParam
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/tidy/grafos/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_relacionados_pue_ppd_grafos_tidy_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[
            Relacionados_createRelacionadosPuePpdGrafosTidyReportJSONRequest,
            JsonBodyParam,
        ],
    ) -> KReportsResponse[list[dict], None]: ...
    @get(
        path="/relacionados/tidy/headers/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__get_relacionados_tidy_report_headers(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/relacionados/tidy/json/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def relacionados__create_relacionados_pue_ppd_tidy_report_json(
        self,
        *,
        rfc: Annotated[str, HeaderParam],
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[BaseBodyHeaderComprobanteRelacionadosTidy, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/reports/blockReport/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def reports__block_report(
        self,
        filters: Annotated[Reports_blockReportRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/reports/downloadReport/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def reports__download_report(
        self,
        filters: Annotated[BodyDownloadReport, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/reports/downloadReportPath/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def reports__download_report_by_path(
        self,
        filters: Annotated[BodyDownloadReportByPath, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/reports/getReports/",
        response_model=KReportsResponse[list[dict], None],
    )
    async def reports__get_reports(
        self,
        skip: Annotated[str, QueryParam],
        limit: Annotated[str, QueryParam],
        sortKey: Annotated[str, QueryParam],
        sortDirection: Annotated[str, QueryParam],
        filters: Annotated[BodyReports, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
    @post(
        path="/reports/reprocess",
        response_model=KReportsResponse[list[dict], None],
    )
    async def reports__reprocess_report(
        self,
        token: Annotated[str, Authorization(scheme=AuthScheme.Bearer)],
        filters: Annotated[Reprocess_reprocess_reportRequest, JsonBodyParam],
    ) -> KReportsResponse[list[dict], None]: ...
