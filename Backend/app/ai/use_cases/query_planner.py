import re

from app.ai.domain.entities import (
    AIExecutionContext,
    AIRequest,
    PlannedQuery,
    QueryResult,
)
from app.ai.domain.interfaces import AIProvider, PromptTemplate, SchemaProvider


class QueryPlanner:
    def __init__(
        self,
        schema_provider: SchemaProvider,
        prompt_template: PromptTemplate,
        ai_provider: AIProvider,
    ) -> None:
        self._schema_provider = schema_provider
        self._prompt_template = prompt_template
        self._ai_provider = ai_provider

    async def plan_query(
        self, question: str, context: AIExecutionContext
    ) -> PlannedQuery:

        print("=" * 80)
        print("INICIO plan_query()")
        print("=" * 80)

        print("Obteniendo esquema...")
        schema = await self._schema_provider.get_database_schema()
        print("✓ Esquema obtenido")

        context.database_schema = schema

        print("Generando prompt...")
        prompt = self._prompt_template.render_sql_prompt(
            question=question,
            schema=schema,
            context=context,
        )

        print("=" * 80)
        print("PROMPT ENVIADO A GROQ")
        print("=" * 80)
        print(prompt)
        print("=" * 80)

        print("ANTES DE LLAMAR A GROQ")

        ai_response = await self._ai_provider.generate(
            AIRequest(prompt=prompt)
        )

        print("DESPUÉS DE LLAMAR A GROQ")

        print("=" * 80)
        print("RESPUESTA COMPLETA DEL LLM")
        print("=" * 80)
        print(ai_response.content)
        print("=" * 80)

        sql = self._extract_sql(ai_response.content)

        print("=" * 80)
        print("SQL EXTRAÍDO")
        print("=" * 80)
        print(sql)
        print("=" * 80)

        return PlannedQuery(
            sql=sql,
            schema=schema,
            prompt=prompt,
        )

    async def format_response(
        self,
        question: str,
        sql: str,
        result: QueryResult,
        context: AIExecutionContext,
    ) -> str:

        prompt = self._prompt_template.render_response_prompt(
            question=question,
            sql=sql,
            result=result,
            context=context,
        )

        print("=" * 80)
        print("PROMPT DE RESPUESTA")
        print("=" * 80)
        print(prompt)
        print("=" * 80)

        ai_response = await self._ai_provider.generate(
            AIRequest(prompt=prompt)
        )

        print("=" * 80)
        print("RESPUESTA FINAL DEL LLM")
        print("=" * 80)
        print(ai_response.content)
        print("=" * 80)

        return ai_response.content

    def _extract_sql(self, content: str) -> str:
        cleaned = content.strip()

        # Eliminar bloques Markdown
        cleaned = re.sub(
            r"^```sql\s*", "", cleaned, flags=re.IGNORECASE
        )
        cleaned = re.sub(r"^```\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

        # Eliminar etiquetas XML/HTML
        cleaned = re.sub(
            r"</?sql>", "", cleaned, flags=re.IGNORECASE
        )
        cleaned = re.sub(
            r"</?query>", "", cleaned, flags=re.IGNORECASE
        )

        # Buscar el primer SELECT
        match = re.search(
            r"(?is)\bSELECT\b.*?;?\s*$",
            cleaned,
        )

        if match:
            cleaned = match.group(0)

        print("=" * 80)
        print("SQL DESPUÉS DE LIMPIEZA")
        print("=" * 80)
        print(cleaned)
        print("=" * 80)

        return cleaned.strip()