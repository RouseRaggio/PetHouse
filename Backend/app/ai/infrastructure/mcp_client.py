import asyncio
import traceback
from typing import Any, Dict, List, Optional, Tuple

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from app.ai.domain.entities import (
    ColumnMetadata,
    DatabaseSchema,
    QueryResult,
    TableMetadata,
)
from app.ai.domain.exceptions import SQLValidationError
from app.ai.domain.interfaces import MCPClient, SQLValidator
from app.ai.infrastructure.exceptions import (
    MCPConnectionError,
    MCPExecutionError,
    MCPInvalidResponseError,
    MCPTimeoutError,
)


class MCPToolboxClient(MCPClient):
    def __init__(
        self,
        toolbox_url: str,
        timeout: float = 30.0,
        sql_validator: Optional[SQLValidator] = None,
    ) -> None:
        self._toolbox_url = toolbox_url
        self._timeout = timeout
        self._sql_validator = sql_validator

    async def get_schema(self) -> DatabaseSchema:
        print("=" * 80)
        print("LLAMANDO A get_schema")
        print("=" * 80)

        raw = await self._call_tool("get_schema", {})

        print("=" * 80)
        print("RESPUESTA CRUDA DEL TOOLBOX (get_schema)")
        print(raw)
        print("=" * 80)

        schema = self._parse_schema(raw)

        print("=" * 80)
        print("SCHEMA PARSEADO")
        print(schema)
        print("=" * 80)

        return schema

    async def execute_query(self, sql: str) -> QueryResult:
        if self._sql_validator is None:
            raise RuntimeError(
                "SQLValidator is not configured. Cannot execute SQL."
            )

        validation = self._sql_validator.validate(sql)

        print("=" * 80)
        print("VALIDACIÓN SQL")
        print(validation)
        print("=" * 80)

        if not validation.is_valid:
            raise SQLValidationError(
                validation.error or "SQL validation failed"
            )

        print("=" * 80)
        print("SQL ENVIADO AL TOOLBOX")
        print(sql)
        print("=" * 80)

        try:
            raw = await self._call_tool(
                "execute_query",
                {
                    "sql": sql,
                    "max_rows": validation.max_rows,
                    "execution_timeout_ms": validation.execution_timeout_ms,
                },
            )

            print("=" * 80)
            print("RESPUESTA CRUDA DEL TOOLBOX (execute_query)")
            print(raw)
            print("=" * 80)

        except asyncio.TimeoutError:
            raise MCPTimeoutError("MCP query execution timed out")

        except (ConnectionError, OSError) as e:
            raise MCPConnectionError(f"MCP connection failed: {e}")

        except RuntimeError as e:
            print("=" * 80)
            print("ERROR DEVUELTO POR EL TOOLBOX")
            print(str(e))
            traceback.print_exc()
            print("=" * 80)
            raise MCPExecutionError(str(e))

        except Exception as e:
            print("=" * 80)
            print("EXCEPCIÓN GENERAL")
            print(repr(e))
            traceback.print_exc()
            print("=" * 80)
            raise MCPExecutionError(f"MCP execution failed: {e}")

        result = self._parse_query_result(raw)

        print("=" * 80)
        print("QUERY RESULT PARSEADO")
        print(result)
        print("=" * 80)

        return result

    async def _call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        print("=" * 80)
        print(f"LLAMANDO TOOL: {tool_name}")
        print("ARGUMENTOS:")
        print(arguments)
        print("=" * 80)

        async with httpx.AsyncClient(
            timeout=httpx.Timeout(self._timeout),
        ) as http_client:
            async with streamable_http_client(
                url=self._toolbox_url,
                http_client=http_client,
            ) as streams:
                async with ClientSession(
                    streams[0],
                    streams[1],
                    read_timeout_seconds=self._timeout,
                ) as session:
                    try:
                        await session.initialize()
                    except Exception as e:
                        print("=" * 80)
                        print("ERROR EN INITIALIZE")
                        traceback.print_exc()
                        print("=" * 80)
                        raise

                    try:
                        result = await session.call_tool(
                            tool_name,
                            arguments,
                        )
                    except Exception as e:
                        print("=" * 80)
                        print("ERROR EN CALL_TOOL (SDK)")
                        traceback.print_exc()
                        print("=" * 80)
                        raise

        print("=" * 80)
        print("RESPUESTA MCP")
        print(result)
        print("=" * 80)

        if result.isError:
            error_text = self._extract_text(result.content)

            print("=" * 80)
            print("ERROR MCP")
            print(error_text)
            print("=" * 80)

            raise RuntimeError(
                f"MCP tool '{tool_name}' failed: {error_text}"
            )

        content = self._extract_content(result.content)

        print("=" * 80)
        print("CONTENIDO EXTRAÍDO")
        print(content)
        print("=" * 80)

        return content

    def _parse_query_result(self, raw: Any) -> QueryResult:
        if isinstance(raw, str):
            import json

            try:
                raw = json.loads(raw)
            except json.JSONDecodeError:
                raise MCPInvalidResponseError(
                    "Failed to parse query result: invalid JSON"
                )

        if not isinstance(raw, dict):
            raise MCPInvalidResponseError(
                "Failed to parse query result: expected a dict"
            )

        columns = raw.get("columns", [])
        rows_raw = raw.get("rows", [])
        execution_ms = raw.get("execution_ms", 0)

        rows: List[Tuple[Any, ...]] = [
            tuple(row) if isinstance(row, list) else (row,)
            for row in rows_raw
        ]

        return QueryResult(
            columns=list(columns),
            rows=rows,
            row_count=len(rows),
            execution_ms=int(execution_ms),
        )

    def _extract_content(self, content: List[Any]) -> Any:
        import json

        texts = []

        for item in content:
            text = getattr(item, "text", None)
            if text is not None:
                texts.append(text)

        raw = "".join(texts)

        if not raw:
            return {}

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw

    def _extract_text(self, content: List[Any]) -> str:
        texts = []

        for item in content:
            text = getattr(item, "text", "")
            if text:
                texts.append(str(text))

        return " ".join(texts)

    def _parse_schema(self, raw: Any) -> DatabaseSchema:
        print("=" * 80)
        print("RAW RECIBIDO EN _parse_schema")
        print(raw)
        print("=" * 80)

        if isinstance(raw, str):
            import json

            try:
                raw = json.loads(raw)
            except json.JSONDecodeError:
                return DatabaseSchema(tables=[])

        if not isinstance(raw, dict):
            return DatabaseSchema(tables=[])

        data = raw

        if "rows" in data:
            rows = data.get("rows", [])

            if rows:
                row = rows[0]

                if row:
                    cell = row[0]

                    if isinstance(cell, str):
                        import json

                        try:
                            cell = json.loads(cell)
                        except json.JSONDecodeError:
                            return DatabaseSchema(tables=[])

                    if isinstance(cell, dict):
                        data = cell

        tables_raw = data.get("tables", [])

        print("=" * 80)
        print("TABLAS ENCONTRADAS")
        print(tables_raw)
        print("=" * 80)

        if not isinstance(tables_raw, list):
            return DatabaseSchema(tables=[])

        tables: List[TableMetadata] = []

        for tbl in tables_raw:
            table = self._parse_table(tbl)

            if table is not None:
                tables.append(table)

        return DatabaseSchema(tables=tables)

    def _parse_table(self, raw: Any) -> Optional[TableMetadata]:
        if not isinstance(raw, dict):
            return None

        name = raw.get("name", "")

        if not name:
            return None

        columns: List[ColumnMetadata] = []

        for col in raw.get("columns", []):
            column = self._parse_column(col)

            if column is not None:
                columns.append(column)

        return TableMetadata(
            name=name,
            columns=columns,
            description=raw.get("description"),
        )

    def _parse_column(self, raw: Any) -> Optional[ColumnMetadata]:
        if not isinstance(raw, dict):
            return None

        name = raw.get("name", "")

        if not name:
            return None

        return ColumnMetadata(
            name=name,
            type=raw.get("type", "TEXT"),
            nullable=bool(raw.get("nullable", True)),
            is_primary_key=bool(raw.get("primary_key", False)),
            foreign_key=raw.get("foreign_key"),
            description=raw.get("description"),
            default_value=raw.get("default_value"),
        )