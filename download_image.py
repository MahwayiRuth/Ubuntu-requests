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
    """Main function to fetch and save images, embodying Ubuntu principles."""
    # Welcome message reflecting Ubuntu's community spirit
    print("Ubuntu Image Collector: Uniting the Web!")
    print("Gather shared images with respect and community spirit\n")
    
    # Prompt for multiple URLs (Challenge 1: Handle multiple URLs)
    urls_input = input("Please enter image URLs (comma-separated): ")
    urls = [url.strip() for url in urls_input.split(',')]
    
    # Create directory for storing images (Requirement: File management)
    directory = "Fetched_Images"
    os.makedirs(directory, exist_ok=True)
    
    for url in urls:
        print(f"\nProcessing URL: {url}")
        try:
            # Fetch image with timeout for safety (Challenge 2: Precautions)
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()  # Check for HTTP errors (Requirement: Error handling)
            
            # Check HTTP headers (Challenge 4: HTTP headers)
            content_type = response.headers.get('content-type', '').lower()
            content_length = response.headers.get('content-length', None)
            
            # Safety check: Ensure content is an image (Challenge 2)
            if not content_type.startswith('image/'):
                print(f"✗ Warning: '{url}' does not point to an image (Content-Type: {content_type})")
                continue
            
            # Safety check: Limit file size to 10MB (Challenge 2)
            max_size = 10 * 1024 * 1024  # 10MB in bytes
            if content_length and int(content_length) > max_size:
                print(f"✗ Warning: '{url}' file too large ({content_length} bytes)")
                continue
            
            # Extract filename from URL (Requirement: File management)
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = "downloaded_image.jpg"
            
            # Ensure appropriate image extension (Challenge 4)
            if not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                if 'png' in content_type:
                    filename += ".png"
                elif 'gif' in content_type:
                    filename += ".gif"
                else:
                    filename += ".jpg"
            
            # Define filepath for saving
            filepath = os.path.join(directory, filename)
            
            # Check for duplicates (Challenge 3: Prevent duplicates)
            temp_filepath = filepath + '.temp'
            with open(temp_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Compare hash to detect duplicates
            new_hash = calculate_file_hash(temp_filepath)
            existing_files = [f for f in os.listdir(directory) if f != filename]
            is_duplicate = False
            for existing_file in existing_files:
                existing_filepath = os.path.join(directory, existing_file)
                if calculate_file_hash(existing_filepath) == new_hash:
                    print(f"✗ Warning: '{filename}' is a duplicate of existing file '{existing_file}'")
                    os.remove(temp_filepath)
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                os.rename(temp_filepath, filepath)  # Save if not duplicate
                print(f"✓ Image captured: {filename}")
                print(f"✓ Stored in: {filepath}")
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection issue: {e}")
        except Exception as e:
            print(f"✗ Something went wrong: {e}")
    
    # Farewell message reflecting Ubuntu's sharing principle
    print("\nTogether we thrive, sharing the web's vibe!")

if __name__ == "__main__":
    main()