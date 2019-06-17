# CbLR Packet Capture Utility

## Introduction

Utility to capture packets remotely from a host and return. Support is now added for using Live Response through the PSC or Response. Multi-profile support is now available.

## Getting Started

1. Ensure Python 3, Pip, and Git are installed
2. Install pipenv (On Linux: `pip install pipenv`, on Windows: `python -m pip install pipenv`)
3. Clone this repository (`git clone https://github.com/americansystems/cblr_packet_capture.git`)
4. Open the cloned directory (`cd cblr_packet_capture`)
5. Run `pipenv install`
6. Run `pipenv shell`
7. Add authentication token for CbAPI (see Authenticating section below)
8. Run `./packet_capture.py [-s SECONDS] [--profile PROFILE] --hostname HOSTNAME`

## Using the Cap Converter

By default, the script will return an `.etl` file, which requires the [Microsoft Message Analyzer](https://www.microsoft.com/en-us/download/details.aspx?id=44226) to open. However, once the Microsoft Message Analyzer is installed, you can use the included `Convert-ETLtoCap.ps1` script to automate conversion to standard .cap files. This is only available on Windows, and there is no support for converting .etl to .cap on Linux at this time.

Flags:

* -InFile \<file-path>: Path of file to convert
* [-OutFile] \<file-path>: Path of output location. If not specified, defaults to \<InFile>.cap
* [-Overwrite]: Will overwrite the output file if it exists
* [-KeepOriginal]: Don't delete the .etl file after conversion

## Authenticating

### Response

After entering the virtual environment (step 6 from Getting Started), run `cbapi-response configure` and enter the requested information.

If running `cbapi-response configure` does not work, you can manually create a credentials.response file at ~/.carbonblack/
Your credentials file is a flat text file conforming to INI format. Here is an example:

```INI
[default]
url = https://<your-server-url>
token = <api-token-goes-here>
ssl_verify = True
```

### PSC

After entering the virtual environment (step 6 from Getting Started), run `cbapi-defense configure`. Then, copy the created file from `~/.carbonblack/credentials.defense` to `~/.carbonblack/credentials.psc`.

If the above steps don't work, you can manually reated a credentials.psc file at ~/.carbonblack/
Your credentials file is a flat text file conforming to INI format. Here is an example:

```INI
[default]
url = https://api-prod05.conferdeploy.net
token = <API-KEY>/<API-ID>
ssl_verify = True
```

## Contribute

Any feedback or contributions are welcome through issues/pull requests. I will gladly accept all the help I can get!
