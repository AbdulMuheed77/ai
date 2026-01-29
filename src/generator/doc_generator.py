"""
AI-Driven Automated Documentation Generator
Layer 4: Documentation Generator

This module formats AI-generated content into standardized documentation.
"""

from typing import Dict, List


class DocumentationGenerator:
    """
    Formats AI-generated documentation into standard formats.
    
    Supports Google-style and NumPy-style docstrings.
    Ensures PEP 257 compliance.
    """
    
    def __init__(self, style: str = 'google'):
        """
        Initialize documentation generator.
        
        Args:
            style: Docstring style ('google' or 'numpy')
        """
        self.style = style.lower()
    
    def generate_function_docs(self, func_info, ai_output) -> str:
        """
        Generate complete function documentation.
        
        Args:
            func_info: FunctionInfo from code parser
            ai_output: DocumentationOutput from AI engine
            
        Returns:
            Formatted docstring
        """
        if self.style == 'google':
            return self._format_google_style(func_info, ai_output)
        elif self.style == 'numpy':
            return self._format_numpy_style(func_info, ai_output)
        else:
            return self._format_google_style(func_info, ai_output)
    
    def _format_google_style(self, func_info, ai_output) -> str:
        """Format documentation in Google style."""
        lines = []
        
        # Brief description (first line)
        brief = ai_output.description.split('\n')[0]
        lines.append(f'"""{brief}')
        lines.append('')
        
        # Detailed description (if available)
        detailed_parts = ai_output.description.split('\n')[1:]
        if detailed_parts:
            for part in detailed_parts:
                if part.strip():
                    lines.append(part.strip())
            lines.append('')
        
        # Parameters section
        params = [p for p in func_info.params if p != 'self']
        if params:
            lines.append('Args:')
            for param in params:
                param_desc = ai_output.param_descriptions.get(param, f'The {param} parameter')
                lines.append(f'    {param}: {param_desc}')
            lines.append('')
        
        # Returns section
        if func_info.return_annotation or ai_output.return_description:
            lines.append('Returns:')
            lines.append(f'    {ai_output.return_description}')
            lines.append('')
        
        # Examples section
        if ai_output.examples:
            lines.append('Examples:')
            for example in ai_output.examples:
                lines.append(f'    {example}')
            lines.append('')
        
        # Close docstring
        lines.append('"""')
        
        return '\n'.join(lines)
    
    def _format_numpy_style(self, func_info, ai_output) -> str:
        """Format documentation in NumPy style."""
        lines = []
        
        # Brief description
        brief = ai_output.description.split('\n')[0]
        lines.append(f'"""{brief}')
        lines.append('')
        
        # Detailed description
        detailed_parts = ai_output.description.split('\n')[1:]
        if detailed_parts:
            for part in detailed_parts:
                if part.strip():
                    lines.append(part.strip())
            lines.append('')
        
        # Parameters section
        params = [p for p in func_info.params if p != 'self']
        if params:
            lines.append('Parameters')
            lines.append('----------')
            for param in params:
                param_desc = ai_output.param_descriptions.get(param, f'The {param} parameter')
                lines.append(f'{param} : type')
                lines.append(f'    {param_desc}')
            lines.append('')
        
        # Returns section
        if func_info.return_annotation or ai_output.return_description:
            lines.append('Returns')
            lines.append('-------')
            return_type = func_info.return_annotation or 'type'
            lines.append(return_type)
            lines.append(f'    {ai_output.return_description}')
            lines.append('')
        
        # Examples section
        if ai_output.examples:
            lines.append('Examples')
            lines.append('--------')
            for example in ai_output.examples:
                lines.append(example)
            lines.append('')
        
        lines.append('"""')
        
        return '\n'.join(lines)
    
    def generate_inline_comments(self, code: str, ai_suggestions: List[str]) -> str:
        """
        Add inline comments to code.
        
        Args:
            code: Original code string
            ai_suggestions: List of comment suggestions
            
        Returns:
            Code with inline comments added
        """
        lines = code.split('\n')
        
        # Simple strategy: add comments at strategic points
        # In production, use AST to identify precise insertion points
        
        commented_lines = []
        suggestion_index = 0
        
        for i, line in enumerate(lines):
            # Add comment before function body
            if 'def ' in line and suggestion_index < len(ai_suggestions):
                commented_lines.append(line)
                if i + 1 < len(lines):
                    indent = len(lines[i + 1]) - len(lines[i + 1].lstrip())
                    commented_lines.append(' ' * indent + ai_suggestions[suggestion_index])
                    suggestion_index += 1
            else:
                commented_lines.append(line)
        
        return '\n'.join(commented_lines)
    
    def generate_module_docs(self, code_structure, project_name: str = "Module") -> str:
        """
        Generate module-level documentation.
        
        Args:
            code_structure: CodeStructure from parser
            project_name: Name of the module/project
            
        Returns:
            Module docstring
        """
        lines = []
        lines.append(f'"""')
        lines.append(f'{project_name}')
        lines.append('')
        lines.append('This module provides the following functionality:')
        lines.append('')
        
        # List functions
        if code_structure.functions:
            lines.append('Functions:')
            for func in code_structure.functions:
                brief = func.docstring.split('\n')[0] if func.docstring else 'Function'
                lines.append(f'    {func.name}: {brief}')
            lines.append('')
        
        # List classes
        if code_structure.classes:
            lines.append('Classes:')
            for cls in code_structure.classes:
                brief = cls.docstring.split('\n')[0] if cls.docstring else 'Class'
                lines.append(f'    {cls.name}: {brief}')
            lines.append('')
        
        lines.append('"""')
        
        return '\n'.join(lines)
    
    def format_output(self, all_docs: Dict[str, str]) -> str:
        """
        Combine all documentation into final output.
        
        Args:
            all_docs: Dictionary mapping function names to docstrings
            
        Returns:
            Complete formatted documentation
        """
        output = []
        
        output.append("# Generated Documentation\n")
        output.append("=" * 60)
        output.append("")
        
        for func_name, docstring in all_docs.items():
            output.append(f"## Function: {func_name}")
            output.append("")
            output.append(docstring)
            output.append("")
            output.append("-" * 60)
            output.append("")
        
        return '\n'.join(output)
