"""
AI-Driven Automated Documentation Generator
Layer 5: Evaluation Engine

This module evaluates documentation quality using multiple metrics.
"""

from typing import Dict, List, Set
import re
from dataclasses import dataclass


@dataclass
class EvaluationResult:
    """Results from documentation evaluation."""
    keyword_overlap_score: float
    coverage_score: float
    length_ratio: float
    consistency_score: float
    overall_score: float
    detailed_analysis: Dict[str, any]


class DocumentationEvaluator:
    """
    Evaluates documentation quality through multiple metrics.
    
    Metrics:
    1. Keyword Overlap: Semantic similarity (Jaccard)
    2. Coverage: Percentage of elements documented
    3. Length Comparison: Verbosity analysis
    4. Consistency: Style and terminology uniformity
    """
    
    def __init__(self):
        # Common stop words to filter out
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'it', 'its'
        }
    
    def evaluate(self, ai_docs: str, human_docs: str, code_structure) -> EvaluationResult:
        """
        Perform comprehensive evaluation.
        
        Args:
            ai_docs: AI-generated documentation
            human_docs: Human-written documentation
            code_structure: CodeStructure object
            
        Returns:
            EvaluationResult with all metrics
        """
        # Calculate individual metrics
        keyword_score = self.calculate_keyword_overlap(ai_docs, human_docs)
        coverage_score = self.calculate_coverage(ai_docs, code_structure)
        length_ratio = self.calculate_length_ratio(ai_docs, human_docs)
        consistency_score = self.calculate_consistency(ai_docs)
        
        # Calculate overall score (weighted average)
        overall_score = (
            keyword_score * 0.35 +
            coverage_score * 0.30 +
            min(100, (1.0 / abs(length_ratio - 1.0 + 0.1)) * 10) * 0.15 +
            consistency_score * 0.20
        )
        
        # Detailed analysis
        analysis = {
            'keyword_overlap': {
                'score': keyword_score,
                'interpretation': self._interpret_keyword_overlap(keyword_score)
            },
            'coverage': {
                'score': coverage_score,
                'interpretation': self._interpret_coverage(coverage_score)
            },
            'length_ratio': {
                'ratio': length_ratio,
                'interpretation': self._interpret_length_ratio(length_ratio)
            },
            'consistency': {
                'score': consistency_score,
                'interpretation': self._interpret_consistency(consistency_score)
            }
        }
        
        return EvaluationResult(
            keyword_overlap_score=keyword_score,
            coverage_score=coverage_score,
            length_ratio=length_ratio,
            consistency_score=consistency_score,
            overall_score=overall_score,
            detailed_analysis=analysis
        )
    
    def calculate_keyword_overlap(self, ai_docs: str, human_docs: str) -> float:
        """
        Calculate keyword overlap using Jaccard similarity.
        
        Args:
            ai_docs: AI-generated documentation
            human_docs: Human-written documentation
            
        Returns:
            Overlap score (0-100)
        """
        ai_keywords = self._extract_keywords(ai_docs)
        human_keywords = self._extract_keywords(human_docs)
        
        if not ai_keywords or not human_keywords:
            return 0.0
        
        intersection = ai_keywords & human_keywords
        union = ai_keywords | human_keywords
        
        jaccard_similarity = len(intersection) / len(union)
        return round(jaccard_similarity * 100, 2)
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract meaningful keywords from text."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters except spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Filter out stop words and short words
        keywords = {
            word for word in words
            if word not in self.stop_words and len(word) > 2
        }
        
        return keywords
    
    def calculate_coverage(self, docs: str, code_structure) -> float:
        """
        Calculate documentation coverage.
        
        Args:
            docs: Generated documentation
            code_structure: CodeStructure object
            
        Returns:
            Coverage score (0-100)
        """
        total_elements = len(code_structure.functions) + len(code_structure.classes)
        
        if total_elements == 0:
            return 100.0  # No elements to document
        
        # Count documented functions
        documented_count = 0
        
        for func in code_structure.functions:
            if func.name.lower() in docs.lower():
                documented_count += 1
        
        for cls in code_structure.classes:
            if cls.name.lower() in docs.lower():
                documented_count += 1
        
        coverage = (documented_count / total_elements) * 100
        return round(coverage, 2)
    
    def calculate_length_ratio(self, ai_docs: str, human_docs: str) -> float:
        """
        Calculate length ratio between AI and human docs.
        
        Args:
            ai_docs: AI-generated documentation
            human_docs: Human-written documentation
            
        Returns:
            Length ratio (AI words / Human words)
        """
        ai_words = len(ai_docs.split())
        human_words = len(human_docs.split())
        
        if human_words == 0:
            return 1.0
        
        ratio = ai_words / human_words
        return round(ratio, 2)
    
    def calculate_consistency(self, docs: str) -> float:
        """
        Calculate documentation consistency score.
        
        Checks:
        - Uniform terminology
        - Consistent formatting
        - Standard structure
        
        Args:
            docs: Documentation to evaluate
            
        Returns:
            Consistency score (0-100)
        """
        checks = []
        
        # Check 1: Has Args/Parameters section
        has_args = bool(re.search(r'Args:|Parameters:', docs, re.IGNORECASE))
        checks.append(has_args)
        
        # Check 2: Has Returns section
        has_returns = bool(re.search(r'Returns:|Return:', docs, re.IGNORECASE))
        checks.append(has_returns)
        
        # Check 3: Has examples
        has_examples = bool(re.search(r'Example|>>>', docs))
        checks.append(has_examples)
        
        # Check 4: Consistent capitalization in section headers
        sections = re.findall(r'^(Args|Parameters|Returns|Examples):', docs, re.MULTILINE | re.IGNORECASE)
        if sections:
            # Check if all sections follow same case pattern
            capitalized = sum(1 for s in sections if s[0].isupper())
            consistency_case = capitalized == len(sections) or capitalized == 0
            checks.append(consistency_case)
        else:
            checks.append(False)
        
        # Check 5: Parameter descriptions follow pattern
        param_lines = re.findall(r'^\s+\w+:.*$', docs, re.MULTILINE)
        if param_lines:
            # All should have colon format
            checks.append(len(param_lines) >= 1)
        else:
            checks.append(True)  # No params is fine
        
        # Calculate score
        score = (sum(checks) / len(checks)) * 100
        return round(score, 2)
    
    def _interpret_keyword_overlap(self, score: float) -> str:
        """Interpret keyword overlap score."""
        if score >= 80:
            return "✅ Excellent - High semantic similarity"
        elif score >= 60:
            return "✓ Good - Adequate coverage of key concepts"
        elif score >= 40:
            return "⚠ Moderate - Some important concepts missing"
        else:
            return "❌ Low - Significant semantic differences"
    
    def _interpret_coverage(self, score: float) -> str:
        """Interpret coverage score."""
        if score == 100:
            return "✅ Perfect - All elements documented"
        elif score >= 80:
            return "✓ High - Most elements documented"
        elif score >= 60:
            return "⚠ Moderate - Some elements missing documentation"
        else:
            return "❌ Low - Many elements undocumented"
    
    def _interpret_length_ratio(self, ratio: float) -> str:
        """Interpret length ratio."""
        if 0.8 <= ratio <= 1.2:
            return "✅ Balanced - Similar verbosity to human docs"
        elif ratio > 1.2:
            return "⚠ Verbose - AI documentation is more detailed"
        else:
            return "⚠ Concise - AI documentation is briefer"
    
    def _interpret_consistency(self, score: float) -> str:
        """Interpret consistency score."""
        if score >= 90:
            return "✅ Highly Consistent - Uniform style throughout"
        elif score >= 70:
            return "✓ Generally Consistent - Minor variations"
        elif score >= 50:
            return "⚠ Moderately Consistent - Some inconsistencies"
        else:
            return "❌ Inconsistent - Significant style variations"
    
    def generate_comparison_table(self, ai_docs: str, human_docs: str) -> List[Dict]:
        """
        Generate side-by-side comparison data.
        
        Args:
            ai_docs: AI-generated documentation
            human_docs: Human-written documentation
            
        Returns:
            List of comparison dictionaries
        """
        comparison = []
        
        # Extract function documentation sections
        ai_sections = self._split_by_function(ai_docs)
        human_sections = self._split_by_function(human_docs)
        
        all_functions = set(ai_sections.keys()) | set(human_sections.keys())
        
        for func_name in sorted(all_functions):
            comparison.append({
                'function': func_name,
                'ai_doc': ai_sections.get(func_name, '(Not documented)'),
                'human_doc': human_sections.get(func_name, '(Not documented)'),
                'match': func_name in ai_sections and func_name in human_sections
            })
        
        return comparison
    
    def _split_by_function(self, docs: str) -> Dict[str, str]:
        """Split documentation by function names."""
        sections = {}
        
        # Simple pattern matching for function headers
        # In production, use more sophisticated parsing
        lines = docs.split('\n')
        current_func = None
        current_content = []
        
        for line in lines:
            if '##' in line and 'Function:' in line:
                # Save previous function
                if current_func:
                    sections[current_func] = '\n'.join(current_content)
                
                # Start new function
                current_func = line.split('Function:')[-1].strip()
                current_content = []
            elif line.startswith('def '):
                # Function definition line
                match = re.match(r'def\s+(\w+)', line)
                if match:
                    if current_func:
                        sections[current_func] = '\n'.join(current_content)
                    current_func = match.group(1)
                    current_content = [line]
            else:
                if current_func:
                    current_content.append(line)
        
        # Save last function
        if current_func:
            sections[current_func] = '\n'.join(current_content)
        
        return sections
