import logging

import pandas as pd
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

logger = logging.getLogger(__name__)


def create_response(bucket, files, counter, pdf_output=False, store_csv=False):
    logger.info("Creating DataFrame")
    df = pd.DataFrame.from_dict(counter, orient="index").reset_index()
    df.columns = ["Word", "Count"]
    df = df.sort_values("Count", ascending=False)
    df = df.reset_index()
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.html")
    file_list = f"{','.join(files[:-1])} and {files[-1]}"
    template_vars = {
        "title": "Words Count",
        "files": file_list,
        "bucket": bucket,
        "words_counter_table": df.to_html(),
    }
    logger.info("Rendering html template")
    html_out = template.render(template_vars)
    if pdf_output:
        logger.info("Creating pdf report")
        HTML(string=html_out).write_pdf("report.pdf")
    if store_csv:
        logger.info("Creating csv report")
        df.to_csv("report.csv")
    logger.info("Creating html report")
    with open("report.html", "w") as f:
        f.write(html_out)
