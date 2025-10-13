#!/usr/bin/env python3
"""
Create a properly formatted HTML version of the Assignment 2 report for PDF conversion
"""

import re
import os

def markdown_to_html(md_content):
    """Convert markdown content to HTML with proper formatting"""
    
    # Convert headers
    md_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', md_content, flags=re.MULTILINE)
    
    # Convert bold text
    md_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md_content)
    
    # Convert italic text
    md_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', md_content)
    
    # Convert inline code
    md_content = re.sub(r'`(.+?)`', r'<code>\1</code>', md_content)
    
    # Convert code blocks
    md_content = re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', md_content, flags=re.DOTALL)
    
    # Convert links
    md_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', md_content)
    
    # Convert lists
    lines = md_content.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            result_lines.append(f'<li>{line.strip()[2:]}</li>')
        elif line.strip().startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ')):
            if not in_list:
                result_lines.append('<ol>')
                in_list = True
            result_lines.append(f'<li>{line.strip()[3:]}</li>')
        else:
            if in_list:
                result_lines.append('</ul>' if line.strip().startswith('-') else '</ol>')
                in_list = False
            if line.strip() and not line.startswith('<'):
                result_lines.append(f'<p>{line}</p>')
            else:
                result_lines.append(line)
    
    if in_list:
        result_lines.append('</ul>')
    
    md_content = '\n'.join(result_lines)
    
    return md_content

def create_html_report():
    """Create HTML report from markdown file"""
    
    input_file = "A2_Report_Davidsons_1685.md"
    output_file = "A2_Report_Davidsons_1685.html"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return False
    
    try:
        # Read markdown file
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to HTML
        html_content = markdown_to_html(md_content)
        
        # Create complete HTML document
        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assignment 2 Report - Davidsons (1685)</title>
    <style>
        @media print {{
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-size: 12pt;
                line-height: 1.6;
                color: #000;
            }}
            h1, h2, h3, h4, h5, h6 {{
                page-break-after: avoid;
                color: #000;
            }}
            pre, blockquote {{
                page-break-inside: avoid;
            }}
            table {{
                page-break-inside: avoid;
            }}
        }}
        
        body {{
            font-family: 'Times New Roman', 'Georgia', serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
            background-color: #fff;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 20px;
            font-size: 24pt;
            text-align: center;
        }}
        
        h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 18pt;
        }}
        
        h3 {{
            color: #2c3e50;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 16pt;
        }}
        
        h4 {{
            color: #34495e;
            margin-top: 15px;
            margin-bottom: 8px;
            font-size: 14pt;
        }}
        
        p {{
            margin-bottom: 12px;
            text-align: justify;
        }}
        
        strong {{
            color: #2c3e50;
            font-weight: bold;
        }}
        
        em {{
            font-style: italic;
            color: #7f8c8d;
        }}
        
        code {{
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', 'Monaco', monospace;
            font-size: 11pt;
            border: 1px solid #e9ecef;
        }}
        
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-left: 4px solid #3498db;
            border-radius: 5px;
            overflow-x: auto;
            margin: 15px 0;
            font-family: 'Courier New', 'Monaco', monospace;
            font-size: 10pt;
            border: 1px solid #e9ecef;
        }}
        
        pre code {{
            background: none;
            padding: 0;
            border: none;
        }}
        
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 11pt;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
            vertical-align: top;
        }}
        
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #f8f9fa;
            color: #555;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #3498db;
            margin: 30px 0;
        }}
        
        .header-info {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
        
        .header-info strong {{
            display: block;
            margin-bottom: 5px;
            font-size: 14pt;
        }}
        
        .toc {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            border: 1px solid #e9ecef;
        }}
        
        .toc h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        
        .toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        
        .toc li {{
            margin-bottom: 5px;
        }}
        
        .toc a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        .toc a:hover {{
            text-decoration: underline;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #3498db;
            text-align: center;
            color: #7f8c8d;
            font-size: 10pt;
        }}
    </style>
</head>
<body>
    <div class="header-info">
        <strong>CISC/CMPE 327, Fall 2025</strong>
        <strong>Assignment 2: Library Management System - Extended Unit Testing & CI/CD</strong>
        <strong>Student: Davidsons (ID: 1685)</strong>
    </div>
    
    {html_content}
    
    <div class="footer">
        <p>Submitted by: Davidsons (Student ID: 1685)<br>
        Course: CISC/CMPE 327, Fall 2025<br>
        Assignment: Library Management System - Extended Unit Testing & CI/CD</p>
    </div>
</body>
</html>"""
        
        # Write HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_doc)
        
        print(f"Successfully created {output_file}")
        return True
        
    except Exception as e:
        print(f"Error creating HTML file: {e}")
        return False

def main():
    """Main function"""
    print("Creating formatted HTML report for PDF conversion...")
    print("=" * 60)
    
    if create_html_report():
        print("\n" + "=" * 60)
        print("HTML REPORT CREATED SUCCESSFULLY!")
        print("=" * 60)
        print("\nTo convert to PDF:")
        print("1. Open 'A2_Report_Davidsons_1685.html' in your web browser")
        print("2. Press Ctrl+P (Windows) or Cmd+P (Mac)")
        print("3. In the print dialog:")
        print("   - Select 'Save as PDF' as destination")
        print("   - Set margins to 'Minimum' or 'None'")
        print("   - Enable 'Background graphics' for better formatting")
        print("   - Choose 'More settings' and select 'A4' paper size")
        print("4. Click 'Save' and name it 'A2_Davidsons_1685.pdf'")
        print("\nThe HTML file is professionally formatted and ready for conversion!")
    else:
        print("Failed to create HTML report.")

if __name__ == "__main__":
    main()
