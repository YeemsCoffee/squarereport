# Setup Guide - Square Cafe Report

## Prerequisites

1. **Python 3.8 or higher** installed on your computer
2. **Square Developer Account** with API access
3. **Square Access Token** and **Location IDs** from your Square account

## Step 1: Get Your Square API Credentials

### Access Token

1. Go to [Square Developer Dashboard](https://developer.squareup.com/apps)
2. Create a new application or select an existing one
3. Go to the "Credentials" tab
4. Copy your **Production Access Token** (starts with `EAA...`)
   - For testing, you can use the **Sandbox Access Token**

### Location IDs

1. In your Square Dashboard, go to "Locations"
2. Click on each location to see its details
3. The Location ID is in the URL or can be found in the location settings
4. You'll need the Location ID for each of your two cafes

**Quick way to get Location IDs using Python:**

```python
from square.client import Client

client = Client(access_token='YOUR_ACCESS_TOKEN', environment='production')
result = client.locations.list_locations()

if result.is_success():
    for location in result.body['locations']:
        print(f"Name: {location['name']}, ID: {location['id']}")
```

## Step 2: Install Dependencies

1. Open a terminal/command prompt
2. Navigate to the project directory:
   ```bash
   cd /path/to/squarereport
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Configure the Application

1. Copy the example configuration file:
   ```bash
   cp config.example.yaml config.yaml
   ```

2. Edit `config.yaml` with your information:
   ```yaml
   square:
     access_token: "YOUR_SQUARE_ACCESS_TOKEN"
     environment: "production"  # or "sandbox" for testing

     locations:
       - id: "YOUR_LOCATION_1_ID"
         name: "Downtown Cafe"
       - id: "YOUR_LOCATION_2_ID"
         name: "Uptown Cafe"

   timezone: "America/Los_Angeles"

   peak_hours:
     start: 11  # 11am
     end: 14    # 2pm
   ```

## Step 4: Run the Application

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Your default web browser will open automatically
   - If not, go to: http://localhost:8501

3. Use the application:
   - Select a location from the dropdown
   - Pick a date
   - Click "Generate Report"

## Packaging as Desktop App (Optional)

To create a standalone desktop application that doesn't require running commands:

### Option 1: Using PyInstaller (Recommended)

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create a launcher script `launcher.py`:
   ```python
   import os
   import sys
   from streamlit.web import cli as stcli

   if __name__ == '__main__':
       sys.argv = ["streamlit", "run", "app.py", "--server.headless", "true"]
       sys.exit(stcli.main())
   ```

3. Build the executable:
   ```bash
   pyinstaller --onefile --add-data "config.yaml:." --add-data "config.example.yaml:." launcher.py
   ```

4. The executable will be in the `dist/` folder

### Option 2: Create a Batch/Shell Script

**Windows (create `run_app.bat`):**
```batch
@echo off
streamlit run app.py
```

**Mac/Linux (create `run_app.sh`):**
```bash
#!/bin/bash
streamlit run app.py
```

Make it executable on Mac/Linux:
```bash
chmod +x run_app.sh
```

## Troubleshooting

### "Configuration file not found" error
- Make sure you created `config.yaml` from the example file
- Check that the file is in the same directory as `app.py`

### "Authentication error" or "Invalid access token"
- Verify your access token is correct
- Make sure you're using the right environment (production vs sandbox)
- Check that your token hasn't expired

### "No orders found"
- Verify the location ID is correct
- Check that there were actual orders on the selected date
- Ensure the date is not in the future

### API rate limiting
- Square has API rate limits
- If you hit the limit, wait a few minutes before trying again

## Support

For Square API issues:
- [Square API Documentation](https://developer.squareup.com/docs)
- [Square Developer Forum](https://developer.squareup.com/forums)

For application issues:
- Check the terminal/console for error messages
- Verify all dependencies are installed correctly
- Ensure Python version is 3.8 or higher

## Security Notes

- **NEVER** commit your `config.yaml` file with real credentials to version control
- Keep your Square access token secure
- Consider using environment variables for production deployments
- Use the sandbox environment for testing before going to production
