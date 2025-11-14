from k_link.db.core import ObjectId
from k_link.db.daos import LinkServicesDAO, ReportCatalogDAO
from k_link.db.models import LinkServices, ReportCatalog
from k_link.extensions.conciliation_type import ConciliationType
from k_link.extensions.report_config import KReportsRequest, ReportConfig
from loggerk import LoggerK
from pandas import DataFrame

from conciliaciones.models.sheets_model import ReportSheet
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage

link_services_dao = LinkServicesDAO()
report_type = ReportCatalogDAO()


class ReportSheets:
    def __init__(
        self,
        run_id: str,
        project_id_str: str,
        month: int,
        year: int,
        conciliation_type: ConciliationType,
    ):
        self._logger = LoggerK(self.__class__.__name__)
        self.project_id_str = project_id_str
        self.month = month
        self.year = year
        self.redis = RedisStorage()
        self.redis_keys = RedisKeys(
            run_id=run_id,
            project_id_str=self.project_id_str,
            month=self.month,
            year=self.year,
            conciliation_type=conciliation_type,
        )

    async def get_report_sheets_key(
        self, report_config: ReportConfig
    ) -> list[ReportSheet]:
        report_sheets: list[KReportsRequest] | None = report_config.report_sheets

        if report_sheets is None:
            report_sheets = []

        sheets_key: list[ReportSheet] = []
        for report_sheet in report_sheets:
            report_type: ReportCatalog | None = await ReportCatalogDAO().get_by_id(
                report_sheet.report_id
            )

            if report_type is None:
                raise ValueError(f"Report type not found: {report_sheet.report_id}")

            service: str = report_type.function_service.service
            funcion: str = report_type.function_service.function_name
            name: str = report_type.name

            if service is None:
                raise ValueError(
                    f"Service not found for report type: {report_sheet.report_id}"
                )

            sheets_key.append(
                ReportSheet(
                    name=name,
                    redis_key=self.redis_keys.get_sat_sheets_key(funcion=funcion),
                )
            )

        return sheets_key

    async def get_report_sheets(
        self,
    ) -> tuple[list[DataFrame], list[str], list[KReportsRequest]]:
        link_services: LinkServices | None = await LinkServicesDAO().get(
            project_id=ObjectId(self.project_id_str)
        )

        if link_services is None:
            raise ValueError(
                f"Link services not found for project: {self.project_id_str}"
            )

        report_sheets_complete: list[KReportsRequest] = []

        if (
            link_services.report_config
            and link_services.report_config.report_sheets is not None
        ):
            report_sheets_complete: list[KReportsRequest] = (
                link_services.report_config.report_sheets
                if link_services.report_config
                and link_services.report_config.report_sheets
                else []
            )

        report_config: ReportConfig | None = link_services.report_config

        if report_config is None:
            raise ValueError(
                f"Report config not found for project: {self.project_id_str}"
            )

        report_sheets: list[ReportSheet] = await self.get_report_sheets_key(
            report_config=report_config
        )

        df_list: list[DataFrame] = []
        name_df: list[str] = []
        for sheet_key in report_sheets:
            redis_key: str = sheet_key.redis_key
            name: str = sheet_key.name

            df: DataFrame | None = self.redis.get_df(redis_key=redis_key)

            if df is None:
                raise ValueError(f"df vacio. ID project: {self.project_id_str}")

            df_list.append(df)
            name_df.append(name)

        return df_list, name_df, report_sheets_complete
