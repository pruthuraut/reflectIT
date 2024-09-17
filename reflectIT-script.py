import requests
import concurrent.futures
import argparse
from urllib.parse import urlparse, parse_qs, urlencode
import html

def check_reflection(url):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    
    for param, value in params.items():
        if 'FUZZ' in value[0]:
            test_value = f"reflectIT_{param}"
            new_params = params.copy()
            new_params[param] = [test_value]
            test_url = parsed_url._replace(query=urlencode(new_params, doseq=True)).geturl()
            
            try:
                response = requests.get(test_url)
                if test_value in response.text:
                    return test_url
            except requests.RequestException:
                pass
    
    return None

def process_urls(urls):
    reflected_urls = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(check_reflection, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            if result:
                reflected_urls.append(result)
    return reflected_urls

def save_to_file(urls, filename):
    with open(filename, 'w') as f:
        for url in urls:
            f.write(f"{url}\n")

def test_special_chars(urls):
    special_chars = ['<', '>', '"', "'", '/', '\\', '&', '(', ')', '[', ']', '{', '}', '=', ';', 'onload', 'onerror', 'onclick', '%3C', '%3E', '%22', '%27', '%2F', '%00']
    results = {}

    for url in urls:
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        
        for param in params:
            test_url = parsed_url._replace(query=urlencode({param: special_chars}, doseq=True)).geturl()
            try:
                response = requests.get(test_url)
                encoded_chars = [html.escape(char) for char in special_chars]
                reflected_chars = [char for char in encoded_chars if char in response.text]
                results[url] = {
                    'status_code': response.status_code,
                    'reflected_chars': reflected_chars
                }
            except requests.RequestException as e:
                results[url] = {'error': str(e)}
    
    return results

def main():
    parser = argparse.ArgumentParser(description="reflectIT: Check for reflected parameters in URLs")
    parser.add_argument("-u", "--url", help="Single URL to check")
    parser.add_argument("-f", "--file", help="File containing list of URLs")
    parser.add_argument("-o", "--output", help="Output file to save reflected URLs")
    args = parser.parse_args()

    urls = []
    if args.url:
        urls = [args.url]
    elif args.file:
        with open(args.file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    else:
        print("Please provide either a URL (-u) or a file with URLs (-f)")
        return

    print("Checking for reflected parameters...")
    reflected_urls = process_urls(urls)

    if reflected_urls:
        print("Reflected URLs found:")
        for url in reflected_urls:
            print(url)

        if args.output:
            save_to_file(reflected_urls, args.output)
            print(f"Reflected URLs saved to {args.output}")

        print("\nTesting special characters...")
        special_char_results = test_special_chars(reflected_urls)
        for url, result in special_char_results.items():
            print(f"\nURL: {url}")
            if 'error' in result:
                print(f"Error: {result['error']}")
            else:
                print(f"Status Code: {result['status_code']}")
                print(f"Reflected Characters: {', '.join(result['reflected_chars'])}")
    else:
        print("No reflected parameters found.")

if __name__ == "__main__":
    main()
