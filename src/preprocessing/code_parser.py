"""
AI-Driven Automated Documentation Generator
Layer 2: Input & Preprocessing

This module handles code validation, parsing, and structure extraction.
"""

import ast
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class FunctionInfo:
    """Information about a function extracted from code."""
    name: str
    params: List[str]
    return_annotation: Optional[str]
    docstring: Optional[str]
    line_start: int
    line_end: int
    body: str


@dataclass
class ClassInfo:
    """Information about a class extracted from code."""
    name: str
    methods: List[FunctionInfo]
    docstring: Optional[str]
    line_start: int
    line_end: int


@dataclass
class CodeStructure:
    """Complete code structure representation."""
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    module_docstring: Optional[str]
    total_lines: int
    is_valid: bool
    error_message: Optional[str] = None


class CodeParser:
    """
    Parses and validates Python source code.
    
    This class implements Layer 2 of the architecture, providing
    code validation and structure extraction using Python's AST module.
    """
    
    def __init__(self):
        self.tree = None
        self.source_lines = []
    
    def validate_syntax(self, code: str) -> tuple[bool, Optional[str]]:
        """
        Validate Python syntax.
        
        Args:
            code: Python source code as string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            self.tree = ast.parse(code)
            self.source_lines = code.split('\n')
            return True, None
        except SyntaxError as e:
            error_msg = f"Syntax error at line {e.lineno}: {e.msg}"
            return False, error_msg
        except Exception as e:
            return False, str(e)
    
    def extract_functions(self, code: str) -> List[FunctionInfo]:
        """
        Extract all function definitions from code.
        
        Args:
            code: Python source code
            
        Returns:
            List of FunctionInfo objects
        """
        if not self.tree:
            is_valid, error = self.validate_syntax(code)
            if not is_valid:
                return []
        
        functions = []
        # Find all function definitions at module level (not inside classes)
        for node in self.tree.body:
            if isinstance(node, ast.FunctionDef):
                func_info = self._parse_function(node, code)
                functions.append(func_info)
        
        return functions
    
    def extract_classes(self, code: str) -> List[ClassInfo]:
        """
        Extract all class definitions from code.
        
        Args:
            code: Python source code
            
        Returns:
            List of ClassInfo objects
        """
        if not self.tree:
            is_valid, error = self.validate_syntax(code)
            if not is_valid:
                return []
        
        classes = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                class_info = self._parse_class(node, code)
                classes.append(class_info)
        
        return classes
    
    def get_structure(self, code: str) -> CodeStructure:
        """
        Get complete code structure.
        
        Args:
            code: Python source code
            
        Returns:
            CodeStructure object with all information
        """
        is_valid, error_msg = self.validate_syntax(code)
        
        if not is_valid:
            return CodeStructure(
                functions=[],
                classes=[],
                module_docstring=None,
                total_lines=len(code.split('\n')),
                is_valid=False,
                error_message=error_msg
            )
        
        functions = self.extract_functions(code)
        classes = self.extract_classes(code)
        module_docstring = ast.get_docstring(self.tree)
        
        return CodeStructure(
            functions=functions,
            classes=classes,
            module_docstring=module_docstring,
            total_lines=len(self.source_lines),
            is_valid=True
        )
    
    def _parse_function(self, node: ast.FunctionDef, code: str) -> FunctionInfo:
        """Parse AST FunctionDef node into FunctionInfo."""
        params = [arg.arg for arg in node.args.args]
        
        return_annotation = None
        if node.returns:
            return_annotation = ast.unparse(node.returns)
        
        docstring = ast.get_docstring(node)
        
        # Extract function body
        lines = code.split('\n')
        body_lines = lines[node.lineno - 1:node.end_lineno]
        body = '\n'.join(body_lines)
        
        return FunctionInfo(
            name=node.name,
            params=params,
            return_annotation=return_annotation,
            docstring=docstring,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            body=body
        )
    
    def _parse_class(self, node: ast.ClassDef, code: str) -> ClassInfo:
        """Parse AST ClassDef node into ClassInfo."""
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._parse_function(item, code)
                methods.append(method_info)
        
        docstring = ast.get_docstring(node)
        
        return ClassInfo(
            name=node.name,
            methods=methods,
            docstring=docstring,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno
        )
    
    def count_lines(self, code: str) -> Dict[str, int]:
        """
        Count various line metrics.
        
        Args:
            code: Python source code
            
        Returns:
            Dictionary with line counts
        """
        lines = code.split('\n')
        total = len(lines)
        blank = sum(1 for line in lines if not line.strip())
        comments = sum(1 for line in lines if line.strip().startswith('#'))
        
        return {
            'total': total,
            'blank': blank,
            'comments': comments,
            'code': total - blank - comments
        }
