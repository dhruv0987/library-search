from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_sample_pdf(filename="books.pdf", num_books=100):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    for i in range(1, num_books + 1):
        title = f"Book Title {i}"
        author = f"Author {chr(65 + (i % 26))}"  # Cycle through A-Z
        isbn = f"ISBN-{100000000000 + i}"

        book_info = f"Title: {title}\nAuthor: {author}\nISBN: {isbn}\n\n"
        para = Paragraph(book_info, styles['Normal'])
        story.append(para)

    doc.build(story)

if __name__ == '__main__':
    generate_sample_pdf("../data/books.pdf")
    print("books.pdf generated in the data directory")