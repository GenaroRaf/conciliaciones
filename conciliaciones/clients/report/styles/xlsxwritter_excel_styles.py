from enum import Enum
from typing import TypeVar

from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook

from conciliaciones.clients.report.styles.class_styles import (
    CellStyle,
    DataStyles,
    HeaderStyles,
    PivotTableStyles,
    SummaryStyles,
)


class StylesExcel:
    header_styles: dict[HeaderStyles, Format]
    data_styles: dict[DataStyles, Format]
    summary_styles: dict[SummaryStyles, Format]
    pivot_table_styles: dict[PivotTableStyles, Format]
    cell_styles: dict[CellStyle, Format]

    def __init__(self, workbook: Workbook) -> None:
        self.header_styles = create_formats(workbook, HeaderStyles)
        self.data_styles = create_formats(workbook, DataStyles)
        self.summary_styles = create_formats(workbook, SummaryStyles)
        self.pivot_table_styles = create_formats(workbook, PivotTableStyles)
        self.cell_styles = create_formats(workbook, CellStyle)


T = TypeVar("T", bound=Enum)


def create_formats(workbook: Workbook, enum_t: type[T]) -> dict[T, Format]:
    """
    Configura y devuelve todos los estilos de Excel agrupados por categorías.
    """
    styles_formats = {member.name: member for member in enum_t}
    return {
        style: workbook.add_format(style.value) for style in styles_formats.values()
    }
