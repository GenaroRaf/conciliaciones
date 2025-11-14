import json
from enum import Enum

from k_link.db.core import ObjectId
from k_link.extensions.conciliation_type import ConciliationType
from k_link.extensions.report_config import HeaderConfig, OrigenColumna, TipoDato
from loggerk import LoggerK

from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage


class HeadersTypes:
    def __init__(
        self,
        run_id,
        project_id_str: str,
        month: int,
        year: int,
        conciliation_type: ConciliationType,
    ):
        self._logger = LoggerK(self.__class__.__name__)
        self.project_id_str: str = project_id_str
        self.project_id = ObjectId(project_id_str)
        self.month: int = month
        self.year: int = year
        self.redis = RedisStorage()
        self._redis_keys = RedisKeys(
            month=month,
            year=year,
            project_id_str=project_id_str,
            run_id=run_id,
            conciliation_type=conciliation_type,
        )

    @staticmethod
    def tipo_dato_serializer(obj):
        """
        Serializa objetos específicos en un formato compatible con JSON.

        Args:
            obj (Any): Objeto a serializar, puede ser de tipo Enum o HeaderConfig.

        Returns:
            Any: Valor serializado del objeto. Puede ser un valor primitivo (para Enum)
            o un diccionario con los atributos serializados (para HeaderConfig).

        Raises:
            TypeError: Si el tipo de objeto no es compatible con la serialización definida.
        """

        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, HeaderConfig):
            return {
                "nombre": obj.nombre,
                "configuracion_tipo_dato": obj.configuracion_tipo_dato.value,
                "origen": obj.origen.value,
                "mostrar_reporte": obj.mostrar_reporte,
            }
        raise TypeError(f"Type {type(obj)} not serializable")

    def _add_headers_valid(
        self,
        header_valid: str,
        pivot_k_header: str,
        headers_pivot: list[HeaderConfig],
    ) -> HeaderConfig | None:
        """
        Agrega un nuevo header de validación al listado de headers dinámicos si se encuentra un header pivote coincidente.

        Args:
            header_valid (str): Nombre del nuevo header de validación a agregar.
            pivot_k_header (str): Nombre del header que actúa como pivote para validar si se debe agregar el nuevo header.
            headers_dynamic (list[HeaderConfig]): Lista de headers dinámicos donde se buscará el pivote y se agregará el nuevo header.

        Returns:
            None

        Logs:
            Info: Si el header de validación fue añadido o si el pivote no fue encontrado.
        """

        header_config = None
        for header_dynamic in headers_pivot:
            if header_dynamic.nombre == pivot_k_header:
                header_config = HeaderConfig(
                    nombre=header_valid,
                    configuracion_tipo_dato=TipoDato.BOOLEANO,
                    origen=OrigenColumna.VALIDACION,
                    mostrar_reporte=True,
                )

                self._logger.info(f"Header pivot: {header_valid} añadido")

                break

        if header_config is None:
            self._logger.info(f"Header pivot: {header_valid} no encontrado")

        return header_config

    def _add_headers_pivot(
        self,
        header_list: list[str],
        pivote_k_header_k: str,
        headers_erp_final: list[HeaderConfig],
        headers_pivot: list[HeaderConfig],
    ) -> None:
        """
        Agrega un nuevo header pivote a la lista de headers dinámicos si se encuentra un header correspondiente en la lista de headers ERP final.

        Args:
            header_list (list[str]): Lista de nombres de headers a verificar y agregar como pivotes.
            pivote_k_header_k (str): Nombre del nuevo header pivote a agregar.
            headers_erp_final (list[HeaderConfig]): Lista de headers ERP final donde se buscarán las coincidencias.
            headers_dynamic (list[HeaderConfig]): Lista de headers dinámicos a los cuales se añadirá el nuevo header pivote.

        Returns:
            None

        Logs:
            Info: Si el header pivote fue añadido o si no se encontró el header correspondiente.
        """

        for header in header_list:
            for header_erp in headers_erp_final:
                if header_erp.nombre == header:
                    header_dynamic = HeaderConfig(
                        nombre=pivote_k_header_k,
                        configuracion_tipo_dato=header_erp.configuracion_tipo_dato,
                        origen=OrigenColumna.PIVOTE,
                        mostrar_reporte=True,
                    )
                    headers_pivot.append(header_dynamic)

                    self._logger.info(f"Header pivot: {header} añadido")

                    break

            self._logger.info(f"Header pivot: {header} no encontrado")

    def get_headers_list(self, redis_key: str) -> list[HeaderConfig]:
        """
        Recupera los headers dinámicos desde una clave en Redis y los convierte en objetos HeaderConfig.

        Returns:
            list[HeaderConfig]: Lista de objetos HeaderConfig que representan los headers dinámicos obtenidos desde Redis.

        Raises:
            ValueError: Si la lista de headers dinámicos en Redis está vacía.

        Logs:
            Info: El número de columnas dinámicas obtenidas y la lista completa de headers dinámicos.
        """

        headers_json_str = self.redis.get(key=redis_key, object_type=str)

        self._logger.info(f"Lista de headers: {redis_key}")

        if headers_json_str is None:
            return []

        headers_json: dict = json.loads(headers_json_str)

        headers_list: list[HeaderConfig] = []

        for header in headers_json:
            header_config = HeaderConfig(
                nombre=header["nombre"],
                configuracion_tipo_dato=header["configuracion_tipo_dato"],
                origen=header["origen"],
                mostrar_reporte=header["mostrar_reporte"],
            )
            headers_list.append(header_config)

        self._logger.info(f"Numero de columnas obtenidas: {len(headers_list)}")
        self._logger.info(f"Headers: {headers_list}")

        return headers_list

    async def save_redis_headers_list(
        self, redis_key: str, headers_list: list[HeaderConfig]
    ):
        """
        Guarda los headers ERP en Redis después de serializarlos en formato JSON.

        Args:
            headers_erp (list[HeaderConfig]): Lista de objetos HeaderConfig que representan los headers ERP a guardar en Redis.

        Returns:
            None

        Logs:
            Info: El número de columnas ERP guardadas y la lista completa de headers ERP.
        """

        # Serializamos a JSON y lo almacenamos en Redis
        headers_json = [
            {
                "nombre": h.nombre,
                "configuracion_tipo_dato": h.configuracion_tipo_dato,
                "origen": h.origen,
                "mostrar_reporte": h.mostrar_reporte,
            }
            for h in headers_list
        ]
        headers_json = json.dumps(
            headers_list, default=HeadersTypes.tipo_dato_serializer
        )

        self._logger.info(f"Numero de columnas guardadas: {len(headers_list)}")
        self._logger.info(f"Headers: {headers_list}")

        # Se guarda lista de headers erp en redis
        self.redis.set(key=redis_key, value=headers_json)

    def save_redis_report_types(
        self, name_report_type: str, headers_report_type: list[HeaderConfig]
    ):
        """
        Guarda los headers del report type correspondiente en Redis después de serializarlos en formato JSON.

        Args:
            headers_dynamic (list[HeaderConfig]): Lista de objetos HeaderConfig que representan los headers
            del report type correspondiente a guardar en Redis.

        Logs:
            Info: El número de columnas dinámicas guardadas y la lista completa de headers dinámicos.
        """

        redis_key_headers_sat = self._redis_keys.get_headers_report_type_list_key(
            name_report_type=name_report_type
        )

        # Serializamos a JSON
        headers_sat_json = [
            {
                "nombre": h.nombre,
                "configuracion_tipo_dato": h.configuracion_tipo_dato,
                "origen": h.origen,
                "mostrar_reporte": h.mostrar_reporte,
            }
            for h in headers_report_type
        ]
        headers_sat_json = json.dumps(
            headers_report_type, default=HeadersTypes.tipo_dato_serializer
        )

        self._logger.info(
            f"Numero de columnas {name_report_type} guardadas: {len(headers_report_type)}"
        )
        self._logger.info(f"{name_report_type} headers: {headers_report_type}")

        # Se guarda lista de dynamic headers en redis
        self.redis.set(key=redis_key_headers_sat, value=headers_sat_json)
