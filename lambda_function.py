import boto3
from PyPDF2 import PdfReader, PdfWriter
import logging
from urllib.parse import unquote_plus
import uuid

s3 = boto3.client('s3')

if len(logging.getLogger().handlers) > 0:
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context):
    for record in event.get('Records', []):
        # get the bucket and key
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        logging.info(f'Processing {key} in {bucket}.')
        # only process pdfs and not ones which have been landscaped already
        if key.lower().endswith('.pdf'):
            if not key.lower().endswith('_landscape.pdf'):
                identifier = uuid.uuid4()
                tmp_in = f'/tmp/{identifier}.pdf'
                tmp_out = f'/tmp/{identifier}_landscape.pdf'
                s3.download_file(bucket, key, tmp_in)
                reader = PdfReader(tmp_in)
                writer = PdfWriter()
                for page in reader.pages:
                    width = page.mediabox.right - page.mediabox.left
                    height = page.mediabox.top - page.mediabox.bottom
                    logging.info(f'height = {height}, width = {width}.')
                    if height > width:
                        logging.info('Performing rotation.')
                        page.rotate(90)
                    writer.add_page(page)
                writer.write(tmp_out)
                s3.upload_file(tmp_out, bucket, key.replace('.pdf', '_landscape.pdf'))
            else:
                logging.info(f'Skipping {key} - already processed.')
        else:
            logging.info(f'Skipping {key} - not a PDF.')