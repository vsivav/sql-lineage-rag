"""
Metadata Generator

Converts LineageResult into ProcedureMetadata.
"""

from __future__ import annotations

from src.metadata.schema import (
    ProcedureMetadata,
    ColumnMetadata,
)


class MetadataGenerator:

    def generate(
        self,
        procedure_name: str,
        lineage_result,
    ) -> ProcedureMetadata:

        metadata = ProcedureMetadata(
            procedure_name=procedure_name
        )

        #
        # Source tables
        #
        metadata.source_tables = sorted({

            r.source_table

            for r in lineage_result.table_relationships

        })

        #
        # Target tables
        #
        metadata.target_tables = sorted({

            r.target_table

            for r in lineage_result.table_relationships

        })

        #
        # Functions
        #
        metadata.functions = sorted({

            f.name

            for f in lineage_result.functions

        })

        #
        # Column mappings
        #
        for item in lineage_result.column_lineage:

            metadata.columns.append(

                ColumnMetadata(

                    target_column=item.target_column,

                    source_columns=[
                        f"{item.source_table}.{item.source_column}"
                    ],

                    transformation=item.expression

                )

            )

        return metadata
