import os

def create_searchable_page(output_file="../website/index.html"):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Library Search</title>
        <link rel="stylesheet" href="style.css">
        <script src="upload.js"></script>
    </head>
    <body>
        <nav>
            <div class="container">
                <a href="#" class="logo">Library Search</a>
                <ul class="nav-links">
                    <li><a href="index.html">Search</a></li>
                    <li><a href="admin.html">Admin</a></li>
                </ul>
            </div>
        </nav>
        <div class="container">
            <h1>Welcome to the Library</h1>
            <input type="text" id="search-box" placeholder="Search books..." class="search-input">
            <button onclick="search()" class="search-button">Search</button>
            <div id="results" class="results-container"></div>
           
        </div>
        <script>
            function search() {
               
                const searchTerm = document.getElementById("search-box").value.toLowerCase();
                const resultsDiv = document.getElementById("results");

                // Retrieve text from local storage
                const allText = localStorage.getItem('processedText');
                if (!allText) {
                    resultsDiv.textContent = "No text available for search.";
                    return;
                }

                if (!searchTerm) {
                    resultsDiv.innerHTML = allText.replace(/\\n/g, '<br>');
                    return;
                }
                const searchRegex = new RegExp(searchTerm, 'g');
                let highlightedText = allText;
                let match;
                    while ((match = searchRegex.exec(allText.toLowerCase())) !== null) {
                    let actualStartIndex = match.index;
                    let actualEndIndex = searchRegex.lastIndex;
                        highlightedText = highlightedText.substring(0, actualStartIndex) +
                            '<mark>' + highlightedText.substring(actualStartIndex, actualEndIndex) +
                            '</mark>' + highlightedText.substring(actualEndIndex);
                    searchRegex.lastIndex = actualEndIndex;
                }
                resultsDiv.innerHTML = highlightedText.replace(/\\n/g, '<br>');
            }
        </script>
    </body>
    </html>
    """

    with open(output_file, "w") as f:
        f.write(html_content)
if __name__ == "__main__":
    create_searchable_page()
    print("index.html created")