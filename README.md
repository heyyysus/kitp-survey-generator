# kitp-survey-generator

### Install Requirments
> pip3 install -r requirments.txt

### Install wkhtmltopdf (MacOS)
> brew install homebrew/cask/wkhtmltopdf

Homebrew is required to install `wkhtmltopdf`

### Database Configuration
1. Copy .env_SAMPLE to .env `cp .env_SAMPLE .env`
2. Edit the following to the appropriate database details: `DB_HOST, DB_USER, DB_PASS, DB_NAME`

### Running the Generator
> python3 main.py <PROGRAM_CODE>

Example: 
> python3 main.py brainlearn23

Output will appear in `out` directory