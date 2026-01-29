"""
AI-Driven Automated Documentation Generator
Command-Line Interface (Optional)

Alternative entry point for CLI usage.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from preprocessing.code_parser import CodeParser
from ai_engine.llm_interface import LLMInterface
from generator.doc_generator import DocumentationGenerator
from evaluation.evaluator import DocumentationEvaluator
from output.formatter import OutputFormatter


def main():
    """CLI main function."""
    # Configure stdout for UTF-8 encoding (Windows compatibility)
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("AI-Driven Automated Documentation Generator")
    print("=" * 60)
    print()
    
    # Load sample code
    print("📂 Loading sample code...")
    with open('data/sample_code.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    print(f"✅ Loaded {len(code.split(chr(10)))} lines of code")
    print()
    
    # Parse code
    print("🔍 Parsing code structure...")
    parser = CodeParser()
    code_structure = parser.get_structure(code)
    
    if not code_structure.is_valid:
        print(f"❌ Error: {code_structure.error_message}")
        return
    
    print(f"✅ Found {len(code_structure.functions)} functions, {len(code_structure.classes)} classes")
    print()
    
    # Generate documentation
    print("🤖 Generating AI documentation...")
    llm = LLMInterface(use_api=False)
    doc_gen = DocumentationGenerator(style='google')
    
    all_docs = {}
    for func in code_structure.functions:
        ai_output = llm.generate_documentation(func)
        docstring = doc_gen.generate_function_docs(func, ai_output)
        all_docs[func.name] = docstring
        print(f"  ✓ Documented: {func.name}()")
    
    ai_docs = doc_gen.format_output(all_docs)
    print()
    print("✅ Documentation generated!")
    print()
    
    # Save to file
    output_file = 'generated_documentation.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ai_docs)
    
    print(f"💾 Saved to: {output_file}")
    print()
    print("=" * 60)
    print("✨ Complete! Run 'streamlit run app.py' for full UI experience")
    print("=" * 60)


if __name__ == "__main__":
    main()
