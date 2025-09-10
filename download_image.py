import requests
import os
from urllib.parse import urlparse
import hashlib

def calculate_file_hash(filepath):
    """Calculate SHA-256 hash of a file to check for duplicates."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def main():
    print("Ubuntu Image Collector: Uniting the Web!")
    print("Gather shared images with respect and community spirit\n")
    
    # Get multiple URLs from user
    urls_input = input("Please enter image URLs (comma-separated): ")
    urls = [url.strip() for url in urls_input.split(',')]
    
    # Create directory if it doesn't exist
    directory = "Fetched_Images"
    os.makedirs(directory, exist_ok=True)
    
    for url in urls:
        print(f"\nProcessing URL: {url}")
        try:
            # Fetch the image with timeout
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Check HTTP headers
            content_type = response.headers.get('content-type', '').lower()
            content_length = response.headers.get('content-length', None)
            
            # Safety precaution: Verify content type is an image
            if not content_type.startswith('image/'):
                print(f"✗ Warning: '{url}' does not point to an image (Content-Type: {content_type})")
                continue
            
            # Safety precaution: Limit file size (e.g., 10MB max)
            max_size = 10 * 1024 * 1024  # 10MB in bytes
            if content_length and int(content_length) > max_size:
                print(f"✗ Warning: '{url}' file too large ({content_length} bytes)")
                continue
            
            # Extract filename from URL or generate one
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = "downloaded_image.jpg"
            
            # Ensure appropriate extension
            if not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                if 'png' in content_type:
                    filename += ".png"
                elif 'gif' in content_type:
                    filename += ".gif"
                else:
                    filename += ".jpg"
            
            # Create filepath
            filepath = os.path.join(directory, filename)
            
            # Check for duplicates by content hash
            temp_filepath = filepath + '.temp'
            with open(temp_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Calculate hash of downloaded content
            new_hash = calculate_file_hash(temp_filepath)
            existing_files = [f for f in os.listdir(directory) if f != filename]
            is_duplicate = False
            for existing_file in existing_files:
                existing_filepath = os.path.join(directory, existing_file)
                if calculate_file_hash(existing_filepath) == new_hash:
                    print(f"✗ Warning: '{filename}' is a duplicate of existing file '{existing_file}'")
                    os.remove(temp_filepath)  # Delete temp file
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                os.rename(temp_filepath, filepath)  # Save file if not duplicate
                print(f"✓ Image captured: {filename}")
                print(f"✓ Stored in: {filepath}")
            else:
                continue
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection issue: {e}")
        except Exception as e:
            print(f"✗ Something went wrong: {e}")
    
    print("\nTogether we thrive, sharing the web's vibe!")

if __name__ == "__main__":
    main()
