import os
import json
import timeit
from typing import Any
import xlsxwriter
from dotenv import load_dotenv
from loguru import logger
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import (
    AnalyzeDocumentRequest,
    AnalyzeResult,
    DocumentPage,
)

load_dotenv()

endpoint = os.getenv("DOC_INTELLIGENCE_ENDPOINT", "")
api_key = os.getenv("DOC_INTELLIGENCE_API_KEY", "")


def analyze_general_documents(
    input_file_location: str, output_content_format: str = "text", tables_output: bool = False
) -> AnalyzeResult:
    """
    Analyze a general document using Azure Document Intelligence.

    :param image_file_path: Path to the image file to be analyzed.
    """
    # Create a client
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(api_key)
    )
    with open(input_file_location, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            body=f,
            content_type="application/octet-stream",
            output_content_format=(
                "markdown" if output_content_format == "markdown" else "text"
            ),
        )
    result = poller.result()

    if tables_output:
        # If tables_output is True, analyze the tables and save to Excel
        analyze_general_documents_table_data_to_excel(
            result, input_file_location
        )
    return result


def analyze_general_documents_table_data_to_excel(result: Any, input_file_location: str):
    # replace the file extension with .xlsx
    output_dir_path = "output"
    file_name = os.path.splitext(os.path.basename(input_file_location))[0]
    # create the output file name with .xlsx extension
    excel_output_file_name = f"document_intelligence_{file_name}_tables.xlsx"

    workbook = xlsxwriter.Workbook(os.path.join(output_dir_path, excel_output_file_name))

    for table_idx, table in enumerate(result.tables):
        adj_row_idx = 0
        adj_col_idx = 0
        tbl_worksheet = workbook.add_worksheet(name=f"{file_name}_{table_idx + 1}")

        logger.info(
            "Table # {} has {} rows and {} columns".format(
                table_idx, table.row_count, table.column_count
            )
        )

        cell_content = ""
        for cell in table.cells:
            cell_content = cell.content
            cell_content = str(cell_content).replace(":unselected:", "")
            cell_content = str(cell_content).replace(":selected:", "")
            cell_content = cell_content.strip()

            row_idx = adj_row_idx + cell.row_index

            if cell.column_index > adj_col_idx:
                adj_col_idx = cell.column_index

            tbl_worksheet.write(row_idx, cell.column_index, cell_content)

        adj_row_idx = adj_row_idx + table.row_count + 1

    logger.info(os.path.join(output_dir_path, excel_output_file_name), ": Excel has been created.")
    workbook.close()


if __name__ == "__main__":
    timeit_start = timeit.default_timer()

    input_file_path = "input/sample.pdf"  # Replace with your image file path
    output_file_path = "output/document_intelligence_output.json"  # Path to save the result
    result = analyze_general_documents(input_file_path, tables_output=True)

    timeit_end = timeit.default_timer()
    logger.info(
        f"Finished processing {input_file_path} in {timeit_end - timeit_start:.2f} seconds."
    )

    json_string = json.dumps(result.as_dict(), indent=4)
    # Save result as json to file
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(json_string)
    logger.info(f"Result saved to {output_file_path}")