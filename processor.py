#!/usr/bin/env python3
import os
import re

def inject_stability_script(target_path):
    """Injects the UI Freezer Shield (v7) into HTML files."""
    print(f"[*] Injecting UI Freezer Shield (v7) into HTML files...")
    script_v7 = '''
<script id="clonescript-stability" type="text/javascript">
(function() {
    console.log("[Clonescript] Freezer Shield v7 active. UI will be paralyzed in 5 seconds.");
    
    // 1. Mock critical APIs to prevent dynamic crashes
    window.fetch = function() { return new Promise(()=>{}); };
    window.XMLHttpRequest.prototype.send = function() {};
    if (window.ServiceWorkerContainer) {
        Object.defineProperty(window.ServiceWorkerContainer.prototype, 'register', { value: function() { return new Promise(()=>{}); } });
    }
    
    // 2. Stub storage
    const noopStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {}, clear: () => {}, key: () => null, length: 0 };
    Object.defineProperty(window, 'localStorage', { value: noopStorage });
    Object.defineProperty(window, 'sessionStorage', { value: noopStorage });

    // 3. The Great Paralysis (Delayed to allow initial static render)
    setTimeout(() => {
        console.log("[Clonescript] Paralyzing UI runtime...");
        
        // Intercept DOM node creation to stop React/Webpack hydration
        const origCreateElement = document.createElement;
        document.createElement = function(tag) {
            if (tag.toLowerCase() === 'script' || tag.toLowerCase() === 'iframe') {
                return origCreateElement.call(document, 'div');
            }
            return origCreateElement.apply(document, arguments);
        };

        // Neutralize internal timeouts
        const maxId = setTimeout(() => {}, 0);
        for (let i = 0; i < maxId; i++) { clearTimeout(i); clearInterval(i); }
        
        window.onclick = function(e) { 
            // Allow navigation but stop dynamic script triggers
            if (e.target.tagName !== 'A' && !e.target.closest('a')) {
                e.stopPropagation();
            }
        };
    }, 5000);
})();
</script>
'''
    count = 0
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    if 'clonescript-stability' not in content:
                        if '<head>' in content:
                            content = content.replace('<head>', f'<head>\n{script_v7}')
                        else:
                            content = f"{script_v7}\n{content}"
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        count += 1
                except Exception as e:
                    print(f"  [!] Stability injection error in {file}: {e}")
    print(f"[+] Freezer Shield v7 injected into {count} files.")

def sanitize_html_files(target_path):
    """De-Hydration (v8) + CORS Sanitization."""
    print(f"[*] Starting Great De-Hydration (v8) + Security Sanitization...")
    count_scripts = 0
    count_cors = 0
    script_re = re.compile(r'(<script\b[^>]*?)(/?)>', re.IGNORECASE | re.DOTALL)
    
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    orig = content
                    def disable_script(match):
                        tag = match.group(1)
                        if 'navigation.js' in tag: return f"{tag}>"
                        if 'clonescript-stability' in tag: return match.group(0)
                        
                        if 'type=' in tag.lower():
                            tag = re.sub(r'type=["\'][^"\']*?["\']', 'type="application/x-clonescript-disabled"', tag, flags=re.IGNORECASE)
                        else:
                            tag += ' type="application/x-clonescript-disabled"'
                        nonlocal count_scripts
                        count_scripts += 1
                        return f"{tag}>"

                    content = script_re.sub(disable_script, content)
                    content = re.sub(r'\s+crossorigin(?:=["\'][^"\']*?["\'])?', '', content, flags=re.IGNORECASE)
                    content = re.sub(r'\s+integrity=["\'][^"\']*?["\']', '', content, flags=re.IGNORECASE)
                    content = re.sub(r'<link\s+[^>]*?rel=["\']manifest["\'][^>]*?>', '', content, flags=re.IGNORECASE)

                    if content != orig:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        count_cors += 1
                except Exception as e:
                    print(f"  [!] Sanitization error in {file}: {e}")
                    
    print(f"[+] De-Hydrated {count_scripts} scripts across the project.")
    print(f"[+] Security attributes removed from {count_cors} files.")

