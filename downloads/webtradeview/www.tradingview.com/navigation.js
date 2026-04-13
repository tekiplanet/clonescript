/**
 * navigation.js
 * Central source of truth for the Header and Footer menus.
 * Premium Build: Transitions, Dropdowns, Mobile Support, and Active States.
 */

(function() {
    // Premium Design Tokens - Dark Mode & Adaptive Colors
    const COLORS = {
        primary: '#2962FF',
        text: 'currentColor',
        subtext: '#787b86',
        bg: '#1e222d',
        border: '#2a2e39',
        hover: '#2a2e39'
    };

    const MENU_DATA = {
        header: [
            {
                title: 'Platform',
                id: 'platform',
                items: [
                    { label: 'Charting Platform', path: 'chart/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M13 3h2v19h-2zm-6 8h2v11H7zm12-4h2v15h-2z" fill="currentColor"/></svg>' },
                    { label: 'Trading Features', path: 'trading/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M19 4h-2v3h-2v2h2v15h2V9h2V7h-2V4zM9 4H7v11H5v2h2v7h2v-7h2v-2H9V4z" fill="currentColor"/></svg>' },
                    { label: 'Desktop App', path: 'trading-platform/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M4 5h20v11H4V5zm0 13h20v2H4v-2zm8 3h4v2h-4v-2z" fill="currentColor"/></svg>' },
                    { label: 'Features', path: 'features/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M14 3L4 9v10l10 6 10-6V9l-10-6zm0 2.3l7.9 4.7L14 14.7 6.1 10 14 5.3zM6 11.2l7 4.2V23l-7-4.2v-7.6zm9 11.8v-7.6l7-4.2V19l-7 4z" fill="currentColor"/></svg>' }
                ]
            },
            {
                title: 'Products',
                id: 'products',
                items: [
                    { label: 'Advanced Library', path: 'advanced-charts/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M4 4h20v20H4V4zm2 2v16h16V6H6zm3 11h2v3H9v-3zm4-4h2v7h-2v-7zm4 2h2v5h-2v-5z" fill="currentColor"/></svg>' },
                    { label: 'Lightweight Charts', path: 'lightweight-charts/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M4 14l8-8 6 6 6-6M4 24h20v-2H4v2z" fill="currentColor" stroke="currentColor" stroke-width="0.5"/></svg>' },
                    { label: 'Integration', path: 'brokerage-integration/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M14 3l-6 10h12L14 3zm0 22l6-10H8l6 10z" fill="currentColor"/></svg>' }
                ]
            },
            {
                title: 'Markets',
                id: 'markets',
                items: [
                    { label: 'Summary', path: 'markets/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M4 4h8v8H4V4zm2 2v4h4V6H6zm12-2h8v8h-8V4zm2 2v4h4V6h-4zM4 16h8v8H4v-8zm2 2v4h4v-4H6zm12-2h8v8h-8v-8zm2 2v4h4v-4h-4z" fill="currentColor"/></svg>' },
                    { label: 'Exchanges', path: 'data-coverage/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M14 3a11 11 0 100 22 11 11 0 000-22zm0 2a9 9 0 011 17.9V5.1a9 9 0 01-1-0.1z" fill="currentColor"/></svg>' }
                ]
            },
            {
                title: 'Brokers',
                id: 'brokers',
                items: [
                    { label: 'Broker List', path: 'brokers/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M4 22h20v2H4v-2zm3-2h2V11H7v9zm6-12h2v12h-2V8zm6 4h2v8h-2v-8zM14 3l8 4v2L6 9V7l8-4z" fill="currentColor"/></svg>' },
                    { label: 'Comparison', path: 'brokers/compare/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M4 7h8v2H4V7zm0 6h8v2H4v-2zm0 6h8v2H4v-2zm12-12h8v14h-8V7zm2 2v10h4V9h-4z" fill="currentColor"/></svg>' },
                    { label: 'Awards', path: 'broker-awards/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M14 4l3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1 3-6z" fill="currentColor"/></svg>' }
                ]
            },
            {
                title: 'Community',
                id: 'community',
                items: [
                    { label: 'Social Feed', path: 'social-network/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M14 3a8 8 0 00-8 8c0 4.4 8 14 8 14s8-9.6 8-14a8 8 0 00-8-8zm0 11a3 3 0 110-6 3 3 0 010 6z" fill="currentColor"/></svg>' },
                    { label: 'Testimonials', path: 'wall-of-love/index.html', icon: '<svg width="20" height="20" viewBox="0 0 28 28"><path d="M14 3c-5 0-9 4-9 9 0 7 9 13 9 13s9-6 9-13c0-5-4-9-9-9zm0 6a3 3 0 110 6 3 3 0 010-6z" fill="currentColor"/></svg>' }
                ]
            }
        ],
        footer: [
            {
                title: 'Product',
                items: [
                    { label: 'Chart', path: 'chart/index.html' },
                    { label: 'App', path: 'trading-platform/index.html' },
                    { label: 'Advanced Charts', path: 'advanced-charts/index.html' },
                    { label: 'Lightweight Charts', path: 'lightweight-charts/index.html' },
                    { label: 'Features', path: 'features/index.html' }
                ]
            },
            {
                title: 'Company',
                items: [
                    { label: 'About', path: 'about/index.html' },
                    { label: 'Space Mission', path: 'space-mission/index.html' },
                    { label: 'Media Kit', path: 'media-kit/index.html' }
                ]
            },
            {
                title: 'Partnerships',
                items: [
                    { label: 'Advertising', path: 'advertising-info/index.html' },
                    { label: 'Partner Program', path: 'partner-program/index.html' },
                    { label: 'Education Program', path: 'students/index.html' }
                ]
            },
            {
                title: 'Support',
                items: [
                    { label: 'Help Center', path: 'support/index.html' },
                    { label: 'Security', path: 'security/index.html' }
                ]
            },
            {
                title: 'Legal',
                items: [
                    { label: 'Privacy Policy', path: 'privacy-policy/index.html' },
                    { label: 'Cookies Policy', path: 'cookies-policy/index.html' },
                    { label: 'Terms of Use', path: 'policies/index.html' },
                    { label: 'Disclaimer', path: 'disclaimer/index.html' }
                ]
            }
        ]
    };

    // Define global callback for Google Translate
    window.googleTranslateElementInit = function() {
        new google.translate.TranslateElement({
            pageLanguage: 'en',
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
            autoDisplay: false
        }, 'google_translate_element');
    };

    function injectShell() {
        // Inject Google Font
        if (!document.getElementById('tv-nav-font')) {
            const font = document.createElement('link');
            font.id = 'tv-nav-font';
            font.rel = 'stylesheet';
            font.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap';
            document.head.appendChild(font);
        }

        // Inject JivoChat Widget
        if (!document.getElementById('jivo-chat-widget')) {
            const jivo = document.createElement('script');
            jivo.id = 'jivo-chat-widget';
            jivo.src = 'https://code.jivosite.com/widget/GHQzWREEq6';
            jivo.async = true;
            document.head.appendChild(jivo);
        }

        // Inject Google Translate API
        if (!document.getElementById('google-translate-api')) {
            const gt = document.createElement('script');
            gt.id = 'google-translate-api';
            gt.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
            document.head.appendChild(gt);
        }

        const css = `
            body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
            
            /* Premium Header Nav */
            .tv-header__main-menu-item { position: relative; padding: 0 8px; }
            .tv-header__link { font-weight: 500; font-size: 15px; color: ${COLORS.text}; transition: color 0.1s ease; }
            .tv-header__link:hover { color: ${COLORS.primary} !important; }
            .tv-header__link.is-active { color: ${COLORS.primary} !important; position: relative; }
            .tv-header__link.is-active::after { 
                content: ""; position: absolute; bottom: -12px; left: 0; width: 100%; height: 3px; 
                background: ${COLORS.primary}; border-radius: 4px 4px 0 0; 
            }
            
            /* The Hover Bridge Fix */
            .tv-nav-dropdown::before {
                content: ""; position: absolute; top: -15px; left: 0; width: 100%; height: 15px; background: transparent;
            }

            /* Desktop Dropdowns - Premium Dark Mode */
            .tv-nav-dropdown {
                position: absolute; top: 100%; left: 0; min-width: 240px; 
                background: rgba(30, 34, 45, 0.98); backdrop-filter: blur(10px);
                border: 1px solid ${COLORS.border}; border-radius: 12px;
                box-shadow: 0 10px 40px -10px rgba(0,0,0,0.5), 0 5px 20px -5px rgba(0,0,0,0.3);
                padding: 12px; opacity: 0; visibility: hidden;
                transform: translateY(10px) scale(0.98); transform-origin: top left;
                transition: transform 0.2s cubic-bezier(0.2, 0, 0, 1), opacity 0.2s ease, visibility 0.2s;
                z-index: 99999; margin-top: 10px;
            }
            .tv-header__main-menu-item:hover .tv-nav-dropdown { opacity: 1; visibility: visible; transform: translateY(0) scale(1); }
            
            .tv-nav-dropdown-item {
                display: flex; align-items: center; gap: 12px; padding: 12px 14px;
                border-radius: 8px; color: #d1d4dc; text-decoration: none;
                font-size: 14px; font-weight: 500; transition: background 0.15s ease, color 0.15s ease;
            }
            .tv-nav-dropdown-item:hover { background: ${COLORS.hover}; color: ${COLORS.primary}; }
            .tv-nav-dropdown-item.is-active { background: ${COLORS.hover}; color: ${COLORS.primary}; }
            .tv-nav-dropdown-icon { color: ${COLORS.subtext}; transition: color 0.15s ease; width: 22px; display: flex; justify-content: center; }
            .tv-nav-dropdown-item:hover .tv-nav-dropdown-icon { color: ${COLORS.primary}; }

            /* Mobile Premium Drawer - Flush Left Build */
            #tv-mobile-nav-overlay {
                position: fixed; top: 0; bottom: 0; left: 0; width: 85%; max-width: 320px;
                background: #000000; z-index: 100000; 
                transform: translateX(-100%);
                transition: transform 0.35s cubic-bezier(0.2, 0, 0, 1);
                padding: 60px 24px 160px; overflow-y: scroll; border-right: 1px solid #2a2e39;
                -webkit-overflow-scrolling: touch; box-sizing: border-box;
            }
            #tv-mobile-nav-overlay.is-open { transform: translateX(0); }
            
            #tv-mobile-close {
                position: absolute; top: 16px; right: 16px; background: none; border: none; 
                color: #d1d4dc; cursor: pointer; padding: 8px;
            }

            #tv-mobile-backdrop {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
                z-index: 99999; opacity: 0; visibility: hidden; transition: opacity 0.3s ease;
            }
            #tv-mobile-backdrop.is-open { opacity: 1; visibility: visible; }
            
            .mobile-group-title { font-size: 11px; font-weight: 700; text-transform: uppercase; color: ${COLORS.subtext}; letter-spacing: 0.1em; margin-bottom: 12px; display: block; }
            .mobile-item { 
                display: flex; align-items: center; gap: 12px; padding: 10px 0; 
                color: #d1d4dc; text-decoration: none; font-size: 16px; font-weight: 500; flex-shrink: 0;
            }
            .mobile-item.is-active { color: ${COLORS.primary}; }

            /* Footer Premium Layout (Fix for Single Column) */
            .footerLinksContainer-hezxxKBJ { 
                display: flex; 
                flex-direction: row; 
                flex-wrap: wrap; 
                justify-content: space-between;
                gap: 40px; 
                flex-grow: 1; 
            }
            .footerLinksColumn-hezxxKBJ { min-width: 170px; }
            .footerLinksColumnTitle-hezxxKBJ { 
                display: block; font-weight: 700; color: #f0f3fa; 
                margin-bottom: 24px; font-size: 18px; text-transform: uppercase; letter-spacing: 0.14em;
            }
            .footerLinksColumnList-hezxxKBJ { list-style: none; padding: 0; margin: 0; }
            .footerLinksColumnListItem-hezxxKBJ { 
                display: block; padding: 10px 0; color: #787b86; 
                text-decoration: none; font-size: 16px; transition: color 0.2s, transform 0.2s;
            }
            .footerLinksColumnListItem-hezxxKBJ:hover { color: ${COLORS.primary} !important; transform: translateX(8px); }
            .footerLinksColumnListItem-hezxxKBJ.is-active { color: #ffffff !important; font-weight: 700; }

            /* Real-Life Mobile Footer (2-Column Grid) */
            @media (max-width: 768px) {
                .tv-footer > div { flex-direction: column !important; gap: 48px !important; align-items: flex-start !important; text-align: left !important; }
                .footerSidebar-hezxxKBJ { max-width: 100% !important; text-align: left !important; align-items: flex-start !important; }
                .footerSidebar-hezxxKBJ p { padding-right: 0 !important; font-size: 14px !important; }
                .footerLinksContainer-hezxxKBJ { 
                    display: grid !important; 
                    grid-template-columns: 1fr 1fr !important; 
                    gap: 32px 16px !important; 
                    width: 100% !important; 
                    text-align: left !important; 
                }
                .footerLinksColumn-hezxxKBJ { min-width: auto !important; }
                .footerLinksColumnTitle-hezxxKBJ { 
                    font-size: 12px !important; 
                    font-weight: 400 !important; 
                    color: #787b86 !important; 
                    margin-bottom: 12px !important;
                }
                .footerLinksColumnListItem-hezxxKBJ { 
                    font-size: 16px !important; 
                    font-weight: 600 !important; 
                    color: #d1d4dc !important; 
                    padding: 6px 0 !important;
                }
                .footerLinksColumnListItem-hezxxKBJ:hover { transform: none !important; }
            }

            /* Social Floating Chat (Bottom Left) */
            .tv-social-fab-container {
                position: fixed; bottom: 20px; left: 20px; z-index: 999999;
                display: flex; flex-direction: column-reverse; align-items: flex-start; gap: 12px;
            }
            .tv-social-fab {
                width: 56px; height: 56px; border-radius: 50%; background: #2962ff;
                display: flex; align-items: center; justify-content: center; color: white;
                box-shadow: 0 4px 12px rgba(41, 98, 255, 0.4); cursor: pointer;
                transition: transform 0.2s cubic-bezier(0.2, 0, 0, 1), background 0.2s;
            }
            .tv-social-fab:hover { transform: scale(1.05); background: #1e4bd8; }
            .tv-social-fab svg { width: 28px; height: 28px; }

            .tv-social-menu {
                display: flex; flex-direction: column; gap: 8px;
                opacity: 0; visibility: hidden; transform: translateY(10px) scale(0.95);
                transition: all 0.2s cubic-bezier(0.2, 0, 0, 1); transform-origin: bottom left;
            }
            .tv-social-menu.is-open { opacity: 1; visibility: visible; transform: translateY(0) scale(1); }

            .tv-social-menu-item {
                display: flex; align-items: center; gap: 10px; padding: 10px 16px;
                background: rgba(30, 34, 45, 0.95); backdrop-filter: blur(8px);
                border: 1px solid rgba(255,255,255,0.1); border-radius: 12px;
                color: white; text-decoration: none; font-size: 14px; font-weight: 600;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2); transition: transform 0.15s;
            }
            .tv-social-menu-item:hover { transform: translateX(5px); background: #2a2e39; }
            .tv-social-menu-item.whatsapp { border-left: 4px solid #25D366; }
            .tv-social-menu-item.telegram { border-left: 4px solid #0088cc; }
            .tv-social-menu-item svg { width: 20px; height: 20px; }

            /* Google Translate Skinning (Native Proxy) */
            .tv-header__area--lang { position: relative; display: flex; align-items: center; gap: 20px; }
            .tv-header__lang-proxy { display: flex; align-items: center; gap: 8px; cursor: pointer; transition: opacity 0.2s; }
            .tv-header__lang-proxy:hover { opacity: 0.8; }
            
            #google_translate_element { 
                position: absolute !important; top: 0 !important; left: 0 !important; 
                width: 70px !important; height: 100% !important; 
                opacity: 0 !important; cursor: pointer !important; z-index: 10 !important;
                overflow: hidden !important;
            }
            .goog-te-gadget-simple { width: 100% !important; height: 100% !important; border: none !important; margin: 0 !important; }

            /* Hide the ugly top bar injected by Google */
            .goog-te-banner-frame { display: none !important; visibility: hidden !important; }
            body { top: 0 !important; }
            
            /* Suppress ONLY the Legacy Language Button (Anti-Double) */
            .js-header-language-button, 
            .tv-header__language-button { 
                display: none !important; 
            }
        `;
        const style = document.createElement('style');
        style.innerHTML = css;
        document.head.appendChild(style);
    }

    function getRelPrefix() {
        const scripts = document.getElementsByTagName('script');
        for (let s of scripts) {
            if (s.src.includes('navigation.js')) {
                const parts = s.getAttribute('src').split('navigation.js')[0];
                return parts || '';
            }
        }
        return '';
    }

    function isPageActive(itemPath) {
        const currentPath = window.location.pathname;
        const cleanItemPath = itemPath.replace('index.html', '').replace(/\/$/, '');
        if (cleanItemPath === '') return currentPath === '/' || currentPath.endsWith('index.html') && !currentPath.includes('/', 1);
        return currentPath.includes('/' + cleanItemPath);
    }

    function renderHeader(prefix) {
        const container = document.querySelector('.tv-header__main-menu');
        if (!container) return;

        let html = '';
        MENU_DATA.header.forEach((group, index) => {
            const firstLink = prefix + group.items[0].path;
            const isGroupActive = group.items.some(item => isPageActive(item.path));
            
            let dropdownHtml = `<div class="tv-nav-dropdown">`;
            group.items.forEach(item => {
                const activeClass = isPageActive(item.path) ? 'is-active' : '';
                dropdownHtml += `
                    <a href="${prefix}${item.path}" class="tv-nav-dropdown-item ${activeClass}">
                        <span class="tv-nav-dropdown-icon">${item.icon}</span>
                        <span class="tv-nav-dropdown-label">${item.label}</span>
                    </a>`;
            });
            dropdownHtml += `</div>`;

            html += `
                <li class="tv-header__main-menu-item">
                    <a class="tv-header__link ${isGroupActive ? 'is-active' : ''}" href="${firstLink}">${group.title}</a>
                    ${dropdownHtml}
                </li>
            `;
        });
        
        // Proxy for the language switcher only
        const langArea = document.querySelector('.tv-header__area--user') || container.parentElement;
        if (langArea && !document.getElementById('tv-lang-managed')) {
            const proxy = document.createElement('div');
            proxy.id = 'tv-lang-managed';
            proxy.className = 'tv-header__area--lang';
            proxy.style.display = 'inline-flex';
            proxy.style.alignItems = 'center';
            proxy.style.position = 'relative';
            proxy.style.marginRight = '12px';
            
            proxy.innerHTML = `
                <div class="tv-header__lang-proxy">
                    <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M14 2C7.37258 2 2 7.37258 2 14C2 20.6274 7.37258 26 14 26C20.6274 26 26 20.6274 26 14C26 7.37258 20.6274 2 14 2Z" stroke="currentColor" stroke-width="1.5"/>
                        <path d="M2.5 14H25.5" stroke="currentColor" stroke-width="1.5"/>
                        <path d="M14 2.5C17.5 2.5 19.5 8 19.5 14C19.5 20 17.5 25.5 14 25.5C10.5 25.5 8.5 20 8.5 14C8.5 8 10.5 2.5 14 2.5Z" stroke="currentColor" stroke-width="1.5"/>
                    </svg>
                    <span style="font-weight: 600; font-size: 14px; margin-left: 8px; color: ${COLORS.text}">EN</span>
                </div>
                <div id="google_translate_element"></div>
            `;
            langArea.insertBefore(proxy, langArea.firstChild);
        }

        container.innerHTML = html;
        
        // Handle Logo Correctly
        const logos = document.querySelectorAll('.tv-header__link--logo');
        logos.forEach(logo => { logo.href = prefix + 'index.html'; });
    }

    function renderFooter(prefix) {
        const container = document.querySelector('.js-footer .footerLinksContainer-hezxxKBJ');
        if (!container) return;

        let html = '';
        MENU_DATA.footer.forEach(group => {
            let linksHtml = '';
            group.items.forEach(item => {
                const activeClass = isPageActive(item.path) ? 'is-active' : '';
                linksHtml += `<li><a class="footerLinksColumnListItem-hezxxKBJ ${activeClass}" href="${prefix}${item.path}">${item.label}</a></li>`;
            });

            html += `
                <div class="footerLinksColumn-hezxxKBJ">
                    <span class="footerLinksColumnTitle-hezxxKBJ">${group.title}</span>
                    <ul class="footerLinksColumnList-hezxxKBJ">
                        ${linksHtml}
                    </ul>
                </div>
            `;
        });
        container.innerHTML = html;
    }

    function setupMobileMenu(prefix) {
        if (!document.getElementById('tv-mobile-nav-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'tv-mobile-nav-overlay';
            const backdrop = document.createElement('div');
            backdrop.id = 'tv-mobile-backdrop';
            
            // Add Close Button
            overlay.innerHTML = `
                <button id="tv-mobile-close" aria-label="Close menu">
                    <svg width="24" height="24" viewBox="0 0 28 28"><path d="M6 6l16 16M6 22L22 6" fill="none" stroke="currentColor" stroke-width="2"/></svg>
                </button>
            `;
            
            let mobileHtml = '';
            MENU_DATA.header.forEach(group => {
                mobileHtml += `<div class="mobile-group"><span class="mobile-group-title">${group.title}</span>`;
                group.items.forEach(item => {
                    const activeClass = isPageActive(item.path) ? 'is-active' : '';
                    mobileHtml += `
                        <a href="${prefix}${item.path}" class="mobile-item ${activeClass}">
                            <span class="mobile-icon">${item.icon}</span>
                            <span class="mobile-label">${item.label}</span>
                        </a>`;
                });
                mobileHtml += `</div>`;
            });
            overlay.innerHTML += mobileHtml;
            document.body.appendChild(backdrop);
            document.body.appendChild(overlay);

            const btn = document.querySelector('.js-header-main-menu-mobile-button');
            const closeBtn = overlay.querySelector('#tv-mobile-close');

            const closeMenu = () => {
                overlay.classList.remove('is-open');
                backdrop.classList.remove('is-open');
            };

            if (btn) {
                btn.onclick = (e) => {
                    e.preventDefault();
                    overlay.classList.toggle('is-open');
                    backdrop.classList.toggle('is-open');
                };
            }
            if (closeBtn) closeBtn.onclick = closeMenu;
            backdrop.onclick = closeMenu;
        }
    }

    function setupSocialFloatingChat() {
        if (document.getElementById('tv-social-fab-container')) return;

        const container = document.createElement('div');
        container.id = 'tv-social-fab-container';
        container.className = 'tv-social-fab-container';
        
        container.innerHTML = `
            <div class="tv-social-fab" id="tv-social-fab-main" title="Contact Support">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
            </div>
            <div class="tv-social-menu" id="tv-social-fab-menu">
                <a href="https://wa.me/14242292950" target="_blank" class="tv-social-menu-item whatsapp">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.399-4.385 9.782-9.714 9.782 m0-17.3c-4.148 0-7.523 3.376-7.523 7.525 0 1.325.344 2.617 1.001 3.759l.115.197-.662 2.42 2.474-.649.19.112c1.103.654 2.368.999 3.665 1.002h.003c4.047 0 7.339-3.291 7.342-7.34a7.359 7.359 0 00-2.164-5.24 7.35 7.35 0 00-5.181-2.109"/></svg>
                    WhatsApp
                </a>
                <a href="https://t.me/webtradeview" target="_blank" class="tv-social-menu-item telegram">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.2-.08-.06-.19-.04-.27-.02-.11.02-1.93 1.23-5.46 3.62-.51.35-.98.52-1.4.51-.46-.01-1.35-.26-2.01-.48-.81-.27-1.46-.42-1.4-.88.03-.24.38-.1.97-.24 3.73-1.62 6.21-2.69 7.44-3.21 3.52-1.48 4.25-1.74 4.73-1.75.11 0 .35.03.5.15.13.1.17.24.18.33.01.07.02.24.01.38z"/></svg>
                    Telegram
                </a>
            </div>
        `;

        document.body.appendChild(container);
        
        const fab = document.getElementById('tv-social-fab-main');
        const menu = document.getElementById('tv-social-fab-menu');

        fab.onclick = (e) => {
            e.stopPropagation();
            menu.classList.toggle('is-open');
        };

        document.addEventListener('click', () => menu.classList.remove('is-open'));
    }
    function setupGlobalShield() {
        const REDIRECT_URL = 'https://app.web-tradeviews.com/login';
        
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a');
            if (!link) return;
            
            const href = link.getAttribute('href');
            if (!href) return;
            
            // Check if the link points to TradingView.com or its subdomains
            const isTradingView = href.includes('tradingview.com') || href.includes('tv.com') || href.includes('tradingview-widget.com');
            
            // Whitelist our own functionalized pages/paths
            // If it's a relative path starting with . or / and doesn't contain 'tradingview.com', it's likely internal
            const isInternal = (href.startsWith('.') || href.startsWith('/') || !href.includes('://')) && !href.includes('tradingview.com');

            if (isTradingView && !isInternal) {
                console.log("[GlobalGuard] Intercepted TradingView link, redirecting to login...");
                e.preventDefault();
                window.location.href = REDIRECT_URL;
            }
        }, true);
    }

    function init() {
        const prefix = getRelPrefix();
        injectShell();
        renderHeader(prefix);
        renderFooter(prefix);
        setupMobileMenu(prefix);
        setupGlobalShield();
        setupSocialFloatingChat();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
