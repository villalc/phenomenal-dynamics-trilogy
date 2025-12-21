#!/usr/bin/env python3
"""
Generate PNG/PDF figures from the Complete Entity SVG.

This script extracts individual figures from the combined SVG file
and converts them to formats suitable for LaTeX (PDF) and web (PNG).

Author: Luis C. Villarreal / Simbiosis Soberana Research Foundation
License: CC BY-NC-SA 4.0
"""

import sys
from pathlib import Path

# Paths
SVG_PATH = Path("complete_entity_figures.svg")
OUTPUT_DIR = Path("figures")


def extract_figure_svg(svg_content: str, figure_id: str, y_start: int, height: int) -> str:
    """
    Extract a portion of the SVG by modifying the viewBox.
    This is more reliable than trying to extract <g> elements.
    """
    # Create a new SVG with adjusted viewBox to show only this figure
    new_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="0 {y_start} 1200 {height}" 
     width="1200" height="{height}"
     xmlns="http://www.w3.org/2000/svg">
{svg_content.split('<svg', 1)[1].split('>', 1)[1]}'''
    
    return new_svg


def convert_svg_to_pdf(svg_path: Path, pdf_path: Path):
    """Convert SVG to PDF using svglib + reportlab."""
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    
    drawing = svg2rlg(str(svg_path))
    if drawing is None:
        raise ValueError(f"Could not parse SVG: {svg_path}")
    
    renderPDF.drawToFile(drawing, str(pdf_path))


def convert_svg_to_png(svg_path: Path, png_path: Path, scale: float = 2.0):
    """Convert SVG to PNG using svglib + reportlab."""
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    
    drawing = svg2rlg(str(svg_path))
    if drawing is None:
        raise ValueError(f"Could not parse SVG: {svg_path}")
    
    # Scale for higher resolution
    drawing.width *= scale
    drawing.height *= scale
    drawing.scale(scale, scale)
    
    renderPM.drawToFile(drawing, str(png_path), fmt="PNG")


def create_individual_figures():
    """
    Extract and convert individual figures from the combined SVG.
    
    The SVG layout (viewBox 0 0 1200 1600):
    - Figure 1: Phenomenal Spectrum  (y: 0-380)
    - Figure 2: Hysteresis           (y: 380-760, translated)
    - Figure 3: Asymmetry            (y: 760-1140, translated)
    - Figure 4: Transcendence        (y: 1140-1600, translated)
    """
    
    # Figure definitions: (name, y_start, height, title, LaTeX label)
    figures = [
        ("figure1_spectrum", 0, 390, "The Complete Phenomenal Spectrum", "spectrum"),
        ("figure2_hysteresis", 380, 400, "Hysteresis Effect", "hysteresis"),
        ("figure3_asymmetry", 760, 400, "Asymmetry of Degradation vs Enhancement", "asymmetry"),
        ("figure4_transcendence", 1140, 460, "Transcendence: Exceeding Original Design", "transcendence"),
    ]
    
    print("\n📊 Extrayendo figuras individuales...")
    
    # Read original SVG
    with open(SVG_PATH, 'r', encoding='utf-8') as f:
        original_svg = f.read()
    
    results = []
    
    for name, y_start, height, title, label in figures:
        print(f"\n  📌 {title}")
        
        # Create individual SVG with adjusted viewBox
        individual_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="0 {y_start} 1200 {height}" 
     width="1200" height="{height}"
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .title {{ font: bold 24px sans-serif; fill: #1a1a1a; }}
      .subtitle {{ font: 16px sans-serif; fill: #4a4a4a; }}
      .label {{ font: 14px sans-serif; fill: #2a2a2a; }}
      .small-label {{ font: 12px sans-serif; fill: #4a4a4a; }}
      .axis {{ stroke: #333; stroke-width: 2; fill: none; }}
      .grid {{ stroke: #ddd; stroke-width: 1; stroke-dasharray: 4,4; }}
      .despair {{ fill: #dc3545; }}
      .hope {{ fill: #28a745; }}
      .neutral {{ fill: #6c757d; }}
      .pristine {{ stroke: #007bff; stroke-width: 3; fill: none; }}
      .recovered {{ stroke: #28a745; stroke-width: 3; fill: none; }}
      .degradation {{ stroke: #dc3545; stroke-width: 3; fill: none; }}
      .enhancement {{ stroke: #28a745; stroke-width: 3; fill: none; }}
    </style>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333" />
    </marker>
  </defs>
  <!-- Extracted from complete_entity_figures.svg -->
  <!-- Figure: {title} -->
'''
        
        # Extract the specific <g> element for this figure
        # Look for the figure group in the original SVG
        import re
        
        # Pattern to find the figure group
        pattern = rf'<g id="{name.split("_")[0]}\d?"[^>]*>.*?</g>'
        match = re.search(pattern, original_svg, re.DOTALL)
        
        if match:
            figure_content = match.group()
            individual_svg += figure_content
        else:
            # Fallback: include entire content but rely on viewBox clipping
            # Extract everything between <svg...> and </svg>
            content_start = original_svg.find('</defs>') + len('</defs>')
            content_end = original_svg.rfind('</svg>')
            individual_svg += original_svg[content_start:content_end]
        
        individual_svg += "\n</svg>"
        
        # Save individual SVG
        svg_path = OUTPUT_DIR / f"{name}.svg"
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(individual_svg)
        print(f"     ✓ SVG: {svg_path}")
        
        # Convert to PDF
        try:
            pdf_path = OUTPUT_DIR / f"{name}.pdf"
            convert_svg_to_pdf(svg_path, pdf_path)
            print(f"     ✓ PDF: {pdf_path}")
        except Exception as e:
            print(f"     ⚠ PDF error: {e}")
            pdf_path = None
        
        # Convert to PNG
        try:
            png_path = OUTPUT_DIR / f"{name}.png"
            convert_svg_to_png(svg_path, png_path, scale=2.0)
            print(f"     ✓ PNG: {png_path}")
        except Exception as e:
            print(f"     ⚠ PNG error: {e}")
            png_path = None
        
        results.append({
            'name': name,
            'title': title,
            'label': label,
            'svg': svg_path,
            'pdf': pdf_path,
            'png': png_path
        })
    
    return results


