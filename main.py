import re
from argparse import ArgumentParser
from collections import Counter

from google.cloud import storage

from constants import DEFAULT_BUCKET, DEFAULT_FILES, STOPCHARS
from report import create_response


def get_text_from_file(bucket_name, storage_file):
    storage_client = storage.Client.create_anonymous_client()
    bucket = storage_client.bucket(bucket_name="apache-beam-samples", user_project=None)
    blob = bucket.blob(storage_file)
    if not blob.exists():
        raise Exception(f"File {storage_file} not found in Google Storage")
    return blob.download_as_string()


def get_counter_from_file(bucket_name, storage_file, sensitive=False):
    text = get_text_from_file(bucket_name, storage_file)
    words = filter(None, re.split(STOPCHARS, text.decode("utf-8")))
    if not sensitive:
        words = (word.lower() for word in words)
    return Counter(words)


def main(bucket_name, files, sensitive=False, pdf_output=False, store_csv=False):
    words_counter = Counter([])
    for storage_file in files:
        words_counter += get_counter_from_file(
            bucket_name, storage_file, sensitive=sensitive
        )
    create_response(
        bucket_name, files, words_counter, pdf_output=pdf_output, store_csv=store_csv
    )


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Words counter for files in public google storage"
    )
    help_message = """
        List of files that will be processed if there are no files then 
        'shakespeare/kinglear.txt', 'shakespeare/othello.txt' and 
        'shakespeare/romeoandjuliet.txt will be used
    """
    parser.add_argument("files", metavar="files", nargs="*", help=help_message)

    parser.add_argument(
        "--bucket_name",
        dest="bucket_name",
        default=DEFAULT_BUCKET,
        help="Name of bucket",
    )
    parser.add_argument(
        "--sensitive", action="store_true", help="Sensitive case for words"
    )
    parser.add_argument("--pdf_report", action="store_true", help="Create pdf report")
    parser.add_argument(
        "--store_csv", action="store_true", help="Store csv with results"
    )

    args = parser.parse_args()
    if not args.files:
        args.files = DEFAULT_FILES
    main(
        args.bucket_name,
        args.files,
        sensitive=args.sensitive,
        pdf_output=args.pdf_report,
        store_csv=args.store_csv,
    )
