import re
import uuid
from io import BytesIO

import pandas as pd
from k_link.db.core import ObjectId
from k_link.db.daos import ERPFilesDAO, ExcelDataTypeDAO, ProjectDAO
from k_link.db.models import ERPFiles, ExcelDataType
from k_link.extensions import Nativo
from k_link.extensions.conciliation_type import ConciliationType
from k_link.extensions.datasources import DataSourceCatalog, DataSources
from k_link.extensions.influx import InfluxLogItem, Strategies
from k_link.extensions.pivot_k import PivoteKHeader
from k_link.extensions.report_config import HeaderConfig, OrigenColumna, TipoDato
from k_link.utils.files.abc_datasource import DataFrame
from loggerk import LoggerK
from pandas.api.types import is_object_dtype, is_string_dtype

from conciliaciones.clients.erp.erp_data.get_erp import DatosERP
from conciliaciones.clients.erp.erp_data.get_pivot_k import PivoteKManager
from conciliaciones.clients.erp.erp_data.utils.data_types import ValidaDataTypes
from conciliaciones.utils.completion_handler.airflow_contex_exception import (
    AirflowContexException,
)
from conciliaciones.utils.headers.headers_types import HeadersTypes
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage

# Constantes de DAO's
DAO_PROYECTO = ProjectDAO()
ERP_FILES = ERPFilesDAO()
EXCEL_DATA_TYPES = ExcelDataTypeDAO()
TYPE_HEADER = "validation"


