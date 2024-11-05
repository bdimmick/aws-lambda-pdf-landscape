import boto3
from PyPDF2 import PdfReader, PdfWriter
from urllib.parse import unquote_plus
import uuid

s3 = boto3.client('s3')


def lambda_handler(event, context):
    for record in event.get('Records', []):
        # get the bucket and key
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        # only process pdfs and not ones which have been landscaped already
        if key.lower().endswith('.pdf') and not key.lower().endswith('_landscape.pdf'):
            id = uuid.uuid4()
            tmp_in = f'/tmp/{id}.pdf'
            tmp_out = f'/tmp/{id}_landscape.pdf'
            s3.download_file(bucket, key, tmp_in)
            reader = PdfReader(tmp_in)
            writer = PdfWriter()
            for page in reader.pages:
                if page.mediaBox.bottom - page.mediaBox.top > page.mediaBox.right - page.mediaBox.left:
                    page.rotate(90)
                writer.add_page(page)
            writer.write(tmp_out)
            s3.upload_file(tmp_out, bucket, key.replace('.pdf', '_landscape.pdf'))