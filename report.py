import pandas as pd
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


def create_response(bucket, files, counter, pdf_output=False, store_csv=False):
    df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    df.columns = ['Word', 'Count']
    df = df.sort_values('Count', ascending=False)
    df = df.reset_index()
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("template.html")
    file_list = f"{','.join(files[:-1])} and {files[-1]}"
    template_vars = {
        "title": "Words Count",
        "files": file_list,
        "bucket": bucket,
        "words_counter_table": df.to_html(),
    }
    html_out = template.render(template_vars)
    if pdf_output:
        HTML(string=html_out).write_pdf("report.pdf")
    if store_csv:
        df.to_csv('report.csv')
    with open('report.html', 'w') as f:
        f.write(html_out)
