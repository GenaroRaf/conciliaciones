from enum import Enum
from typing import TypeVar

from openpyxl.styles import Alignment, Border, Font, NamedStyle, PatternFill, Side

from conciliaciones.clients.report.styles.class_styles import (
    CellStyle,
    DataStyles,
    HeaderStyles,
    PivotTableStyles,
    SummaryStyles,
)


class OpenpyxlStylesExcel:
    header_styles: dict[HeaderStyles, NamedStyle]
    data_styles: dict[DataStyles, NamedStyle]
    summary_styles: dict[SummaryStyles, NamedStyle]
    pivot_table_styles: dict[PivotTableStyles, NamedStyle]
    cell_styles: dict[CellStyle, NamedStyle]

    def __init__(
        self,
    ) -> None:
        self.header_styles = create_named_styles(HeaderStyles)
        self.data_styles = create_named_styles(DataStyles)
        self.summary_styles = create_named_styles(SummaryStyles)
        self.pivot_table_styles = create_named_styles(PivotTableStyles)
        self.cell_styles = create_named_styles(CellStyle)


T = TypeVar("T", bound=Enum)


def create_named_styles(enum_t: type[T]) -> dict[T, NamedStyle]:
    styles = {}
    for style in enum_t:
        named_style = NamedStyle(name=f"{enum_t.__name__}_{style.name}")
        style_def = style.value

        if "font_color" in style_def:
            named_style.font = Font(
                bold=style_def.get("bold", False),
                italic=style_def.get("italic", False),
                color=style_def["font_color"],
            )

        if "align" in style_def:
            named_style.alignment = Alignment(horizontal=style_def["align"])

        if "bg_color" in style_def:
            named_style.fill = PatternFill(
                start_color=style_def["bg_color"],
                end_color=style_def["bg_color"],
                fill_type="solid",
            )

        if "border" in style_def and style_def["border"]:
            thin = Side(border_style="thin", color="000000")
            named_style.border = Border(left=thin, right=thin, top=thin, bottom=thin)

        styles[style] = named_style
    return styles
