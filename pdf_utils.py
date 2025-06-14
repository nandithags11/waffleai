import fitz # pymupdf

def extract_text_from_pdf(pdf_path) -> tuple[str,list[str]]:

    """
    Extracts text from a PDF file and returns it along with the list of images found.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        tuple[str, list[str]]: A tuple containing the extracted text and a list of image links.
    """
    doc = fitz.open(stream=pdf_path.read(), filetype="pdf")
    news_chunks = ""
    image_data= []

    for page_number, page in enumerate(doc):
        text_blocks = page.get_text("blocks")  # returns: (x0, y0, x1, y1, "text", block_no, block_type)
        images = page.get_images(full=True)

        # Group text by vertical alignment into chunks
        for block in text_blocks:
            x0, y0, x1, y1, text, *_ = block
            if text.strip():
                news_chunks.append({
                    "page": page_number + 1,
                    "bbox": (x0, y0, x1, y1),
                    "text": text.strip()
                })

        # Extract image metadata
        for idx, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            name = f"Page-{page_number+1}-Img-{idx+1}"
            news_chunks.append({
                "page": page_number + 1,
                "xref": xref,
                "name": name,
                "bbox": img[1],  # image bbox (x, y, width, height)
            })

    doc.close()
    return news_chunks, image_data


def assign_images_to_chunks(news_chunks, image_data):
    assigned = []

    for chunk in news_chunks:
        chunk_images = []
        cx0, cy0, cx1, cy1 = chunk['bbox']
        cpage = chunk['page']

        for img in image_data:
            if img["page"] != cpage:
                continue

            ix, iy, iw, ih = img["bbox"]
            # Simple overlap check or vertical closeness
            if abs(iy - cy1) < 100 or (ix >= cx0 and ix <= cx1):
                chunk_images.append(img["name"])

        assigned.append({
            "text": chunk["text"],
            "page": chunk["page"],
            "images": chunk_images
        })

    return assigned

