
def generate_html_report(df):
    html = f"""<html>
    <head><style>
        body {{ font-family: Arial; }}
        h1 {{ color: #2E86C1; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 8px 12px; border: 1px solid #ddd; text-align: center; }}
    </style></head>
    <body>
        <h1>📊 Report Ω Depot</h1>
        {df.to_html(index=False)}
    </body></html>"""
    return html
