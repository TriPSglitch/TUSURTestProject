from openpyxl.styles import *

border_style = Border(
    left=Side(border_style='thin', color='000000'),
    right=Side(border_style='thin', color='000000'),
    top=Side(border_style='thin', color='000000'),
    bottom=Side(border_style='thin', color='000000')
)

header_style = NamedStyle(name='header')
header_style.font = Font(bold=True, color='FFFFFF')
header_style.alignment = Alignment(horizontal='center', vertical='center')
header_style.fill = PatternFill(start_color='4F81BD', end_color='4F81BD', fill_type='solid')
header_style.border = border_style

cell_style = NamedStyle(name='cell')
cell_style.alignment = Alignment(horizontal='left', vertical='center')
cell_style.border = border_style

city_style = NamedStyle(name='city')
city_style.font = Font(bold=True)
city_style.alignment = Alignment(horizontal='center', vertical='center')
city_style.border = border_style


def get_header_style() -> NamedStyle:
    return header_style


def get_cell_style() -> NamedStyle:
    return cell_style


def get_city_style() -> NamedStyle:
    return city_style


def get_border_style() -> Border:
    return border_style


def get_columns_width(*, columns: tuple) -> int:
    max_length = 0
    for cell in columns:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        except:
            pass
    adjusted_width = (max_length + 2)
    return adjusted_width
