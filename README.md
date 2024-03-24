# SlangMachine
brought to you by MateoHack's Team Tomatoes
## Break barriers, translate slang

Our project is an AI enhanced language translator that can translate between 20 different languages while taking literary aspects like slang, idioms, and subtext into account. Our slang translator works to bridge the generational gap by translating slang with the help of Urban Dictionary's API. 

# Prerequisites
- OpenAI API Key [Get One Here](https://platform.openai.com/api-keys)

# Dependencies
- Flask (tested on 3.0.2)
- PyEnchant (tested on 3.2.2)

`pip install pyenchant flask`

# Steps to Run
 1. Download the latest source code in the [Releases](https://github.com/nima-bhavansikar/mateohacks-project-team-tomatoes/releases) section
 2. Unzip the source code and open the folder in your favorite code editor
 3. Install the required dependencies for the project listed above
 4. Set your `OPENAI_API_KEY` environment variable to your api key as a string
    1. Windows Powershell: `$Env:OPENAI_API_KEY='YOUR_API_KEY_HERE'`
    2. Windows Cmd: `set OPENAI_API_KEY='YOUR_API_KEY_HERE'`
    3. macOS/Linux: `export OPENAI_API_KEY='YOUR_API_KEY_HERE'`
 5. Run the `app.py` file with your Python interpreter and visit `127.0.0.1:8080` to see the web app