def inject_header_shell(target_path):
    """Injects empty menu container for navigation.js."""
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
                        content = re.sub(r'(<ul[^>]*?class=["\'][^"\']*?tv-header__main-menu[^"\']*?["\'][^>]*?>).*?(</ul>)', r'\1<!-- Nav-Bridge -->\2', content, flags=re.DOTALL)
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        count += 1
                except Exception as e:
                    print(f"  [!] Header Error in {file}: {e}")
    print(f"[+] Header shells restored on {count} pages.")

def inject_footer_shell(target_path):
    """Injects layout container for navigation.js."""
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
                    except ValueError: prefix = ""

                    sidebar_html = f'''
                        <div class="footerSidebar-hezxxKBJ" style="max-width: 280px; flex-shrink: 0; display: flex; flex-direction: column; align-items: flex-start;">
                            <span class="tv-header__logo" style="margin-bottom: 24px; display: block;">
                                <a href="{prefix}index.html" class="tv-header__link tv-header__link--logo" style="color: #f0f3fa; display: flex; align-items: center; gap: 8px;">
                                    <svg width="36" height="28" viewBox="0 0 36 28"><path d="M14 22H7V11H0V4h14v18zM28 22h-8l7.5-18h8L28 22z" fill="currentColor"/><circle cx="20" cy="8" r="4" fill="currentColor"/></svg>
                                    <span style="font-size: 20px; font-weight: 700; letter-spacing: -0.01em;">TradingView</span>
                                </a>
                            </span>
                            <p style="color: #787b86; font-size: 14px; line-height: 1.6; margin-bottom: 32px; margin-top: 0; padding-right: 20px;">
                                TradingView is a world-class charting platform and social network used by 50M+ traders and investors worldwide to spot opportunities across global markets.
                            </p>
                            <div class="footerSocials-hezxxKBJ" style="display: flex; gap: 20px; flex-wrap: wrap; color: #787b86;">
                    '''
                    for label, url, svg in SOCIALS:
                        sidebar_html += f'<a href="{url}" target="_blank" aria-label="{label}" style="color: inherit; transition: color 0.2s;">{svg}</a>'
                    sidebar_html += '</div></div>'

                    full_footer = f'<footer class="tv-footer js-footer" style="padding: 80px 0; border-top: 1px solid #2a2e39; background: #000000;"><div style="max-width: 1200px; margin: 0 auto; display: flex; flex-direction: row; gap: 80px; padding: 0 20px;">{sidebar_html}<div class="footerLinksContainer-hezxxKBJ"></div></div></footer>'
                    content = re.sub(r'<footer\b.*?>.*?</footer>', full_footer, content, flags=re.DOTALL | re.IGNORECASE)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    count += 1
                except Exception as e:
                    print(f"  [!] Footer Error in {file}: {e}")
    print(f"[+] Footer shells injected into {count} files.")

def ensure_navigation_inclusion(target_path):
    """Ensures navigation.js is linked globally."""
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
                    except ValueError: prefix = ""

                    script_tag = f'<script src="{prefix}navigation.js"></script>'
                    content = re.sub(r'<script[^>]*?navigation\.js[^>]*?></script>', '', content, flags=re.IGNORECASE)
                    if '</body>' in content:
                        content = content.replace('</body>', f'{script_tag}\n</body>')
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    count += 1
                except Exception as e:
                    print(f"  [!] Script Inclusion Error in {file}: {e}")
    print(f"[+] Script inclusion verified for {count} pages.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Processor: Modernizes and Stabilizes Cloned Sites")
    parser.add_argument("path", help="Path to the cloned project directory")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"[!] Error: Path {args.path} not found.")
        return

    inject_stability_script(args.path)
    sanitize_html_files(args.path)
    inject_header_shell(args.path)
    inject_footer_shell(args.path)
    ensure_navigation_inclusion(args.path)

if __name__ == "__main__":
    main()
