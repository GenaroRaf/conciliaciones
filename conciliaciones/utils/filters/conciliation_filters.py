from k_link.db.core import ObjectId
from k_link.db.daos import ProjectDAO
from k_link.db.models import Project
from k_link.extensions import ConciliationType
from k_link.extensions.report_result import ReportMetadata


class ConciliationReportUtils:
    @staticmethod
    def build_filters_for_conciliation_type(
        project_id: ObjectId,
        conciliation_type: ConciliationType,
        year: int,
        month: int,
    ) -> dict:
        filters: dict = {
            "project_id": project_id,
            "conciliation_type": conciliation_type.value,
        }

        if conciliation_type == ConciliationType.MONTHLY:
            filters = {
                **filters,
                "conciliation_parameters.year": year,
                "conciliation_parameters.month": month,
            }
        elif conciliation_type == ConciliationType.ACCUMULATED:
            filters = {
                **filters,
                "conciliation_parameters.year": year,
            }

        return filters

    @staticmethod
    def find_today_execution_report(
        reports: list[ReportMetadata], run_id: str
    ) -> ReportMetadata | None:
        execution_report: ReportMetadata | None = next(
            (
                report
                for report in reports
                if ((report_run_id := report.run_id) and (report_run_id == run_id))
            ),
            None,
        )

        return execution_report

    @staticmethod
    def validate_history_report(project_id: ObjectId) -> bool:
        project_dao: ProjectDAO = ProjectDAO()

        find_project: Project | None = project_dao.get_by_id_sync(item_id=project_id)

        if find_project is None:
            raise ValueError(
                f"Proyecto con el ID {project_id} no encontrado al validar historial"
            )

        save_history: bool = find_project.save_history

        return save_history