class CleanData:
    _logger: LoggerK
    """
        Clase para limpieza y validación de datos, con manejo de UUIDs y 
        configuraciones de pivotes.
    """

    PIVOTE_K_UUID = "Pivote K UUID"
    PIVOTE_K_SERIE_FOLIO = "Pivote K SERIE_FOLIO"
    PIVOTE_K_FOLIO = "Pivote K FOLIO"

    def __init__(
        self,
        run_id: str,
        project_id_str: str,
        year: int,
        month: int,
        conciliation_type: ConciliationType,
    ) -> None:
        super().__init__()
        self._logger = LoggerK(self.__class__.__name__)
        self.project_id_str = project_id_str
        self.project_id = ObjectId(self.project_id_str)
        self.redis = RedisStorage()
        self.year = year
        self.month = month
        self._conciliation_type: ConciliationType = conciliation_type
        self.erp = DatosERP(
            run_id=run_id,
            project_id_str=self.project_id_str,
            year=year,
            month=month,
            conciliation_type=self._conciliation_type,
        )
        self.redis_keys = RedisKeys(
            run_id=run_id,
            project_id_str=self.project_id_str,
            month=month,
            year=year,
            conciliation_type=self._conciliation_type,
        )
        self._airflow_fail_exception = AirflowContexException(
            year=self.year,
            month=self.month,
            project_id=project_id_str,
            run_id=run_id,
            conciliation_type=self._conciliation_type,
        )
        self._header_types = HeadersTypes(
            run_id=run_id,
            project_id_str=self.project_id_str,
            month=month,
            year=year,
            conciliation_type=conciliation_type,
        )
        self.validos = 0
        self.no_validos = 0

    async def validador_pivotes(self) -> None:
        """
        Valida los pivotes definidos en la configuración de conciliación
        para un proyecto.
        """

        df_erp = self.get_df_erp()
        erp_files = await ERP_FILES.get(project_id=self.project_id)
        if erp_files is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró configuración de ERP Files para el proyecto {self.project_id}"
            )

        self._logger.info(f"Pivotes config: {erp_files.pivot_k}")
        if erp_files.pivot_k is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay configuración de Pivot K para el proyecto: {self.project_id}"
            )

        # Se recupera de redis la lista de dynamic headers
        headers_pivot: list[HeaderConfig] = self._header_types.get_headers_list(
            redis_key=self.redis_keys.get_headers_pivot_list_key()
        )
        headers_validation: list[HeaderConfig] = []

        total_validos = 0

        for pivote in erp_files.pivot_k:
            pivote_k_header = PivoteKManager.get_pivote_k_header_name(
                strategy=pivote.pivote_k_header
            )
            self._logger.info(msg=f"Estrategy: {pivote.pivote_k_header.value}")
            self._logger.info(msg=f"Header name: {pivote_k_header}")

            if pivote_k_header not in df_erp.columns:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"El pivote configurado no se encuentra en el archivo para el proyecto: {self.project_id}"
                )

            if pivote.pivote_k_header == PivoteKHeader.UUID:
                df_erp[pivote_k_header] = (
                    df_erp[pivote_k_header]
                    .str.upper()
                    .str.strip()
                    .str.replace("\t", "")
                )

            total_uuids: int = int(df_erp[pivote_k_header].count())
            self._logger.info(f"Total {pivote.pivote_k_header.value}: {total_uuids}")

            col_valida_str: str = f"(Valido) {pivote_k_header}"

            # Se añade valid header a la lista de dynamic headers
            header_validation: HeaderConfig | None = (
                self._header_types._add_headers_valid(
                    header_valid=col_valida_str,
                    pivot_k_header=pivote_k_header,
                    headers_pivot=headers_pivot,
                )
            )

            if header_validation is not None:
                headers_validation.append(header_validation)

            self.valida_pivot_header(
                header_type=pivote.pivote_k_header,
                header_name=pivote_k_header,
                col_name_pivote=df_erp,
            )

            df_filtro: DataFrame = pd.DataFrame(
                df_erp[df_erp[col_valida_str]][[pivote_k_header]]
            )
            buffer_df: BytesIO = self.redis.set_parquet(df=df_filtro)
            self.redis.set(
                key=self.redis_keys.get_erp_validos_redis_key(
                    strategy=pivote.pivote_k_header
                ),
                value=buffer_df,
            )

            validos_uuids = len(df_filtro)
            total_validos += validos_uuids
            self._logger.info(f"{pivote.pivote_k_header.value} valid: {validos_uuids}")

        # Se cargan los datos para guardar el log
        total_procesados = len(df_erp)
        metrics_key = self.redis_keys.get_metrics_redis_key()
        metrics_log = self.redis.get(metrics_key, InfluxLogItem) or InfluxLogItem()
        metrics_log.registers_metrics[Strategies.TOTAL].valid = int(total_validos)
        metrics_log.registers_metrics[Strategies.TOTAL].not_valid = int(
            len(df_erp) - total_validos
        )
        metrics_log.registers_metrics[Strategies.TOTAL].percentage_valid = (
            float(total_validos / len(df_erp)) * 100
        )
        metrics_log.registers_metrics[Strategies.TOTAL].percentage_not_valid = (
            float((len(df_erp) - total_validos) / len(df_erp)) * 100
        )

        ##Se cargan por estrategia
        if self.PIVOTE_K_UUID in df_erp.columns:
            metrics_log.registers_metrics[Strategies.UUID].valid = int(
                (df_erp[f"(Valido) {self.PIVOTE_K_UUID}"] == True).sum()
            )
            metrics_log.registers_metrics[Strategies.UUID].not_valid = int(
                (df_erp[f"(Valido) {self.PIVOTE_K_UUID}"] == False).sum()
            )
            metrics_log.registers_metrics[Strategies.UUID].percentage_valid = float(
                (df_erp[f"(Valido) {self.PIVOTE_K_UUID}"] == True).sum()
                / len(df_erp)
                * 100
            )
            metrics_log.registers_metrics[Strategies.UUID].percentage_not_valid = float(
                (df_erp[f"(Valido) {self.PIVOTE_K_UUID}"] == False).sum()
                / len(df_erp)
                * 100
            )
        if self.PIVOTE_K_FOLIO in df_erp.columns:
            metrics_log.registers_metrics[Strategies.FOLIO].valid = int(
                (df_erp[f"(Valido) {self.PIVOTE_K_FOLIO}"] == True).sum()
            )
            metrics_log.registers_metrics[Strategies.FOLIO].not_valid = int(
                (df_erp[f"(Valido) {self.PIVOTE_K_FOLIO}"] == False).sum()
            )
            metrics_log.registers_metrics[Strategies.FOLIO].percentage_valid = float(
                (df_erp[f"(Valido) {self.PIVOTE_K_FOLIO}"] == True).sum()
                / len(df_erp)
                * 100
            )
            metrics_log.registers_metrics[
                Strategies.FOLIO
            ].percentage_not_valid = float(
                (df_erp[f"(Valido) {self.PIVOTE_K_FOLIO}"] == False).sum()
                / len(df_erp)
                * 100
            )
        if self.PIVOTE_K_SERIE_FOLIO in df_erp.columns:
            metrics_log.registers_metrics[Strategies.SERIE_FOLIO].valid = int(
                (df_erp[f"(Valido) {self.PIVOTE_K_SERIE_FOLIO}"] == True).sum()
            )
            metrics_log.registers_metrics[Strategies.SERIE_FOLIO].not_valid = int(
                (df_erp[f"(Valido) {self.PIVOTE_K_SERIE_FOLIO}"] == False).sum()
            )
            metrics_log.registers_metrics[
                Strategies.SERIE_FOLIO
            ].percentage_valid = float(
                (df_erp[f"(Valido) {self.PIVOTE_K_SERIE_FOLIO}"] == True).sum()
                / len(df_erp)
                * 100
            )
            metrics_log.registers_metrics[
                Strategies.SERIE_FOLIO
            ].percentage_not_valid = float(
                (df_erp[f"(Valido) {self.PIVOTE_K_SERIE_FOLIO}"] == False).sum()
                / len(df_erp)
                * 100
            )
        # Se guarda lista dynamic headers en redis
        await self._header_types.save_redis_headers_list(
            redis_key=self.redis_keys.get_headers_validation_list_key(),
            headers_list=headers_validation,
        )

        self._logger.info(f"DF ERP: {df_erp.info()}")
        buffer_df: BytesIO = self.redis.set_parquet(df=df_erp)
        self.redis.set(key=self.redis_keys.get_erp_redis_key(), value=buffer_df)
        self.redis.set(
            key=self.redis_keys.get_metrics_redis_key(),
            value=metrics_log,
        )

    def get_df_erp(self) -> pd.DataFrame:
        """
        Obtiene el DataFrame almacenado en Redis.

            Returns:
                pd.DataFrame: DataFrame de ERP obtenido de Redis.

            Raises:
                ValueError: Si el DataFrame no se encuentra en Redis.
        """
        self._logger.info(f"Project ID: {self.project_id_str}")

        df_erp: pd.DataFrame | None = self.redis.get_df(
            redis_key=self.redis_keys.get_erp_redis_key()
        )

        if df_erp is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El DataFrame guardado en Redis con la key: {self.redis_keys.get_erp_redis_key()} no se encontró para el proyecto: {self.project_id_str}."
            )
        self._logger.info("DF ERP Data")
        self._logger.info(df_erp.info())
        return df_erp

    def valida_pivot_header(
        self,
        header_type: PivoteKHeader,
        header_name: str,
        col_name_pivote: pd.DataFrame,
    ) -> pd.Series:
        """
        Valida un encabezado de pivote.

            Args:
                header_type (EstrategiaConcilia): Tipo de estrategia.
                header_name (str): Nombre del encabezado.
                col_name_pivote (pd.DataFrame): Columna de pivote.

            Returns:
                pd.Series: Serie booleana con los resultados de la validación.
        """
        col_valida = f"(Valido) {header_name}"
        if header_type == PivoteKHeader.UUID:
            col_name_pivote[col_valida], col_name_pivote[header_name] = (
                self.validate_uuids(col_name_pivote[f"{header_name}"])
            )

            self.validos = 0

        elif header_type == PivoteKHeader.SERIE:
            col_name_pivote[col_valida] = self.validate_series(
                col_name_pivote[f"{header_name}"]
            )

            self.validos = 0

        elif (
            header_type == PivoteKHeader.FOLIO
            or header_type == PivoteKHeader.SERIE_FOLIO
        ):
            col_name_pivote[col_valida] = self.validate_folios(
                col_name_pivote[f"{header_name}"]
            )

            self.validos = 0

        return pd.Series(col_name_pivote[col_valida])

    def validate_uuids(self, column: pd.Series) -> tuple[pd.Series, pd.Series]:
        """
        Valida si los valores de una columna de pandas son UUIDs válidos.

            Args:
                column (pd.Series): Columna de un DataFrame de pandas a validar.

            Returns:
                pd.Series: Columna booleana indicando True si el valor es un UUID válido,
                False en caso contrario.
        """

        def is_valid_uuid(value_in) -> tuple[bool, str]:
            """
            Valida si los valores de una columna de pandas son UUIDs válidos.

                Args:
                    column (pd.Series): Columna a validar.

                Returns:
                    pd.Series: Serie booleana con True si es UUID válido,
                    False en caso contrario.
            """
            value: str = str(value_in)
            try:
                # Intentar convertir a UUID, permitiendo tanto mayúsculas como minúsculas
                value: str = self.normalizar_uuid(uuid=value)
                # str_value = re.sub(r"[^\w-]", "", value).strip()
                uuid_regex = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
                if re.match(uuid_regex, value) is None:
                    raise ValueError(
                        f"No hubo match al validar el uuid: {value} para el proyecto: {self.project_id_str}"
                    )

                uuid.UUID(value)
                self.validos += 1
                return True, value
            except (ValueError, TypeError):
                self.no_validos += 1
                return False, value

        resultados = column.apply(is_valid_uuid)
        validos, uuids_normalizados = zip(*resultados)

        return pd.Series(validos, index=column.index), pd.Series(
            uuids_normalizados, index=column.index
        )

    def validate_folios(self, column) -> pd.Series:
        """
        Valida si los valores de una columna de pandas son numeros enteros.

            Args:
                column (pd.Series): Columna de un DataFrame de pandas a validar.

            Returns:
                pd.Series: Columna booleana indicando True si el valor es un número válido,
                False en caso contrario.
        """

        def is_not_nan(value) -> bool:
            """No sean vacios o NaN"""
            return pd.notna(value) and pd.notnull(value)

            # try:
            #     str(value).isdigit()
            #     return True
            # except (ValueError, TypeError):
            #     return False

        return column.apply(is_not_nan)

    def validate_series(self, column) -> pd.Series:
        """
        Valida si los valores de una columna de pandas son letras Aa-Zz.

            Args:
                column (pd.Series): Columna a validar.

            Returns:
                pd.Series: Serie booleana con True si es una letra válida,
                False en caso contrario.
        """

        def is_valid_alpha(value) -> bool:
            """
            Valida si los valores de una columna de pandas son letras Aa-Zz.

                Args:
                    column (pd.Series): Columna a validar.

                Returns:
                    pd.Series: Serie booleana con True si es una letra válida,
                    False en caso contrario.
            """
            if not isinstance(value, str) or not value.strip():
                return False
            return bool(re.fullmatch(r"[A-Za-z]", value))

        return column.apply(is_valid_alpha)

    async def validador_tipo_datos(self, datasources_optional: list[str]):
        erp_files: ERPFiles | None = await ERP_FILES.get(project_id=self.project_id)

        if erp_files is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró configuración de ERP Files para el proyecto {self.project_id}"
            )

        headers_erp: list[HeaderConfig] = []

        data_sources: list[DataSources] = erp_files.data_sources
        data_sources_catalogs: list[DataSourceCatalog] = erp_files.data_sources_catalogs

        headers_erp = await self.validated_data_souces(
            data_sources=data_sources,
            data_sources_optional=datasources_optional,
            headers_erp=headers_erp,
        )

        headers_erp = await self.validated_data_sources_catalogs(
            data_sources_catalogs=data_sources_catalogs,
            headers_erp=headers_erp,
        )

        self._logger.info(f"Headers ERP: {headers_erp}")

        # Se guarda lista erp headers en redis
        await self._header_types.save_redis_headers_list(
            redis_key=self.redis_keys.get_headers_erp_list_key(),
            headers_list=headers_erp,
        )

    async def validated_data_souces(
        self,
        data_sources: list[DataSources],
        data_sources_optional: list[str],
        headers_erp: list[HeaderConfig],
    ) -> list[HeaderConfig]:
        """
        Valida los data sources y extrae los datos necesarios.

        Args:
            data_sources (list[DataSources]): lista de data sources a validar.
            data_sources_optional (list[str]): lista de data sources opcionales.

        """

        for data_source in data_sources:
            data_source_name: str = data_source.config.datasource_name
            self._logger.info(f"Data Source: {data_source_name}")
            self._logger.info(f"Data Source Name: {data_source.config.datasource_name}")

            if data_source_name in data_sources_optional:
                self._logger.info(
                    f"Data source {data_source_name} is optional, skipping."
                )
                continue

            redis_key: str = self.redis_keys.get_erp_data_source_redis_key(
                datasource=data_source_name
            )

            df_erp: pd.DataFrame | None = self.redis.get_df(redis_key=redis_key)

            if df_erp is None:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"DataFrame no encontrado en redis key: {redis_key} para el proyecto: {self.project_id_str}"
                )

            df_erp_clean: DataFrame = df_erp.copy()
            header_types: dict[str, ObjectId] = data_source.config.header_types

            df_erp_clean, headers_erp = await self.validated_headers_types(
                header_types=header_types,
                df_erp_clean=df_erp_clean,
                headers_erp=headers_erp,
            )

            # Asegurar que todos los registros tengan el origen correcto
            df_erp_clean["Origen Data Source"] = data_source_name
            self._logger.info(
                f"Columna 'Origen Data Source' actualizada con valor: {data_source_name}"
            )

            header_origen: HeaderConfig = HeaderConfig(
                nombre="Origen Data Source",
                configuracion_tipo_dato=TipoDato.TEXTO,
                origen=OrigenColumna.LABEL,
                mostrar_reporte=True,
            )
            headers_erp.append(header_origen)

            self.erp.save_redis(df_erp=df_erp_clean, redis_key=redis_key)

        return headers_erp

    async def validated_data_sources_catalogs(
        self,
        data_sources_catalogs: list[DataSourceCatalog],
        headers_erp: list[HeaderConfig],
    ) -> list[HeaderConfig]:
        """
        Valida los data sources catalogs y extrae los datos necesarios.

        Args:
            data_sources_catalogs (list[DataSourceCatalog]): lista de data sources catalogs a validar.
            headers_erp (list[HeaderConfig]): lista de headers ERP a actualizar.
        """
        for catalog in data_sources_catalogs:
            catalog_name = catalog.name
            self._logger.info(f"Catalog: {catalog}")
            self._logger.info(f"Catalog Name: {catalog_name}")

            redis_key: str = self.redis_keys.get_erp_data_source_redis_key(
                datasource=catalog_name
            )

            df_catalog: pd.DataFrame | None = self.redis.get_df(redis_key=redis_key)

            if df_catalog is None:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"DataFrame no encontrado en redis key: {redis_key} para el proyecto: {self.project_id_str}"
                )

            df_catalog_clean: DataFrame = df_catalog.copy()
            header_types: dict[str, ObjectId] = catalog.header_types

            df_catalog_clean, headers_erp = await self.validated_headers_types(
                header_types=header_types,
                df_erp_clean=df_catalog_clean,
                headers_erp=headers_erp,
            )

            self.erp.save_redis(df_erp=df_catalog_clean, redis_key=redis_key)

        return headers_erp

    async def validated_headers_types(
        self,
        header_types: dict[str, ObjectId],
        df_erp_clean: pd.DataFrame,
        headers_erp: list[HeaderConfig],
    ) -> tuple[DataFrame, list[HeaderConfig]]:
        self._logger.info(f"Header Types: {header_types}")

        for header, data_type in header_types.items():
            data_type_config: ExcelDataType | None = await EXCEL_DATA_TYPES.get_by_id(
                data_type
            )

            if data_type_config is None:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"Tipo de dato {data_type} no identificado para {header} en el proyecto: {self.project_id_str}"
                )

            self._logger.info(f"Header : {header} - {data_type_config}")

            # Configuracion para el ERP header
            nativo: Nativo = data_type_config.nativo
            nombre_erp: str = header
            tipo_dato: TipoDato = nativo.tipo_dato

            header_erp: HeaderConfig = HeaderConfig(
                nombre=nombre_erp,
                configuracion_tipo_dato=tipo_dato,
                origen=OrigenColumna.ERP,
                mostrar_reporte=True,
            )
            headers_erp.append(header_erp)

            # Nombre para erp_k header
            column_name = f"{header} (K)"

            # Header erp_k
            if tipo_dato == TipoDato.TEXTO:
                mostrar_reporte = False
            else:
                mostrar_reporte = True

            header_erp_k: HeaderConfig = HeaderConfig(
                nombre=column_name,
                configuracion_tipo_dato=tipo_dato,
                origen=OrigenColumna.CLEAN_DATA,
                mostrar_reporte=mostrar_reporte,
            )
            headers_erp.append(header_erp_k)

            col = df_erp_clean[header]

            if (
                (nativo == Nativo.STRING)
                and (is_object_dtype(arr_or_dtype=col))
                or (is_string_dtype(arr_or_dtype=col))
            ):
                column_name: str = header
            else:
                # Generación de nuevo columna con datos procesados
                df_erp_clean[column_name] = await self.clean_data_type(
                    nativo=nativo,
                    formato=data_type_config.formato,
                    data_values=pd.Series(df_erp_clean[header]),
                )

                if nativo == Nativo.STRING:
                    df_erp_clean.loc[len(df_erp_clean), column_name] = "-"
                    df_erp_clean[column_name] = df_erp_clean[column_name].replace(
                        r"\.0$", "", regex=True
                    )

        return df_erp_clean, headers_erp

    async def clean_data_type(
        self, nativo: Nativo, formato: str, data_values: pd.Series
    ) -> pd.Series:
        """
        Limpia y valida un tipo de dato.

        Args:
            data_type (Any): Tipo de dato a validar.
            data_values (pd.Series): Valores a limpiar y validar.

        Returns:
            pd. : Datos limpios.
        """
        valida_data_type = ValidaDataTypes(
            values=data_values, dtype=nativo, date_format=formato
        )
        data_values = valida_data_type.validate_data()
        return data_values

    def normalizar_uuid(self, uuid: str) -> str:
        uuid_limpio: str = uuid.replace("‐", "-").replace("–", "-").replace("—", "-")
        # uuid_limpio: str = uuid_limpio.replace('\ufeff', '').replace('\u200b', '').replace('\xa0', '').strip()

        if uuid_limpio != uuid:
            self._logger.error(f"UUID limpiado: {uuid} -> {uuid_limpio}")
        return uuid_limpio
