from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

@app.route('/')
def display_table():
    # Path to your CSV file
    file_path = r"C:\Users\Ev\Desktop\TRG Week 20\CryptoAnalysis.csv"
    
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)
    
    # Convert the dataframe to an HTML table
    html_table = df.to_html(classes='table table-striped', index=False)
    
    # HTML template with the table embedded
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Crypto Analysis</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="mb-4">Crypto Analysis</h1>
            {html_table}
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
