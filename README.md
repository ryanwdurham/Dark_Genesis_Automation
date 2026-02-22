# 🦇 Dark Genesis - Automation Testing Suite

## ✨ Features

Automates my Dark Genesis Creature Creator Application using Python, Selenium and Pytest.

- 🎯 **Visual Highlighting** - Green glowing borders show exactly what's being automated
- 📊 **Beautiful HTML Reports** - Dark Genesis-themed test reports with pass/fail status
- ⏱️ **Smart Waiting** - Intelligent waits for AI image generation (up to 2 minutes)
- 🎬 **Demo Mode** - Runs at a pace perfect for demonstrations
- 📝 **Detailed Logging** - Step-by-step console output with emojis
- 🔄 **Comprehensive Testing** - Tests all major user workflows



  Click here to see the automation in action:  https://www.loom.com/share/3371576527fc4a159d7e9d721d930b74
<br>



  Click here to see the test report with failure:  https://ryanwdurham.github.io/Dark_Genesis_Automation/dark_genesis_test_report.html 
<br>
## 🔧 Requirements

### Software Requirements

- **Python 3.12+** (or 3.11+)
- **Google Chrome** (latest version)
- **ChromeDriver** (compatible with your Chrome version)

### Python Packages

```
selenium>=4.0.0
pytest>=7.0.0
```



## 🎮 Test Flow

The automation performs the following steps:

### 1. **Start Creating** (2 seconds)
   - Opens Dark Genesis website
   - Clicks "Start Creating" button
   - Waits for creator page to load

### 2. **Roll All Traits** (~8 seconds)
   - Automatically finds all 8 trait sections:
     - Core Monster Category
     - Physical Features
     - Origin / Backstory
     - Powers & Abilities
     - Weaknesses / Vulnerabilities
     - Personality / Behavior
     - Setting / Domain
     - Signature / Trophy
   - Clicks "Roll" button for each trait (2x per trait)
   - Scrolls automatically to see all traits

### 3. **Generate Creature Name** (~3 seconds)
   - Scrolls to top where name input is
   - Clicks "Generate" button 3 times
   - Displays generated names in console

### 4. **Create Creature** (1-2 seconds)
   - Scrolls to "Create Creature" button
   - Clicks to initiate creation
   - Navigates to result page

### 5. **Wait for Image Generation** (10-120 seconds) ⚠️
   - **THIS STEP FAILS** - Image does NOT get created (FAIL)
   - Waits at top of page for AI image to generate
   - Shows progress updates every 5 seconds
   - Displays creature for 8 seconds once loaded

### 6. **Download Creature Card** (3-5 seconds)
   - Scrolls to bottom of result page
   - Clicks "Download Card" button
   - Handles browser alert/popup
   - Saves HTML file to Downloads folder

### 7. **Generate Test Report**
   - Creates beautiful HTML report
   - Auto-opens in default browser
   - Shows pass/fail for each step
   - Shows Failure of 

## ⚠️ Known Issues

### AI Image Generation Failure

**Issue:** The AI image generation step may fail or timeout after 120 seconds.

**Cause:** The application uses external AI image generation APIs (Hugging Face, Pollinations.ai) which now require API keys or have rate limits. Free tier access has been restricted.

**Impact:** 
- Test will mark "Wait for AI Image Generation" as **FAIL**
- Overall test status will be **FAIL**
- Download step may not execute (test stops if image fails)


### Browser Compatibility

- **Chrome Only:** Currently only tested with Google Chrome
- **ChromeDriver:** Must match your Chrome version
- Auto-updates may break compatibility

## 📊 Report Output

After each test run, an HTML report is generated:

```

### Report Features
- ✅ **Pass/Fail Status** for overall test
- 📈 **Summary Dashboard** with statistics
- 📝 **Step-by-Step Results** with timing
- 🎨 **Dark Genesis Theme** matching the app
- ⏱️ **Timestamps** for each action
- 📋 **Detailed Error Messages** when steps fail

### Report Opens Automatically
The report automatically opens in your default browser when the test completes.


## 📁 Project Structure

```
Dark_Genesis/
│
├── test_dark_genesis.py       # Main test file
├── dark_genesis_test_report.html   # Generated report (after test runs)
├── README.md                  # This file
│
└── index.html                 # Dark Genesis app (if local)
```

## 🎓 Understanding the Code

### Test Class: `TestDarkGenesis`

Main automation class containing:
- `inject_highlight_styles()` - Adds green glow CSS
- `highlight_and_click()` - Highlights and clicks elements
- `scroll_to_top/bottom()` - Page navigation
- `wait_for_image_generation()` - Smart image waiting
- `handle_download_alert()` - Alert management
- `test_complete_dark_genesis_demo()` - Main test flow


**Tested On:**
- Python 3.14.2
- Chrome 144.x
- Windows 10/11

---

### 🦇 *"Forge your nightmare. One test at a time."* 🦇
