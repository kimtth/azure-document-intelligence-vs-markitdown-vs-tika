import os
import sys
import timeit
from loguru import logger
from markitdown import MarkItDown

# Add a console sink
# logger.add(sys.stderr, level="DEBUG")

timestamp_yyyymmdd_hhmm = timeit.default_timer()

# Add a file sink
# logger.add(f"log_.log", level="INFO")

md = MarkItDown(enable_plugins=False) # Set to True to enable plugins

input_file_path = "input/sample.pdf"  # Replace with your PDF file path
output_file_path = os.path.join("output", "markitdown_extracted_text.txt")

timeit_start = timeit.default_timer()

print(f"Processing {input_file_path}...")
logger.info(f"Processing {input_file_path}...")

result = md.convert(input_file_path)
contents = result.text_content # Extract the text content from the conversion result

with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(contents)

timeit_end = timeit.default_timer()
print(f"Finished processing {input_file_path} in {timeit_end - timeit_start:.2f} seconds.")

logger.info(f"Finished processing {input_file_path} in {timeit_end - timeit_start:.2f} seconds.")