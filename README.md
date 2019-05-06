# CbLR Packet Capture Utility

## Introduction
Utility to capture packets remotely from a host and return.

## Getting Started
1.	Ensure Python 3, Pip, Git, and the git-credential-manager are installed
2.	Install pipenv (On Linux: `pip install pipenv`, on Windows: `python -m pip install pipenv`)
3.  Clone this repository (`git clone https://github.com/americansystems/cblr_packet_capture.git`)
4.  Open the cloned directory (`cd cblr_packet_capture`)
5.	Run `pipenv install`
6.  Run `pipenv shell`
7.  Add authentication token for CbAPI (run `cbapi-response configure` or see below)
8.	Run `./packet_capture.py [-s SECONDS] --hostname HOSTNAME`

## Using the Cap Converter
By default, the script will return a `.etl` file, which requires the [Microsoft Message Analyzer](https://www.microsoft.com/en-us/download/details.aspx?id=44226) to open. However, once the Microsoft Message Analyzer is installed, you can use the included `Convert-ETLtoCap.ps1` script to automate conversion to standard .cap files. This is only available in Windows, and there is no support for converting .etl to .cap in Linux at this time.

Flags:
* -InFile \<file-path>: Full path of file to convert
* [-OutFile] \<file-path>: Full path of output location. If not specified, defaults to \<InFile>.cap
* [-Overwrite]: Will overwrite the output file if it exists
* [-KeepOriginal]: Don't delete the .etl file after conversion


## Authenticating
If running `cbapi-response configure` does not work, you can manually create a credentials.response file at ~/.carbonblack/
Your credentials file is a flat text file conforming to INI format. Here is an example:

```
[default]
url=https://<your-server-url>
token=<api-token-goes-here>
ssl_verify=True
```

## Testing
This is largely untested in Windows, but it should all work without issue. If you experience any problems, feel free to open an issue/PR.

## Contribute
Any feedback or contributions are welcome through issues/pull requests. I will gladly accept all the help I can get!
