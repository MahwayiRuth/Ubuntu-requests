Ubuntu Image Collector

🌍 Overview
The Ubuntu Image Collector is a Python script that downloads images from user-provided URLs, inspired by the Ubuntu philosophy of community, sharing, and respect. It supports batch downloading, ensures safety with content validation and size limits, prevents duplicates using SHA-256 hashing, and provides robust error handling.

✨ Features
1. Batch Downloading: Processes multiple comma-separated image URLs in one go.

2. File Management: Saves images to a Fetched_Images directory with proper filenames and extensions.

3. Safety Checks:
. Validates image content using Content-Type headers.
. Limits file size to 10MB to prevent resource overuse.
. Implements a 10-second timeout for HTTP requests.

4. Duplicate Prevention: Uses SHA-256 hashing to detect and skip duplicate images.

4. Error Handling: Gracefully handles HTTP errors, connection issues, and file errors.

5. Ubuntu Spirit: Embeds messages reflecting community and collaboration.