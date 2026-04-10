#!/usr/bin/env python3
import os
import subprocess
import argparse
import re
import requests
from urllib.parse import urlparse, urljoin

def sanitize_folder_name(url):
    """Converts a URL into a safe directory name."""
    parsed = urlparse(url)
    # Combine netloc and path, replace non-alphanumeric with undersrcore
    name = f"{parsed.netloc}{parsed.path}"
    name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    # Remove trailing/leading underscores
    name = name.strip('_')
    return name if name else "cloned_page"
def create_root_redirect(target_path, urls):
    """Creates a root index.html that redirects to the primary site entry point."""
    if not urls:
        return
    
    # Use the first URL as the primary entry point
    parsed = urlparse(urls[0])
    host = parsed.netloc
    path = parsed.path.strip("/")
    
    # Wget with -E will save as .html even if original path doesn't have it
    # We try to guess the local path wget created
    if not path:
        entry_file = f"{host}/index.html"
    else:
        # If path is 'about', wget creates 'about/index.html'
        entry_file = f"{host}/{path}/index.html"
    
    # If the exact path doesn't exist, try just the index in host root
    if not os.path.exists(os.path.join(target_path, entry_file)):
        entry_file = f"{host}/index.html"

    redirect_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url={entry_file}">
    <title>Redirecting to {host}</title>
    <style>
        body {{ font-family: sans-serif; text-align: center; padding: 50px; background: #f4f4f4; }}
        .card {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }}
        a {{ color: #007bff; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="card">
        <h2>Project: {host}</h2>
        <p>Your clone is ready. If you are not redirected automatically,</p>
        <p><a href="{entry_file}">Click here to open the homepage</a></p>
    </div>
</body>
</html>
"""
    with open(os.path.join(target_path, "index.html"), "w") as f:
        f.write(redirect_html)
    print(f"[+] Root redirect created: {os.path.join(target_path, 'index.html')}")

def discover_and_download_chunks(target_path):
    """
    Scans JS files for hidden bundle names and downloads them.
    Capped at 200 attempts per JS file to prevent hanging on large bundles.
    """
    print(f"[*] Starting Deep Mirroring (Scavenging hidden chunks)...")
    
    # Pattern 1: Literal filenames (e.g. "path/to/chunk.hash.js")
    literal_pattern = re.compile(r'([a-zA-Z0-9\-_.]+\.[a-f0-9]{20,32}\.(js|css))')
    
    # Pattern 2: Webpack mappings (e.g. 45035:"f42cc55a90c9884121e5")
    # Only generate ID.hash.js/css — not speculative bare hash.js/hash.css
    mapping_pattern = re.compile(r'([0-9]{2,7}):"([a-f0-9]{20,32})"')
    
    MAX_ATTEMPTS_PER_FILE = 200  # Safety cap to prevent hanging
    downloaded_count = 0
    
    # Determine the project root
    if any(os.path.isdir(os.path.join(target_path, d)) for d in os.listdir(target_path) if '.' in d):
        project_root = target_path
    else:
        project_root = os.path.dirname(target_path)

    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(".js"):
                file_path = os.path.join(root, file)
                rel_to_root = os.path.relpath(root, project_root)
                host = rel_to_root.split(os.sep)[0]
                if '.' not in host: continue
                
                base_url = f"https://{host}/"
                
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    found_files = []
                    
                    # Search literals
                    for m in literal_pattern.findall(content):
                        found_files.append(m[0].lstrip('.'))
                        
                    # Search mappings — only generate ID.hash format (most likely to exist)
                    for m in mapping_pattern.findall(content):
                        cid, chash = m
                        found_files.append(f"{cid}.{chash}.js")
                        found_files.append(f"{cid}.{chash}.css")

                    if not found_files: continue
                    
                    # Deduplicate and cap
                    found_files = list(set(found_files))[:MAX_ATTEMPTS_PER_FILE]
                    
                    for chunk_name in found_files:
                        local_chunk_path = os.path.join(root, chunk_name)
                        
                        if not os.path.exists(local_chunk_path):
                            host_root_path = os.path.join(project_root, host)
                            rel_dir_from_host = os.path.relpath(root, host_root_path)
                            if rel_dir_from_host == ".": rel_dir_from_host = ""
                            
                            remote_url = urljoin(base_url, os.path.join(rel_dir_from_host, chunk_name))
                            
                            try:
                                r = requests.get(remote_url, timeout=1.5)
                                if r.status_code == 200:
                                    with open(local_chunk_path, "wb") as cf:
                                        cf.write(r.content)
                                    downloaded_count += 1
                            except Exception:
                                pass
                except Exception as e:
                    print(f"  [!] Scan error in {file}: {e}")
                    
    print(f"[+] Deep Mirroring complete. Downloaded {downloaded_count} hidden assets.")


def inject_stability_script(target_path):
    """
    Injects The Freezer (v7) shield.
    Paralyzes all JS execution after 5 seconds to lock the rendered UI in place.
    """
    print(f"[*] Injecting UI Freezer Shield (v7) into HTML files...")
    
    stability_js = """
    <script id="clonescript-stability">
    (function() {
        console.log("[Clonescript] Freezer Shield v7 active. UI will be paralyzed in 5 seconds.");
        
        // 1. Initial Protection (from v6)
        const isMajorElement = (el) => {
            if (!el) return false;
            return el === document.body || el.id === 'react-root' || el.hasAttribute('data-reactroot') || el.tagName === 'MAIN' || el.tagName === 'SECTION';
        };

        const originalDescriptor = Object.getOwnPropertyDescriptor(Element.prototype, 'innerHTML') || 
                                   Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'innerHTML');
        if (originalDescriptor && originalDescriptor.set) {
            Object.defineProperty(Element.prototype, 'innerHTML', {
                set: function(value) {
                    if ((value === '' || value.length < 50) && isMajorElement(this)) {
                        console.warn("[Clonescript] Blocked attempt to clear UI.");
                        return;
                    }
                    return originalDescriptor.set.call(this, value);
                }
            });
        }

        // 2. THE FREEZER: Paralytic Strike after 5 seconds
        setTimeout(() => {
            console.warn("[Clonescript] 5s elapsed. Paralyzing UI logic to prevent collapse...");
            
            // Kill all Timers
            window.setTimeout = function() { return 0; };
            window.setInterval = function() { return 0; };
            window.requestAnimationFrame = function() { return 0; };
            
            // Kill all Observers
            MutationObserver.prototype.observe = function() { return; };
            
            // Kill all Network
            window.fetch = function() { return new Promise(() => {}); };
            XMLHttpRequest.prototype.send = function() { return; };
            XMLHttpRequest.prototype.open = function() { return; };
            
            console.log("[Clonescript] UI Logic is now frozen. Site should be stable.");
        }, 5000);

        // 3. Persistence Mocks
        window.WebSocket = function() { this.readyState = 1; this.send = ()=>{}; this.close = ()=>{}; };
        window.WebSocket.prototype = { CONNECTING: 0, OPEN: 1, CLOSING: 2, CLOSED: 3 };

        try {
            Object.defineProperty(navigator, 'serviceWorker', {
                get: () => ({ register: () => new Promise(()=>{}), getRegistration: () => Promise.resolve(null), getRegistrations: () => Promise.resolve([]), addEventListener: ()=>{} })
            });
        } catch(e) {}

        window.addEventListener('unhandledrejection', (e) => { e.stopImmediatePropagation(); e.preventDefault(); });
        window.onerror = () => true;
    })();
    </script>
    """
    
    count = 0
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    if 'clonescript-stability' in content:
                        p1 = content.find('<script id="clonescript-stability">')
                        p2 = content.find('</script>', p1) + 9
                        new_content = content[:p1] + stability_js + content[p2:]
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        count += 1
                    elif '<head>' in content:
                        new_content = content.replace('<head>', f'<head>{stability_js}', 1)
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        count += 1
                except Exception as e:
                    print(f"  [!] Injection error in {file}: {e}")
    print(f"[+] Freezer Shield v7 injected into {count} files.")

def sanitize_html_files(target_path):
    """
    Finds all HTML files in the target directory and strips out 
    Implements The De-Hydrator (v8). 
    Physically disables all hydration scripts to preserve the stable HTML state.
    Also strips CORS-blocking attributes.
    """
    print(f"[*] Starting Great De-Hydration (v8) + Security Sanitization...")
    
    # regex for script tags
    import re
    script_re = re.compile(r'(<script\b[^>]*?)>', re.IGNORECASE)
    
    count_scripts = 0
    count_cors = 0
    
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    # 1. Great De-Hydration: Disable all non-shield scripts (EXCEPT navigation logic)
                    orig = content
                    def disable_script(match):
                        tag = match.group(1)
                        # WHITELIST: Don't disable our custom navigation script
                        if 'navigation.js' in tag:
                            return f"{tag}>"
                        
                        if 'clonescript-stability' in tag:
                            return match.group(0) # Keep our shield
                        
                        # Add or replace type with disabled type
                        if 'type=' in tag.lower():
                            tag = re.sub(r'type=["\'][^"\']*?["\']', 'type="application/x-clonescript-disabled"', tag, flags=re.IGNORECASE)
                        else:
                            tag += ' type="application/x-clonescript-disabled"'
                        
                        nonlocal count_scripts
                        count_scripts += 1
                        return f"{tag}>"

                    content = script_re.sub(disable_script, content)
                    
                    # 2. CORS Sanitization: Universal strip for file:// protocol stability
                    # Strips crossorigin and integrity from ALL tags (img, svg, link, script, source, a)
                    content = re.sub(r'\s+crossorigin(?:=["\'][^"\']*?["\'])?', '', content, flags=re.IGNORECASE)
                    content = re.sub(r'\s+integrity=["\'][^"\']*?["\']', '', content, flags=re.IGNORECASE)
                    
                    # 3. Manifest Cleanup: Remove <link rel="manifest"> which causes CORS errors on file://
                    content = re.sub(r'<link\s+[^>]*?rel=["\']manifest["\'][^>]*?>', '', content, flags=re.IGNORECASE)

                    if content != orig:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        count_cors += 1
                except Exception as e:
                    print(f"  [!] Sanitization error in {file}: {e}")
                    
    print(f"[+] De-Hydrated {count_scripts} scripts across the project.")
    print(f"[+] Security attributes removed from {count_cors} files.")

def inject_footer_shell(target_path):
    """
    Injects the HTML shell for the footer. 
    Maintains Sidebar (Logo+Socials) but leaves links container empty for navigation.js.
    """
    print(f"[*] Injecting Footer Shell (v12)...")
    
    SOCIALS = [
        ("X", "https://twitter.com/tradingview/", '<svg width="18" height="18" viewBox="0 0 18 18"><path d="M10.74 7.64L17.15 0h-1.52l-5.57 6.47L5.59 0H.44l6.73 9.79L.44 17.68h1.52l5.88-6.84 4.7 6.84h5.15L10.74 7.64zm-2.08 2.42l-.68-.97L2.51 1.25H4.85l4.5 6.43.68.98 5.6 7.99h-2.33l-5.04-7.19z" fill="currentColor"/></svg>'),
        ("Facebook", "https://www.facebook.com/tradingview/", '<svg width="22" height="22" viewBox="0 0 24 24"><path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H8v-3h2V9.5C10 7.57 11.57 6 13.5 6H16v3h-2c-.55 0-1 .45-1 1V12h3v3h-3v6.8c4.56-.93 8-4.96 8-9.8z" fill="currentColor"/></svg>'),
        ("YouTube", "https://www.youtube.com/@TradingView", '<svg width="22" height="22" viewBox="0 0 24 24"><path d="M21.58 7.19c-.23-.86-.91-1.54-1.78-1.78C18.25 5 12 5 12 5s-6.25 0-7.8.41c-.87.24-1.55.92-1.78 1.78C2 8.75 2 12 2 12s0 3.25.42 4.81c.23.86.91 1.54 1.78 1.78 1.55.41 7.8.41 7.8.41s6.25 0 7.8-.41c.87-.24 1.55-.92 1.78-1.78.42-1.56.42-4.81.42-4.81s0-3.25-.42-4.81zM10 15V9l5.2 3L10 15z" fill="currentColor"/></svg>'),
        ("LinkedIn", "https://www.linkedin.com/company/tradingview/", '<svg width="22" height="22" viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a2.7 2.7 0 0 0-2.7-2.7c-1.1 0-1.9.6-2.3 1.5v-1.3H11v7.8h2.5v-4.2c0-.6.5-1.1 1.1-1.1s1.1.5 1.1 1.1v4.2h2.5M7 10h2.5V17.5H7V10m0-3.5a1.25 1.25 0 1 0 2.5 0 1.25 1.25 0 0 0-2.5 0z" fill="currentColor"/></svg>'),
        ("Instagram", "https://www.instagram.com/tradingview/", '<svg width="22" height="22" viewBox="0 0 24 24"><path d="M7.8 2h8.4C19.4 2 22 4.6 22 7.8v8.4c0 3.2-2.6 5.8-5.8 5.8H7.8C4.6 22 2 19.4 2 16.2V7.8C2 4.6 4.6 2 7.8 2m-.2 2C5.6 4 4 5.6 4 7.6v8.8C4 18.4 5.6 20 7.6 20h8.8c2 0 3.6-1.6 3.6-3.6V7.6c0-2-1.6-3.6-3.6-3.6H7.6m9.4 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2m-5 3c2.8 0 5 2.2 5 5s-2.2 5-5 5-5-2.2-5-5 2.2-5 5-5m0 2c-1.7 0-3 1.3-3 3s1.3 3 3 3 3-1.3 3-3-1.3-3-3-3z" fill="currentColor"/></svg>')
    ]

    count = 0
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    parts = os.path.relpath(root, target_path).split(os.sep)
                    try:
                        idx = parts.index('www.tradingview.com')
                        depth = len(parts) - 1 - idx
                        prefix = "../" * depth
                    except ValueError:
                        prefix = ""

                    sidebar_html = f'''
                        <div class="footerSidebar-hezxxKBJ">
                            <span class="tv-header__logo" style="margin-bottom: 24px; display: block;">
                                <a href="{prefix}index.html" class="tv-header__link tv-header__link--logo" style="color: currentColor; display: flex; align-items: center; gap: 8px;">
                                    <svg width="36" height="28" viewBox="0 0 36 28"><path d="M14 22H7V11H0V4h14v18zM28 22h-8l7.5-18h8L28 22z" fill="currentColor"/><circle cx="20" cy="8" r="4" fill="currentColor"/></svg>
                                    <span style="font-size: 20px; font-weight: 700; letter-spacing: -0.02em;">TradingView</span>
                                </a>
                            </span>
                            <div class="footerSocials-hezxxKBJ" style="display: flex; gap: 16px; margin-bottom: 32px; flex-wrap: wrap;">
                    '''
                    for label, url, svg in SOCIALS:
                        sidebar_html += f'<a href="{url}" target="_blank" aria-label="{label}" style="color: #d1d4dc; transition: color 0.2s;">{svg}</a>'
                    sidebar_html += '</div></div>'

                    # Shell for navigation.js
                    full_footer = f'<footer class="tv-footer js-footer" style="padding: 60px 0; border-top: 1px solid #2a2e39; background: #131722;"><div style="max-width: 1200px; margin: 0 auto; display: flex; flex-direction: row; gap: 60px; padding: 0 20px;">{sidebar_html}<div class="footerLinksContainer-hezxxKBJ"></div></div></footer>'

                    new_content = re.sub(r'<footer\b.*?>.*?</footer>', full_footer, content, flags=re.DOTALL | re.IGNORECASE)
                    
                    if new_content != content:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        count += 1
                except Exception as e:
                    print(f"  [!] Footer Error in {file}: {e}")

    print(f"[+] Footer shells (v12) injected into {count} files.")

def inject_header_shell(target_path):
    """
    Ensures the .tv-header__main-menu container exists but is empty for navigation.js.
    """
    print(f"[*] Injecting Header Shell (v12)...")
    count = 0
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    if 'tv-header__main-menu' in content:
                        # Empty it out so navigation.js can fill it
                        content = re.sub(r'(<ul[^>]*?class=["\'][^"\']*?tv-header__main-menu[^"\']*?["\'][^>]*?>).*?(</ul>)', r'\1<!-- Nav-Bridge -->\2', content, flags=re.DOTALL)
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    count += 1
                except Exception as e:
                    print(f"  [!] Header Shell Error in {file}: {e}")
    print(f"[+] Header shells restored on {count} pages.")

def ensure_navigation_inclusion(target_path):
    """
    Ensures that every page has <script src="navigation.js"></script> 
    with correct relative pathing just before </body>.
    """
    print(f"[*] Ensuring Navigation Script Inclusion (v12)...")
    count = 0
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    parts = os.path.relpath(root, target_path).split(os.sep)
                    try:
                        idx = parts.index('www.tradingview.com')
                        depth = len(parts) - 1 - idx
                        prefix = "../" * depth
                    except ValueError:
                        prefix = ""

                    script_tag = f'<script src="{prefix}navigation.js"></script>'
                    
                    # Remove any existing disabled navigation script
                    content = re.sub(r'<script[^>]*?navigation\.js[^>]*?></script>', '', content, flags=re.IGNORECASE)
                    
                    # Add it before </body>
                    if '</body>' in content:
                        content = content.replace('</body>', f'{script_tag}\n</body>')
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    count += 1
                except Exception as e:
                    print(f"  [!] Script Inclusion Error in {file}: {e}")
    print(f"[+] Script inclusion verified for {count} pages.")

def clone_project(urls, output_dir, project_name=None):
    """Executes wget with batch support and host preservation."""
    if project_name:
        folder_name = project_name
    else:
        folder_name = sanitize_folder_name(urls[0])
        
    target_path = os.path.join(output_dir, folder_name)
    
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    print(f"[*] Project Mode: Host Preservation Enabled")
    print(f"[*] Target folder: {target_path}")
    print(f"[*] Processing {len(urls)} URLs...")
    
    # Flags explained:
    # -p: Page requisites (css, js, images)
    # -k: Convert links for offline viewing
    # -E: Adjust extension (adds .html if missing)
    # -H: Span hosts (for external assets like CDNs)
    # -P: Prefix/output directory
    # (Removed -nH to prevent host collision issues)
    
    cmd = [
        "wget",
        "-p", "-k", "-E", "-H",
        "-P", target_path
    ]
    cmd.extend(urls)
    
    try:
        subprocess.run(cmd, check=True)
        print(f"[+] Success: Project '{folder_name}' cloned.")
        create_root_redirect(target_path, urls)
        # Note: Scavenger (discover_and_download_chunks) removed - all scripts are
        # de-hydrated (disabled) by sanitize_html_files anyway, so chunk downloads are redundant.
        inject_stability_script(target_path)      # Inject stability shield
        sanitize_html_files(target_path)          # De-hydrate scripts + cleanup CORS
    except subprocess.CalledProcessError as e:
        print(f"[!] Error during batch cloning: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Clonescript: Robust Multi-Host Downloader")
    parser.add_argument("urls", nargs="*", help="URLs to clone")
    parser.add_argument("--file", "-f", help="File containing URLs to clone (one per line)")
    parser.add_argument("--out", "-o", default="downloads", help="Output directory (default: downloads)")
    parser.add_argument("--project", "-p", help="Project/Site name")
    
    args = parser.parse_args()
    
    urls_to_process = []
    
    if args.urls:
        urls_to_process.extend(args.urls)
    
    if args.file:
        if os.path.exists(args.file):
            with open(args.file, 'r') as f:
                for line in f:
                    u = line.strip()
                    if u and not u.startswith("#"):
                        urls_to_process.append(u)
        else:
            print(f"[!] Error: File {args.file} not found.")

    if not urls_to_process:
        print("[!] No URLs provided. Use 'python cloner.py <URL>' or '--file queue.txt'")
        return

    # Create main output directory
    if not os.path.exists(args.out):
        os.makedirs(args.out)

    clone_project(urls_to_process, args.out, project_name=args.project)

if __name__ == "__main__":
    main()

