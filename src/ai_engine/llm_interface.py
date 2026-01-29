"""
AI-Driven Automated Documentation Generator
Layer 3: AI Inference

This module interfaces with AI models to generate documentation.
Supports both mock (template-based) and real API modes.
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
import re


@dataclass
class DocumentationOutput:
    """AI-generated documentation content."""
    function_name: str
    description: str
    param_descriptions: Dict[str, str]
    return_description: str
    examples: List[str]
    inline_comments: List[str]


class LLMInterface:
    """
    Interface for AI-based documentation generation.
    
    Supports two modes:
    1. Mock Mode (default): Template-based intelligent generation
    2. API Mode: OpenAI GPT integration
    """
    
    def __init__(self, use_api: bool = False, api_key: Optional[str] = None):
        """
        Initialize LLM interface.
        
        Args:
            use_api: Whether to use real API (True) or mock (False)
            api_key: OpenAI API key (required if use_api=True)
        """
        self.use_api = use_api
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if self.use_api and not self.api_key:
            print("Warning: API mode requested but no API key found. Falling back to mock mode.")
            self.use_api = False
    
    def generate_documentation(self, function_info) -> DocumentationOutput:
        """
        Generate documentation for a function.
        
        Args:
            function_info: FunctionInfo object from code parser
            
        Returns:
            DocumentationOutput with AI-generated content
        """
        if self.use_api:
            return self._generate_with_api(function_info)
        else:
            return self._generate_with_mock(function_info)
    
    def _generate_with_mock(self, func_info) -> DocumentationOutput:
        """
        Generate documentation using intelligent templates.
        
        This mock generator analyzes function names, parameters,
        and structure to create realistic documentation.
        """
        # Analyze function name for context
        name_parts = self._split_function_name(func_info.name)
        action = name_parts[0] if name_parts else "process"
        
        # Generate description based on name analysis
        description = self._generate_description(func_info.name, name_parts, func_info.params)
        
        # Generate parameter descriptions
        param_descriptions = {}
        for param in func_info.params:
            if param == 'self':
                continue
            param_descriptions[param] = self._generate_param_description(param, func_info.name)
        
        # Generate return description
        return_desc = self._generate_return_description(func_info.name, func_info.return_annotation)
        
        # Generate examples
        examples = self._generate_examples(func_info.name, func_info.params)
        
        # Generate inline comments suggestions
        inline_comments = self._generate_inline_comments(func_info)
        
        return DocumentationOutput(
            function_name=func_info.name,
            description=description,
            param_descriptions=param_descriptions,
            return_description=return_desc,
            examples=examples,
            inline_comments=inline_comments
        )
    
    def _split_function_name(self, name: str) -> List[str]:
        """Split snake_case or camelCase function name into parts."""
        # Handle snake_case
        if '_' in name:
            return name.split('_')
        # Handle camelCase
        parts = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\W|$)|\d+', name)
        return [p.lower() for p in parts]
    
    def _generate_description(self, func_name: str, name_parts: List[str], params: List[str]) -> str:
        """Generate function description based on name and parameters."""
        # Common action verbs and their descriptions
        action_templates = {
            'get': 'Retrieves',
            'set': 'Sets or updates',
            'calculate': 'Calculates',
            'compute': 'Computes',
            'process': 'Processes',
            'validate': 'Validates',
            'check': 'Checks',
            'find': 'Finds',
            'search': 'Searches for',
            'create': 'Creates',
            'generate': 'Generates',
            'build': 'Builds',
            'parse': 'Parses',
            'format': 'Formats',
            'convert': 'Converts',
            'transform': 'Transforms',
            'sort': 'Sorts',
            'filter': 'Filters',
            'load': 'Loads',
            'save': 'Saves',
            'delete': 'Deletes',
            'update': 'Updates',
            'add': 'Adds',
            'remove': 'Removes'
        }
        
        action = name_parts[0] if name_parts else 'process'
        action_desc = action_templates.get(action, f'{action.capitalize()}s')
        
        # Build object description from remaining name parts
        if len(name_parts) > 1:
            obj = ' '.join(name_parts[1:])
            description = f"{action_desc} {obj}"
        else:
            description = f"{action_desc} the input data"
        
        # Add parameter context if relevant
        if len([p for p in params if p != 'self']) > 2:
            description += " with multiple parameters"
        
        description += "."
        
        # Add detailed explanation
        detailed = f"\n\nThis function performs {action} operations"
        if len(name_parts) > 1:
            detailed += f" on {' '.join(name_parts[1:])}"
        detailed += ". It is designed to handle various input scenarios and provide reliable results."
        
        return description + detailed
    
    def _generate_param_description(self, param: str, func_name: str) -> str:
        """Generate parameter description based on name."""
        # Common parameter name patterns
        param_lower = param.lower()
        
        if param_lower in ['data', 'input', 'value']:
            return f"The input {param} to be processed"
        elif param_lower in ['name', 'filename', 'file']:
            return f"The {param} of the file or resource"
        elif param_lower in ['path', 'filepath']:
            return f"The {param} to the file or directory"
        elif param_lower in ['key', 'id', 'identifier']:
            return f"Unique {param} for identification"
        elif param_lower in ['options', 'config', 'settings']:
            return f"Configuration {param} for the operation"
        elif param_lower in ['items', 'list', 'array']:
            return f"Collection of {param} to process"
        elif 'count' in param_lower or 'num' in param_lower or 'size' in param_lower:
            return f"The {param} specifying quantity"
        elif 'flag' in param_lower or 'enable' in param_lower or param_lower.startswith('is_'):
            return f"Boolean flag indicating whether to {param.replace('is_', '').replace('_', ' ')}"
        else:
            return f"The {param} parameter"
    
    def _generate_return_description(self, func_name: str, return_annotation: Optional[str]) -> str:
        """Generate return value description."""
        if return_annotation:
            if 'bool' in return_annotation.lower():
                return "Boolean value indicating success or validation result"
            elif 'int' in return_annotation.lower():
                return "Integer value representing the computed result or count"
            elif 'str' in return_annotation.lower():
                return "String containing the processed or formatted output"
            elif 'list' in return_annotation.lower() or 'List' in return_annotation:
                return "List of processed items or results"
            elif 'dict' in return_annotation.lower() or 'Dict' in return_annotation:
                return "Dictionary containing structured result data"
            else:
                return f"{return_annotation} object with the result"
        else:
            # Infer from function name
            if func_name.startswith('is_') or func_name.startswith('has_') or func_name.startswith('check_'):
                return "Boolean value indicating the validation result"
            elif func_name.startswith('get_') or func_name.startswith('find_'):
                return "The requested data or resource"
            elif func_name.startswith('calculate_') or func_name.startswith('compute_'):
                return "The calculated numerical result"
            else:
                return "The processed result of the operation"
    
    def _generate_examples(self, func_name: str, params: List[str]) -> List[str]:
        """Generate usage examples."""
        non_self_params = [p for p in params if p != 'self']
        
        if not non_self_params:
            return [f">>> {func_name}()", "result"]
        
        # Generate sample parameter values
        example_values = []
        for param in non_self_params:
            param_lower = param.lower()
            if 'name' in param_lower or 'str' in param_lower:
                example_values.append(f'"{param}_value"')
            elif 'num' in param_lower or 'count' in param_lower or 'size' in param_lower:
                example_values.append('10')
            elif 'list' in param_lower or 'items' in param_lower:
                example_values.append('[1, 2, 3]')
            elif 'dict' in param_lower or 'data' in param_lower:
                example_values.append('{"key": "value"}')
            elif param_lower.startswith('is_') or 'flag' in param_lower:
                example_values.append('True')
            else:
                example_values.append(f'{param}_value')
        
        example_call = f">>> {func_name}({', '.join(example_values)})"
        return [example_call, "expected_result"]
    
    def _generate_inline_comments(self, func_info) -> List[str]:
        """Generate suggestions for inline comments."""
        comments = []
        
        if len(func_info.params) > 1:
            comments.append("# Validate input parameters")
        
        comments.append("# Perform main operation")
        
        if 'return' in func_info.body.lower() or func_info.return_annotation:
            comments.append("# Return processed result")
        
        return comments
    
    def _generate_with_api(self, func_info) -> DocumentationOutput:
        """
        Generate documentation using OpenAI API.
        
        Note: This is a placeholder for real API integration.
        Implement if API key is available.
        """
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = self._create_prompt(func_info)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a technical documentation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse response (simplified)
            content = response.choices[0].message.content
            return self._parse_api_response(content, func_info)
            
        except Exception as e:
            print(f"API call failed: {e}. Falling back to mock mode.")
            return self._generate_with_mock(func_info)
    
    def _create_prompt(self, func_info) -> str:
        """Create prompt for API-based generation."""
        prompt = f"""Generate comprehensive documentation for this Python function:

Function Name: {func_info.name}
Parameters: {', '.join(func_info.params)}
Return Type: {func_info.return_annotation or 'Not specified'}

Provide:
1. Brief description (1-2 sentences)
2. Parameter descriptions
3. Return value description
4. Usage example

Format as Google-style docstring."""
        return prompt
    
    def _parse_api_response(self, response: str, func_info) -> DocumentationOutput:
        """Parse API response into DocumentationOutput format."""
        # Simplified parsing - in production, use more robust parsing
        return DocumentationOutput(
            function_name=func_info.name,
            description=response[:200],  # First part as description
            param_descriptions={p: f"Description of {p}" for p in func_info.params if p != 'self'},
            return_description="Return value description",
            examples=[">>> example()", "result"],
            inline_comments=["# Main operation"]
        )