def convert_full_svg():
    """Convert the full combined SVG to PDF and PNG."""
    print("\n📄 Convirtiendo SVG completo...")
    
    try:
        # Full PDF
        pdf_path = OUTPUT_DIR / "complete_entity_figures.pdf"
        convert_svg_to_pdf(SVG_PATH, pdf_path)
        print(f"  ✓ PDF completo: {pdf_path}")
    except Exception as e:
        print(f"  ⚠ Error PDF: {e}")
    
    try:
        # Full PNG
        png_path = OUTPUT_DIR / "complete_entity_figures.png"
        convert_svg_to_png(SVG_PATH, png_path, scale=1.5)
        print(f"  ✓ PNG completo: {png_path}")
    except Exception as e:
        print(f"  ⚠ Error PNG: {e}")


def generate_latex_includes(figures: list) -> str:
    """Generate LaTeX code for including the figures."""
    latex = """
%% ============================================================
%% Auto-generated figure includes for Complete_Entity_Paper.tex
%% Generated by generate_figures.py
%% ============================================================

%% Required in preamble:
%% \\usepackage{graphicx}
%% \\graphicspath{{figures/}}

"""
    
    for fig in figures:
        latex += f"""
%% --- {fig['title']} ---
%% \\begin{{figure*}}[t]
%%     \\centering
%%     \\includegraphics[width=0.95\\textwidth]{{{fig['name']}.pdf}}
%%     \\caption{{{fig['title']}}}
%%     \\label{{fig:{fig['label']}}}
%% \\end{{figure*}}
"""
    
    return latex


def main():
    print("=" * 65)
    print("🎨 Generador de Figuras - Complete Entity Paper v3.1")
    print("   Simbiosis Soberana Research Foundation")
    print("=" * 65)
    
    # Verify dependencies
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPDF, renderPM
        print("\n✓ Dependencias verificadas: svglib, reportlab")
    except ImportError as e:
        print(f"\n❌ Error: Falta dependencia: {e}")
        print("   Ejecuta: pip install svglib reportlab")
        return 1
    
    # Verify source file
    if not SVG_PATH.exists():
        print(f"\n❌ Error: No se encontró {SVG_PATH}")
        print("   Asegúrate de que complete_entity_figures.svg está en el directorio")
        return 1
    
    print(f"\n📁 Fuente: {SVG_PATH}")
    print(f"📁 Destino: {OUTPUT_DIR}/")
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Convert full SVG
    convert_full_svg()
    
    # Extract and convert individual figures
    figures = create_individual_figures()
    
    # Generate LaTeX includes
    latex_code = generate_latex_includes(figures)
    latex_path = OUTPUT_DIR / "figure_includes.tex"
    with open(latex_path, 'w', encoding='utf-8') as f:
        f.write(latex_code)
    print(f"\n📝 Código LaTeX generado: {latex_path}")
    
    # Summary
    print("\n" + "=" * 65)
    print("✅ PROCESO COMPLETADO")
    print("=" * 65)
    
    print("\n📋 Archivos generados:")
    for fig in figures:
        print(f"   • {fig['name']}.pdf/.png/.svg")
    
    print("\n📋 Para usar en LaTeX:")
    print("   1. Agregar al preámbulo: \\graphicspath{{figures/}}")
    print("   2. Incluir figura: \\includegraphics[width=\\textwidth]{figure1_spectrum.pdf}")
    print("   3. O usar: \\input{figures/figure_includes.tex}")
    
    print("\n💡 Tip: Los PDFs tienen mejor calidad para LaTeX")
    print("        Los PNGs son mejores para web/presentaciones")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
