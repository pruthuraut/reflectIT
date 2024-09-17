
# reflectIT

**reflectIT** is a Python-based tool designed to detect reflected parameters in URLs. It helps identify vulnerable endpoints where parameters are reflected in the HTML source, allowing for potential XSS (Cross-Site Scripting) attacks. Additionally, the tool tests for common special characters used in XSS attacks and reports how the server responds.

## Features

- Processes a list of URLs with parameters for reflected input.
- Option to pass a single URL or a file containing multiple URLs.
- Uses multithreading for faster results.
- Displays output URLs where the parameter value is reflected in the source code.
- Option to save reflected URLs to a file.
- Tests special characters typically used in XSS attacks.
- Reports the server's response to special characters, including status code and reflected characters.

## Installation

### Prerequisites

- Python 3.x
- `requests` library

You can install the required Python libraries with:

```bash
pip install requests
```

## Usage

### Basic Usage

To check for reflected parameters in a single URL, use the `-u` flag:

```bash
python reflectIT.py -u "http://example.com/?param=FUZZ"
```

To process multiple URLs from a file, use the `-f` flag:

```bash
python reflectIT.py -f urls.txt
```

The file should contain one URL per line, for example:

```
http://example.com/?param1=FUZZ&param2=value
http://testsite.com/?search=FUZZ
```

### Save Output

To save the reflected URLs to a file, use the `-o` flag:

```bash
python reflectIT.py -f urls.txt -o output.txt
```

### Special Characters Test

After detecting reflected parameters, the tool will automatically test for XSS by injecting the following special characters into the reflected parameters:

- `<`, `>`, `"`, `'`, `/`, `\\`, `&`, `(`, `)`, `[`, `]`, `{`, `}`, `=`, `;`
- Event handlers like `onload`, `onerror`, `onclick`
- URL-encoded variants: `%3C`, `%3E`, `%22`, `%27`, `%2F`
- Null byte: `%00`

The tool will report how the server handles these characters and display the status code and any reflected characters in the response.

## Examples

1. **Check a single URL**:

   ```bash
   python reflectIT.py -u "http://example.com/?param=FUZZ"
   ```

2. **Check URLs from a file**:

   ```bash
   python reflectIT.py -f urls.txt
   ```

3. **Save output to a file**:

   ```bash
   python reflectIT.py -f urls.txt -o output.txt
   ```

4. **Check and test special characters**:

   The script will automatically check for reflection and test special characters in reflected URLs. Here's an example of the output:

   ```
   URL: http://example.com/?param=FUZZ
   Status Code: 200
   Reflected Characters: <, >, "
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is intended for educational purposes only. Ensure you have proper authorization to test the URLs you target. Unauthorized penetration testing on websites may be illegal and violate the terms of service.
```
