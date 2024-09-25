# SlangMachine
Brought to you by MateoHacks's Team Tomatoes

## Break barriers, translate slang

Our project is an AI-enhanced language translator that can translate between 20 different languages while taking literary aspects like slang, idioms, and subtext into account. Our slang translator works to bridge the generational gap by translating slang with the help of Urban Dictionary's API, a revolutionary platform that hosts up-to-date definitions of informal English terms. 

# Prerequisites
- OpenAI API Key ([Get One Here](https://platform.openai.com/api-keys))

# Dependencies
- Flask (tested on 3.0.2)
- PyEnchant (tested on 3.2.2)

`pip install pyenchant flask`

<details>
<summary>Note: For users who require the 'enchant' C library for PyEnchant</summary>
<br>
<ul>
   <li>Linux Users: Install the <code>libenchant-2-2</code> package (or similar naming) from your Linux package manager: <code>sudo apt install libenchant-2-2</code></li>
   <li>MacOS Users: Install the <code>enchant</code> package using HomeBrew: <code>brew update && brew install enchant</code></li>
   <li>Windows Users (If you want more than English): You need to install PyEnchant on a Linux platform (WSL works) or use MinGW
      <ul>
         <li>For WSL users, you can follow the instructions for Linux and install the appropriate package</li>
         <li>For MinGW (from MSYS2) users, install the wheel of PyEnchant without the binary</li>
         <ul>
            <li><code>pip install --no-binary pyenchant</code></li>
            <li>Install the appropriate packages for PyEnchant using MSYS2's package manager <code>pacman</code></li>
            <li><code>pacman -S enchant</code></li>
         </ul>
      </ul>
   </li>
</ul>
</details>


# Steps to Run
 1. Download the latest source code in the [Releases](https://github.com/nima-bhavansikar/mateohacks-project-team-tomatoes/releases) section
 2. Unzip the source code and open the folder in your favorite code editor
 3. Install the required dependencies for the project listed above
 4. Set your `OPENAI_API_KEY` environment variable to your api key as a string
    1. Windows Powershell: `$Env:OPENAI_API_KEY='YOUR_API_KEY_HERE'`
    2. Windows Cmd: `set OPENAI_API_KEY='YOUR_API_KEY_HERE'`
    3. macOS/Linux: `export OPENAI_API_KEY='YOUR_API_KEY_HERE'`
 5. Run the `app.py` file with your Python interpreter and visit `127.0.0.1:8080` to see the web app
