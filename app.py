from fastapi import FastAPI, Form, Response
import asyncio
from pyppeteer import launch
from starlette.responses import FileResponse

app = FastAPI()

import os
from datetime import datetime

# Assuming your FastAPI app code is here

async def take_screenshot(url):
 
    browser = await launch()
    page = await browser.newPage()

    # Navigate to the URL
    await page.goto(url)

    # Wait for JavaScript to load (adjust the wait time according to your needs)
    await page.waitFor(5000)

    # Directory where you want to save the PDFs
    pdf_dir = 'pdf_outputs'
    os.makedirs(pdf_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Generate a unique filename for each PDF
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(pdf_dir, filename)

    # Save the PDF to the specified path
    await page.pdf({
        'path': filepath,  # Specify the filepath here
        'format': 'A4',
        'printBackground': True,
        'margin': {
            'top': '1cm',
            'right': '1cm',
            'bottom': '1cm',
            'left': '1cm'
        }
    })

    await browser.close()
    return filepath  # Return the path to the saved PDF

@app.post('/generate_pdf')
async def generate_pdf(url: str = Form(...)):
    pdf_file_path = await take_screenshot(url)
    return FileResponse(path=pdf_file_path, media_type='application/pdf', filename=os.path.basename(pdf_file_path))