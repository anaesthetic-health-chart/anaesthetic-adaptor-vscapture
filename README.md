#anaesthetic-adaptor-vscapture

Adaptor to pass data captured data from the Datex S/5 anaesthetic monitor using
VSCapture into the anaesthetic health chart app.

This little Python script will open the passed CSV file containing the CSV
output from the VSCapture program, parse the data, and then pass it to the
anaesthetic health chart app using the REST API.

first:
```bash
pip install -r requirements.txt
```

```bash
Usage: %s <VSCAPTURE_CSV> <HEALTH_CHART_BASE_URL>
  <VSCAPTURE_CSV> The CSV file being written to by VSCapture
  <HEALTH_CHART_BASE_URL> Base URL of the health chart to send the data to
```

VSCapture, written by John George K. (@johngeorgedon), is a C# .NET app to
download or capture data from Datex AS3 S/5 Anesthesia monitors. It requires
Visual Studio 2010, .NET 4 or MonoDevelop to compile. Android version requires
Xamarin Studio, Android SDK to compile. Support for capture from other
monitors is planned in future.

This script is currently using the version of VSCapture that has been modified
by (@doismellburning) to include O2 ET and CO2 FI
(https://github.com/doismellburning/VSCapture).
