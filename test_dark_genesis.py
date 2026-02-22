import time
import webbrowser
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import pytest


class TestReporter:
    """Tracks test results and generates beautiful HTML report"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.steps = []
        self.test_name = "Dark Genesis Automation Test"
        self.status = "RUNNING"
        
    def add_step(self, step_name, status, details="", duration=0):
        """Add a test step"""
        self.steps.append({
            'name': step_name,
            'status': status,  # PASS, FAIL, RUNNING
            'details': details,
            'duration': duration,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
    
    def set_final_status(self, status):
        """Set overall test status"""
        self.status = status
        
    def generate_html_report(self):
        """Generate beautiful Dark Genesis-themed HTML report"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        passed = sum(1 for s in self.steps if s['status'] == 'PASS')
        failed = sum(1 for s in self.steps if s['status'] == 'FAIL')
        total = len(self.steps)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dark Genesis - Test Report</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Cormorant+Garamond:wght@300;400;600&display=swap');
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Cormorant Garamond', serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0a0f 50%, #0f0a1a 100%);
            color: #e0e0e0;
            padding: 40px 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 2px solid rgba(139, 0, 0, 0.3);
        }}
        
        .header h1 {{
            font-family: 'Cinzel', serif;
            font-size: 3rem;
            color: #8b0000;
            text-shadow: 0 0 20px rgba(139, 0, 0, 0.8);
            margin-bottom: 10px;
            animation: glow 2s ease-in-out infinite;
        }}
        
        @keyframes glow {{
            0%, 100% {{ text-shadow: 0 0 20px rgba(139, 0, 0, 0.8), 0 0 40px rgba(139, 0, 0, 0.4); }}
            50% {{ text-shadow: 0 0 30px rgba(139, 0, 0, 1), 0 0 60px rgba(139, 0, 0, 0.6); }}
        }}
        
        .header h2 {{
            font-family: 'Cinzel', serif;
            color: #999;
            font-size: 1.5rem;
            font-weight: 400;
        }}
        
        .summary {{
            background: rgba(20, 10, 15, 0.8);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(139, 0, 0, 0.4);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .summary-item {{
            background: rgba(0, 0, 0, 0.5);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(139, 0, 0, 0.3);
            text-align: center;
        }}
        
        .summary-item h3 {{
            font-family: 'Cinzel', serif;
            color: #8b0000;
            font-size: 0.9rem;
            text-transform: uppercase;
            margin-bottom: 10px;
            letter-spacing: 0.1rem;
        }}
        
        .summary-item p {{
            font-size: 2rem;
            font-weight: 600;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 8px 20px;
            border-radius: 5px;
            font-family: 'Cinzel', serif;
            font-size: 1.2rem;
            text-transform: uppercase;
            letter-spacing: 0.15rem;
            margin-top: 10px;
        }}
        
        .status-pass {{
            background: rgba(0, 200, 0, 0.2);
            color: #00ff00;
            border: 2px solid #00ff00;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
        }}
        
        .status-fail {{
            background: rgba(200, 0, 0, 0.2);
            color: #ff0000;
            border: 2px solid #ff0000;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
        }}
        
        .steps {{
            background: rgba(20, 10, 15, 0.8);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(139, 0, 0, 0.4);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
        }}
        
        .steps h2 {{
            font-family: 'Cinzel', serif;
            color: #8b0000;
            font-size: 2rem;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 0.15rem;
        }}
        
        .step {{
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(139, 0, 0, 0.3);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }}
        
        .step:hover {{
            border-color: rgba(139, 0, 0, 0.6);
            box-shadow: 0 5px 20px rgba(139, 0, 0, 0.3);
        }}
        
        .step-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .step-name {{
            font-size: 1.3rem;
            font-weight: 600;
            color: #e0e0e0;
        }}
        
        .step-status {{
            padding: 5px 15px;
            border-radius: 5px;
            font-family: 'Cinzel', serif;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.1rem;
        }}
        
        .step-pass {{
            background: rgba(0, 200, 0, 0.2);
            color: #00ff00;
            border: 1px solid #00ff00;
        }}
        
        .step-fail {{
            background: rgba(200, 0, 0, 0.2);
            color: #ff0000;
            border: 1px solid #ff0000;
        }}
        
        .step-details {{
            color: #999;
            font-size: 1rem;
            margin-top: 10px;
            line-height: 1.6;
        }}
        
        .step-meta {{
            display: flex;
            gap: 20px;
            margin-top: 10px;
            font-size: 0.9rem;
            color: #666;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(139, 0, 0, 0.2);
            color: #666;
            font-size: 0.9rem;
        }}
        
        .pass-count {{ color: #00ff00; }}
        .fail-count {{ color: #ff0000; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>DARK GENESIS</h1>
            <h2>Automation Test Report</h2>
        </div>
        
        <div class="summary">
            <div class="summary-grid">
                <div class="summary-item">
                    <h3>Test Status</h3>
                    <p><span class="status-badge status-{self.status.lower()}">{self.status}</span></p>
                </div>
                <div class="summary-item">
                    <h3>Total Steps</h3>
                    <p>{total}</p>
                </div>
                <div class="summary-item">
                    <h3>Passed</h3>
                    <p class="pass-count">{passed}</p>
                </div>
                <div class="summary-item">
                    <h3>Failed</h3>
                    <p class="fail-count">{failed}</p>
                </div>
                <div class="summary-item">
                    <h3>Duration</h3>
                    <p>{duration:.1f}s</p>
                </div>
                <div class="summary-item">
                    <h3>Start Time</h3>
                    <p>{self.start_time.strftime("%H:%M:%S")}</p>
                </div>
            </div>
        </div>
        
        <div class="steps">
            <h2>Test Steps</h2>
"""
        
        for i, step in enumerate(self.steps, 1):
            status_class = 'step-pass' if step['status'] == 'PASS' else 'step-fail'
            html += f"""
            <div class="step">
                <div class="step-header">
                    <div class="step-name">{i}. {step['name']}</div>
                    <div class="step-status {status_class}">{step['status']}</div>
                </div>
                {f'<div class="step-details">{step["details"]}</div>' if step['details'] else ''}
                <div class="step-meta">
                    <span>⏱️ {step['timestamp']}</span>
                    {f'<span>⌛ {step["duration"]:.1f}s</span>' if step['duration'] > 0 else ''}
                </div>
            </div>
"""
        
        html += f"""
        </div>
        
        <div class="footer">
            <p>Generated on {end_time.strftime("%B %d, %Y at %H:%M:%S")}</p>
            <p>Dark Genesis Automation Framework v1.0</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Save report
        report_path = Path("dark_genesis_test_report.html")
        report_path.write_text(html, encoding='utf-8')
        
        print(f"\n📄 Test report generated: {report_path.absolute()}")
        
        # Open in browser
        webbrowser.open(f"file://{report_path.absolute()}")
        
        return str(report_path.absolute())


class TestDarkGenesis:
    """Dark Genesis - Automated Demo Test"""
    
    def inject_highlight_styles(self):
        """Inject bright highlighting for demo visibility"""
        highlight_css = """
        .automation-highlight {
            outline: 5px solid #00ff00 !important;
            outline-offset: 5px !important;
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.9) !important;
            position: relative !important;
            z-index: 9999 !important;
            animation: pulse-glow 1s ease-in-out infinite !important;
        }
        
        @keyframes pulse-glow {
            0%, 100% { 
                outline-color: #00ff00; 
                box-shadow: 0 0 30px rgba(0, 255, 0, 0.9);
            }
            50% { 
                outline-color: #00ff00; 
                box-shadow: 0 0 50px rgba(0, 255, 0, 1);
            }
        }
        """
        self.driver.execute_script(f"""
            var style = document.createElement('style');
            style.textContent = `{highlight_css}`;
            document.head.appendChild(style);
        """)
    
    def highlight_and_click(self, element, label="Element", pause=0.6):
        """Highlight element, click it, then remove highlight - FASTER"""
        print(f"🖱️  Clicking: {label}")
        
        # Scroll to element
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )
        time.sleep(0.3)
        
        # Add highlight
        self.driver.execute_script(
            "arguments[0].classList.add('automation-highlight');",
            element
        )
        time.sleep(0.7)  # Faster highlight
        
        # Click
        element.click()
        time.sleep(pause)
        
        # Remove highlight
        self.driver.execute_script(
            "arguments[0].classList.remove('automation-highlight');",
            element
        )
    
    def scroll_to_top(self, pause=1.0):
        """Smooth scroll to top - FASTER"""
        print("⬆️  Scrolling to TOP...")
        self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
        time.sleep(pause)
    
    def scroll_to_bottom(self, pause=1.0):
        """Smooth scroll to bottom - FASTER"""
        print("⬇️  Scrolling to BOTTOM...")
        self.driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        time.sleep(pause)
    
    def wait_for_image_generation(self, timeout=120):
        """Wait for AI image to be fully generated - STRICT VERSION"""
        print(f"🖼️  Waiting for AI image to generate (max {timeout} seconds)...")
        print("   Please wait - AI is creating your creature image...\n")
        
        try:
            result_image = self.wait.until(
                EC.presence_of_element_located((By.ID, "result-image"))
            )
            
            # Wait for image src to contain actual data
            start_time = time.time()
            last_update = 0
            
            while time.time() - start_time < timeout:
                img_src = result_image.get_attribute('src')
                elapsed = int(time.time() - start_time)
                
                # Check if it's a real image (data URI or valid URL with substantial length)
                if img_src and len(img_src) > 500:
                    # Additional check: not just placeholder
                    if 'data:image' in img_src or 'pollinations.ai' in img_src or 'huggingface' in img_src or 'blob:' in img_src:
                        print(f"✅ Image generated successfully! (took {elapsed}s)")
                        print(f"   Image source type: {img_src[:50]}...")
                        print("\n📖 Displaying creature for viewing...")
                        print("   - View the generated image")
                        print("   - Read the biography")
                        print("\n⏱️  Pausing for 8 seconds to view creature...\n")
                        
                        # Count down so user knows what's happening
                        for i in range(8, 0, -1):
                            print(f"   {i} seconds remaining...")
                            time.sleep(1)
                        
                        print()
                        return True, elapsed
                
                # Show progress every 5 seconds
                if elapsed - last_update >= 5 and elapsed > 0:
                    print(f"   ⏳ Still generating... ({elapsed}s elapsed)")
                    last_update = elapsed
                
                time.sleep(1)
            
            # TIMEOUT - This is actually a FAILURE
            print("❌ IMAGE GENERATION FAILED - TIMEOUT!")
            print(f"   Waited {timeout} seconds but image never loaded")
            return False, timeout
            
        except Exception as e:
            print(f"❌ IMAGE GENERATION ERROR: {str(e)}")
            return False, 0
    
    def handle_download_alert(self):
        """Handle the download confirmation alert - ROBUST VERSION"""
        try:
            print("📢 Waiting for download alert...")
            # Wait up to 10 seconds for alert
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            
            # Switch to alert
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            
            print(f"   ✅ Alert found!")
            print(f"   📝 Alert message: {alert_text}")
            
            # Accept the alert
            alert.accept()
            print("   ✅ Alert accepted!")
            
            # Wait a moment for alert to close
            time.sleep(1.5)
            
            return True, alert_text
            
        except TimeoutException:
            print("   ℹ️  No alert appeared (this might be okay)")
            return False, "No alert"
        except Exception as e:
            print(f"   ⚠️  Alert handling error: {str(e)}")
            # Try to accept any alert that might be present
            try:
                self.driver.switch_to.alert.accept()
                time.sleep(1)
            except:
                pass
            return False, str(e)
    
    def test_complete_dark_genesis_demo(self):
        """
        COMPLETE DARK GENESIS DEMONSTRATION
        - Highlights all interactions
        - Waits for AI image generation
        - Downloads creature card
        - Generates beautiful HTML test report
        """
        
        # Initialize reporter
        reporter = TestReporter()
        
        # Setup browser
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 60)
        
        self.driver.get("https://ryanwdurham.github.io/Dark-Genesis/")
        self.inject_highlight_styles()
        
        try:
            print("\n" + "="*70)
            print("DARK GENESIS - AUTOMATED DEMONSTRATION")
            print("="*70 + "\n")
            
            # STEP 1: Start Creating
            step_start = time.time()
            print("📍 STEP 1: Click 'Start Creating'\n")
            time.sleep(1.5)
            
            try:
                start_btn = self.wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "start-btn"))
                )
                self.highlight_and_click(start_btn, "Start Creating Button", pause=1.0)
                
                self.wait.until(EC.visibility_of_element_located((By.ID, "creator")))
                print("✅ Creator page loaded\n")
                time.sleep(0.5)
                
                reporter.add_step(
                    "Click Start Creating",
                    "PASS",
                    "Successfully navigated to creator page",
                    time.time() - step_start
                )
            except Exception as e:
                reporter.add_step("Click Start Creating", "FAIL", str(e))
                raise
            
            # STEP 2: Roll ALL Traits
            step_start = time.time()
            print("📍 STEP 2: Rolling ALL Traits\n")
            
            try:
                trait_sections = self.driver.find_elements(By.CLASS_NAME, "trait-section")
                print(f"   Found {len(trait_sections)} traits to roll\n")
                
                for i, section in enumerate(trait_sections, 1):
                    roll_btn = section.find_element(By.CLASS_NAME, "roll-btn")
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                        roll_btn
                    )
                    time.sleep(0.2)
                    self.highlight_and_click(roll_btn, f"Trait {i} Roll Button", pause=0.5)
                
                print("✅ All traits rolled!\n")
                time.sleep(0.5)
                
                reporter.add_step(
                    "Roll All Traits",
                    "PASS",
                    f"Successfully rolled all {len(trait_sections)} traits",
                    time.time() - step_start
                )
            except Exception as e:
                reporter.add_step("Roll All Traits", "FAIL", str(e))
                raise
            
            # STEP 3: Generate Creature Name
            step_start = time.time()
            print("📍 STEP 3: Generate Creature Name\n")
            
            try:
                self.scroll_to_top(pause=1.0)
                
                name_input = self.driver.find_element(By.ID, "creature-name-input")
                name_section = name_input.find_element(By.XPATH, "../..")
                generate_btn = name_section.find_element(By.XPATH, ".//button[contains(text(), 'Generate')]")
                
                generated_names = []
                for i in range(3):
                    self.highlight_and_click(generate_btn, f"Generate Name (click {i+1})", pause=0.4)
                    generated_name = name_input.get_attribute('value')
                    generated_names.append(generated_name)
                    print(f"   Generated: {generated_name}\n")
                
                time.sleep(0.5)
                
                reporter.add_step(
                    "Generate Creature Name",
                    "PASS",
                    f"Generated names: {', '.join(generated_names)}",
                    time.time() - step_start
                )
            except Exception as e:
                reporter.add_step("Generate Creature Name", "FAIL", str(e))
                raise
            
            # STEP 4: Click Create Creature
            step_start = time.time()
            print("📍 STEP 4: Create Creature\n")
            
            try:
                create_btn = self.driver.find_element(By.CLASS_NAME, "create-btn")
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    create_btn
                )
                time.sleep(0.7)
                
                self.highlight_and_click(create_btn, "Create Creature Button", pause=1.5)
                
                print("⏳ Waiting for result page to load...")
                self.wait.until(EC.visibility_of_element_located((By.ID, "result")))
                print("✅ Result page loaded!\n")
                
                reporter.add_step(
                    "Create Creature",
                    "PASS",
                    "Creature creation initiated successfully",
                    time.time() - step_start
                )
            except Exception as e:
                reporter.add_step("Create Creature", "FAIL", str(e))
                raise
            
            # STEP 5: Wait for Image - THIS MUST SUCCEED
            step_start = time.time()
            print("📍 STEP 5: View Generated Creature\n")
            
            try:
                print("📍 Scrolling to TOP to view image and biography...")
                self.scroll_to_top(pause=1.5)
                
                success, duration = self.wait_for_image_generation(timeout=120)
                
                if success:
                    reporter.add_step(
                        "Wait for AI Image Generation",
                        "PASS",
                        f"Image generated and displayed for viewing (generation took {duration}s)",
                        time.time() - step_start
                    )
                else:
                    # IMAGE FAILED - Mark as FAIL and stop test
                    reporter.add_step(
                        "Wait for AI Image Generation",
                        "FAIL",
                        f"Image generation failed or timed out after {duration}s",
                        time.time() - step_start
                    )
                    reporter.set_final_status("FAIL")
                    print("\n❌ TEST FAILED: Image did not generate!")
                    print("   Cannot proceed to download without image.\n")
                    raise Exception("Image generation failed - test cannot continue")
                    
            except Exception as e:
                reporter.add_step("Wait for AI Image Generation", "FAIL", str(e))
                reporter.set_final_status("FAIL")
                raise
            
            # STEP 6: Download Card
            step_start = time.time()
            print("\n📍 STEP 6: Download Creature Card\n")
            
            try:
                print("📍 Scrolling to BOTTOM to find Download button...")
                self.scroll_to_bottom(pause=2.0)
                
                print("🔍 Looking for Download Card button...")
                download_btn = self.wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH, 
                        "//div[@id='result']//button[contains(text(), 'Download')]"
                    ))
                )
                
                print("✅ Download button found!")
                
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    download_btn
                )
                time.sleep(1.0)
                
                self.highlight_and_click(download_btn, "Download Card Button", pause=2.0)
                
                alert_handled = self.handle_download_alert()
                
                print("✅ Download initiated!\n")
                
                reporter.add_step(
                    "Download Creature Card",
                    "PASS",
                    f"Download successful, alert handled: {alert_handled}",
                    time.time() - step_start
                )
            except Exception as e:
                reporter.add_step("Download Creature Card", "FAIL", str(e))
                print(f"❌ Download failed: {str(e)}\n")
            
            # Check if all steps passed
            all_passed = all(step['status'] == 'PASS' for step in reporter.steps)
            
            if all_passed and reporter.status != "FAIL":
                reporter.set_final_status("PASS")
                print("\n" + "="*70)
                print("✅ DEMONSTRATION COMPLETE - ALL TESTS PASSED!")
                print("="*70 + "\n")
            else:
                reporter.set_final_status("FAIL")
                print("\n" + "="*70)
                print("❌ DEMONSTRATION COMPLETE - SOME TESTS FAILED!")
                print("="*70 + "\n")
            
            print("Summary:")
            print("  ✅ Started creature creation")
            print("  ✅ Rolled all traits")
            print("  ✅ Generated creature name")
            print("  ✅ Created creature")
            
            if all_passed:
                print("  ✅ Waited for AI image to generate")
                print("  ✅ Viewed creature image and biography (8 seconds)")
                print("  ✅ Downloaded creature card")
                print("  ✅ Dismissed download popup")
            else:
                print("  ❌ Some steps failed - check report for details")
            print()
            
            # Keep browser open to view results
            print("Keeping browser open for 3 seconds...")
            time.sleep(3)
            
        except Exception as e:
            print(f"\n❌ TEST FAILED WITH ERROR: {str(e)}\n")
            reporter.set_final_status("FAIL")
            
            # Add error to report if not already added
            if not any(step['status'] == 'FAIL' for step in reporter.steps):
                reporter.add_step("Test Execution", "FAIL", f"Unexpected error: {str(e)}")
            
        finally:
            print("Closing browser...")
            self.driver.quit()
            print("✅ Demo complete!\n")
            
            # Generate and open report
            print("📊 Generating test report...")
            reporter.generate_html_report()
            print("✅ Report opened in browser!\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])