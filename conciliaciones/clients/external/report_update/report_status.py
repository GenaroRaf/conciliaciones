from contextvars import Context

from k_link.db.core.objectid import ObjectId
from k_link.db.daos import ConciliationReportDAO
from k_link.db.models import ConciliationReport
from k_link.extensions import ConciliationType
from k_link.extensions.parameters import (
    AccumulatedParameters,
    MonthlyParameters,
    UnitParameters,
)
from k_link.extensions.report_result import (
    ReportMetadata,
    StatusConciliationReport,
)
from k_link.utils.bucket import BucketManager
from k_link.utils.pydantic_types import Date
from loggerk import LoggerK

from conciliaciones.utils.completion_handler.airflow_contex_exception import (
    AirflowContexException,
)
from conciliaciones.utils.filters.conciliation_filters import ConciliationReportUtils
from conciliaciones.utils.redis.redis_storage import RedisStorage


class StatusReportManager:
    _logger: LoggerK
    _context: Context

    def __init__(
        self,
        run_id: str,
        project_id_str: str,
        conciliation_type: ConciliationType,
        month: int,
        year: int,
    ) -> None:
        super().__init__()
        self._logger = LoggerK(self.__class__.__name__)
        self.run_id: str = run_id
        self.project_id_str: str = project_id_str
        self.project_id = ObjectId(project_id_str)
        self.redis = RedisStorage()  # noqa: F821
        self.year: int = year
        self.month: int = month
        self._conciliation_type: ConciliationType = conciliation_type

        self._conciliation_report_dao = ConciliationReportDAO()
        self._bucket_manager = BucketManager()

        self._airflow_fail_exception = AirflowContexException(
            year=self.year,
            month=self.month,
            project_id=project_id_str,
            run_id=run_id,
            conciliation_type=conciliation_type,
        )

    async def set_started_status_report(self) -> None:
        self._logger.info(
            f"Setting started status report for project {self.project_id_str}, year {self.year}, month {self.month}, type {self._conciliation_type}, run_id {self.run_id}"
        )

        filters: dict = ConciliationReportUtils.build_filters_for_conciliation_type(
            project_id=self.project_id,
            conciliation_type=self._conciliation_type,
            year=self.year,
            month=self.month,
        )

        create_execution_date = Date().today()

        conciliation_report: (
            ConciliationReport | None
        ) = await self._conciliation_report_dao.get(**filters)

        if conciliation_report is None:
            if self._conciliation_type == ConciliationType.MONTHLY:
                conciliation_parameters = MonthlyParameters(
                    year=self.year,
                    month=self.month,
                )
            elif self._conciliation_type == ConciliationType.ACCUMULATED:
                conciliation_parameters = AccumulatedParameters(
                    year=self.year,
                )
            else:
                conciliation_parameters = UnitParameters()

            conciliation_report = ConciliationReport(
                project_id=self.project_id,
                conciliation_type=self._conciliation_type,
                conciliation_parameters=conciliation_parameters,
                report_metadata=[
                    ReportMetadata(
                        run_id=self.run_id,
                        name={},
                        s3_path={},
                        status=StatusConciliationReport.STARTED,
                        detail="Reporte iniciado",
                        requested_by=None,
                        creation_date=create_execution_date,
                    )
                ],
            )

            await self._conciliation_report_dao.create(data=conciliation_report)

            return

        reports: list[ReportMetadata] = conciliation_report.report_metadata

        self._logger.info(f"Reports result: {reports}")

        if not ConciliationReportUtils.validate_history_report(self.project_id):
            report_result = reports[-1]

            if report_result.s3_path:
                for value in report_result.s3_path.values():
                    self._bucket_manager.delete_dir(value)

            report_result.s3_path = {}
            report_result.name = {}
            report_result.status = StatusConciliationReport.STARTED

            mongo_updated: (
                ConciliationReport | None
            ) = await self._conciliation_report_dao.update_by_id(
                item_id=conciliation_report.id,  # type: ignore
                data=conciliation_report,
            )

            if not mongo_updated:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"No se pudo actualizar el reporte de conciliación en la base de datos para el proyecto: {self.project_id}"
                )

            return

        report_result: ReportMetadata | None = (
            ConciliationReportUtils.find_today_execution_report(reports, self.run_id)
        )

        if report_result is not None:
            if report_result.s3_path:
                for value in report_result.s3_path.values():
                    self._bucket_manager.delete_dir(value)

            report_result.status = StatusConciliationReport.STARTED
            report_result.detail = "Reporte iniciado"
        else:
            report_metadata = ReportMetadata(
                run_id=self.run_id,
                name={},
                s3_path={},
                status=StatusConciliationReport.STARTED,
                detail="Reporte iniciado",
                requested_by=None,
                creation_date=create_execution_date,
            )
            reports.append(report_metadata)

        updated: (
            ConciliationReport | None
        ) = await self._conciliation_report_dao.update_by_id(
            item_id=conciliation_report.id,  # type: ignore
            data=conciliation_report,
        )

        if not updated:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se pudo actualizar el reporte de conciliación en la base de datos para el proyecto: {self.project_id}"
            )

        return
