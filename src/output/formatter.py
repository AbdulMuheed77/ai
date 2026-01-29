"""
AI-Driven Automated Documentation Generator
Layer 6: Output Layer

This module formats results for presentation in the UI.
"""

from typing import Dict, List, Any
import json


class OutputFormatter:
    """
    Formats evaluation results and documentation for display.
    
    Prepares data for UI visualization and export.
    """
    
    def __init__(self):
        pass
    
    def format_comparison(self, ai_docs: str, human_docs: str, 
                          comparison_data: List[Dict]) -> Dict[str, Any]:
        """
        Format side-by-side comparison.
        
        Args:
            ai_docs: AI-generated documentation
            human_docs: Human-written documentation
            comparison_data: Comparison data from evaluator
            
        Returns:
            Formatted comparison dictionary
        """
        return {
            'ai_documentation': ai_docs,
            'human_documentation': human_docs,
            'function_comparisons': comparison_data,
            'summary': {
                'total_functions': len(comparison_data),
                'both_documented': sum(1 for item in comparison_data if item['match']),
                'only_ai': sum(1 for item in comparison_data 
                              if item['ai_doc'] != '(Not documented)' and item['human_doc'] == '(Not documented)'),
                'only_human': sum(1 for item in comparison_data 
                                 if item['human_doc'] != '(Not documented)' and item['ai_doc'] == '(Not documented)')
            }
        }
    
    def generate_report(self, eval_result, code_structure) -> str:
        """
        Generate detailed evaluation report.
        
        Args:
            eval_result: EvaluationResult object
            code_structure: CodeStructure object
            
        Returns:
            Formatted markdown report
        """
        lines = []
        
        lines.append("# Documentation Evaluation Report")
        lines.append("")
        lines.append("## Overall Score")
        lines.append(f"**{eval_result.overall_score:.1f}/100**")
        lines.append("")
        
        # Score interpretation
        if eval_result.overall_score >= 85:
            lines.append("🏆 **Excellent** - AI documentation quality is outstanding")
        elif eval_result.overall_score >= 70:
            lines.append("✅ **Good** - AI documentation quality is solid")
        elif eval_result.overall_score >= 55:
            lines.append("⚠️ **Fair** - AI documentation quality is acceptable but has room for improvement")
        else:
            lines.append("❌ **Needs Improvement** - AI documentation quality requires significant enhancement")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Individual metrics
        lines.append("## Individual Metrics")
        lines.append("")
        
        # Keyword Overlap
        lines.append("### 1. Keyword Overlap Score")
        lines.append(f"**Score:** {eval_result.keyword_overlap_score:.1f}%")
        lines.append(f"**Assessment:** {eval_result.detailed_analysis['keyword_overlap']['interpretation']}")
        lines.append("")
        lines.append("*Measures semantic similarity between AI and human documentation using Jaccard similarity.*")
        lines.append("")
        
        # Coverage
        lines.append("### 2. Coverage Score")
        lines.append(f"**Score:** {eval_result.coverage_score:.1f}%")
        lines.append(f"**Assessment:** {eval_result.detailed_analysis['coverage']['interpretation']}")
        lines.append("")
        total_elements = len(code_structure.functions) + len(code_structure.classes)
        lines.append(f"*Documented {int(eval_result.coverage_score * total_elements / 100)} out of {total_elements} code elements.*")
        lines.append("")
        
        # Length Ratio
        lines.append("### 3. Length Comparison")
        lines.append(f"**Ratio:** {eval_result.length_ratio:.2f}")
        lines.append(f"**Assessment:** {eval_result.detailed_analysis['length_ratio']['interpretation']}")
        lines.append("")
        lines.append("*Compares verbosity (AI word count / Human word count). Ideal range: 0.8-1.2*")
        lines.append("")
        
        # Consistency
        lines.append("### 4. Consistency Score")
        lines.append(f"**Score:** {eval_result.consistency_score:.1f}%")
        lines.append(f"**Assessment:** {eval_result.detailed_analysis['consistency']['interpretation']}")
        lines.append("")
        lines.append("*Evaluates uniformity of style, formatting, and terminology.*")
        lines.append("")
        
        lines.append("---")
        lines.append("")
        
        # Code Statistics
        lines.append("## Code Statistics")
        lines.append("")
        lines.append(f"- **Total Lines:** {code_structure.total_lines}")
        lines.append(f"- **Functions:** {len(code_structure.functions)}")
        lines.append(f"- **Classes:** {len(code_structure.classes)}")
        lines.append("")
        
        return '\n'.join(lines)
    
    def create_visualization_data(self, eval_result) -> Dict[str, Any]:
        """
        Prepare data for UI visualizations (charts, gauges).
        
        Args:
            eval_result: EvaluationResult object
            
        Returns:
            Dictionary with visualization-ready data
        """
        return {
            'metrics': [
                {
                    'name': 'Keyword Overlap',
                    'value': eval_result.keyword_overlap_score,
                    'max': 100,
                    'color': self._get_color(eval_result.keyword_overlap_score)
                },
                {
                    'name': 'Coverage',
                    'value': eval_result.coverage_score,
                    'max': 100,
                    'color': self._get_color(eval_result.coverage_score)
                },
                {
                    'name': 'Consistency',
                    'value': eval_result.consistency_score,
                    'max': 100,
                    'color': self._get_color(eval_result.consistency_score)
                }
            ],
            'overall': {
                'score': eval_result.overall_score,
                'color': self._get_color(eval_result.overall_score),
                'label': self._get_label(eval_result.overall_score)
            },
            'length_ratio': {
                'value': eval_result.length_ratio,
                'ideal_min': 0.8,
                'ideal_max': 1.2,
                'status': 'ideal' if 0.8 <= eval_result.length_ratio <= 1.2 else 'warning'
            }
        }
    
    def _get_color(self, score: float) -> str:
        """Get color based on score."""
        if score >= 80:
            return 'green'
        elif score >= 60:
            return 'yellow'
        elif score >= 40:
            return 'orange'
        else:
            return 'red'
    
    def _get_label(self, score: float) -> str:
        """Get label based on score."""
        if score >= 85:
            return 'Excellent'
        elif score >= 70:
            return 'Good'
        elif score >= 55:
            return 'Fair'
        else:
            return 'Needs Improvement'
    
    def export_json(self, all_data: Dict[str, Any], filepath: str) -> bool:
        """
        Export results to JSON file.
        
        Args:
            all_data: Complete data to export
            filepath: Output file path
            
        Returns:
            Success status
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    def format_metric_cards(self, eval_result) -> List[Dict[str, str]]:
        """
        Format metrics as card data for UI.
        
        Args:
            eval_result: EvaluationResult object
            
        Returns:
            List of card dictionaries
        """
        return [
            {
                'title': 'Keyword Overlap',
                'value': f"{eval_result.keyword_overlap_score:.1f}%",
                'description': 'Semantic similarity between AI and human docs',
                'interpretation': eval_result.detailed_analysis['keyword_overlap']['interpretation'],
                'icon': '🔤'
            },
            {
                'title': 'Coverage Score',
                'value': f"{eval_result.coverage_score:.1f}%",
                'description': 'Percentage of code elements documented',
                'interpretation': eval_result.detailed_analysis['coverage']['interpretation'],
                'icon': '📊'
            },
            {
                'title': 'Length Ratio',
                'value': f"{eval_result.length_ratio:.2f}x",
                'description': 'AI verbosity compared to human docs',
                'interpretation': eval_result.detailed_analysis['length_ratio']['interpretation'],
                'icon': '📏'
            },
            {
                'title': 'Consistency',
                'value': f"{eval_result.consistency_score:.1f}%",
                'description': 'Uniformity of style and formatting',
                'interpretation': eval_result.detailed_analysis['consistency']['interpretation'],
                'icon': '✨'
            },
            {
                'title': 'Overall Score',
                'value': f"{eval_result.overall_score:.1f}/100",
                'description': 'Weighted average of all metrics',
                'interpretation': self._get_label(eval_result.overall_score),
                'icon': '🎯'
            }
        ]
