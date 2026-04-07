import os
import glob
import re

template_dir = r"c:\zaid\Autocare\Autocareapp\templates\Autocareapp"
files = glob.glob(os.path.join(template_dir, "*.html"))

css_link = """
    <!-- Theme CSS -->
    <link rel="stylesheet" href="{% static 'css/theme.css' %}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
"""

js_link_and_button = """
    <!-- Floating Theme Toggle Button -->
    <button id="theme-toggle" class="theme-toggle-btn" style="position: fixed; bottom: 20px; right: 20px; z-index: 1000; background: var(--card-bg); border-radius: 50%; width: 50px; height: 50px; box-shadow: var(--glass-shadow); border: 1px solid var(--border-color);">
        <i class="bi bi-moon-stars-fill"></i>
    </button>
    <!-- Theme JS -->
    <script src="{% static 'js/theme.js' %}"></script>
"""

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
        
    # Ensure {% load static %} is at the top
    if "{% load static %}" not in content:
        # Avoid putting it before <?xml or similar, but generally top is fine.
        content = "{% load static %}\n" + content
        
    # Add CSS before </head> if not already there
    if "css/theme.css" not in content and "</head>" in content:
        content = content.replace("</head>", css_link + "\n</head>")
        
    # Add JS and button before </body> if not already there
    if "js/theme.js" not in content and "</body>" in content:
        content = content.replace("</body>", js_link_and_button + "\n</body>")
        
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(file_path)}")
    else:
        print(f"Skipped {os.path.basename(file_path)} (already updated or formatting differ)")
        
print("Template updating complete.")
