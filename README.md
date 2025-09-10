Ubuntu Image Collector
Overview
The Ubuntu Image Collector is a Python script that downloads images from user-provided URLs, embodying the Ubuntu philosophy of community, sharing, and respect. It supports batch downloading, ensures safety through content validation and size limits, prevents duplicate files using SHA-256 hashing, and provides robust error handling.
Features
Batch Downloading: Processes multiple comma-separated image URLs in a single run.
File Management: Saves images to a Fetched_Images directory with proper filenames and extensions.
Safety Checks:
Validates URLs point to images using Content-Type headers.
Limits file size to 10MB to prevent resource overuse.
Implements a 10-second timeout for HTTP requests.
Duplicate Prevention: Uses SHA-256 hashing to detect and skip duplicate images.
Error Handling: Gracefully manages HTTP errors, connection issues, and file-related errors.
Ubuntu Philosophy: Incorporates messages reflecting community and collaboration.
Requirements
Python 3.x
Dependencies:
requests: For HTTP requests.
urllib.parse: For URL parsing.
hashlib: For file hashing.
os: For file and directory operations.