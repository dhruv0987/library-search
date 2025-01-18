import os
from pdf_process import process_pdf

def create_searchable_page(pdf_path, output_file="../website/index.html"):
    extracted_text = process_pdf(pdf_path)
    if extracted_text is None:
        print("Could not create webpage due to PDF processing failure.")
        return

    html_content_start = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Library Search</title>
        <style>
            body { font-family: sans-serif; }
            #search-box { margin-bottom: 20px; }
            #results { white-space: pre-line; }
        </style>
    </head>
    <body>
        <h1>Library Book Search</h1>
        <input type="text" id="search-box" placeholder="Enter keywords...">
        <button onclick="search()">Search</button>
        <div id="results">
    """
    html_content_end =  """</div>
    <script>
        function search() {
            const searchTerm = document.getElementById("search-box").value.toLowerCase();
            const resultsDiv = document.getElementById("results");
            const allText = `""" + extracted_text.replace('\n', '\\n') + """`.toLowerCase();
            if (!searchTerm) {
                resultsDiv.textContent = `""" + extracted_text + """`;
                return;
            }
            const searchRegex = new RegExp(searchTerm, 'g');
            let highlightedText = `""" + extracted_text + """`;
            
            
             let match;
                while ((match = searchRegex.exec(allText)) !== null) {
                let actualStartIndex = match.index;
                 let actualEndIndex = searchRegex.lastIndex;
                    highlightedText = highlightedText.substring(0, actualStartIndex) +
                       '<mark>' + highlightedText.substring(actualStartIndex, actualEndIndex) +
                       '</mark>' + highlightedText.substring(actualEndIndex);
                    // To prevent infinite loops when matching with empty string
                   searchRegex.lastIndex = actualEndIndex;
            }
            resultsDiv.innerHTML = highlightedText;

        }
    </script>
    </body>
    </html>
    """
    
    html_content = html_content_start + extracted_text + html_content_end


    with open(output_file, "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    create_searchable_page("../data/books.pdf")
    print("index.html created")