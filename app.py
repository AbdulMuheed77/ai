"""
AI-Driven Automated Documentation Generator  
Main Streamlit Application (Layer 1: UI)

A university-grade SDA project with professional UI.
"""

import streamlit as st
import sys
import os
import json

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from preprocessing.code_parser import CodeParser
from ai_engine.llm_interface import LLMInterface
from generator.doc_generator import DocumentationGenerator
from evaluation.evaluator import DocumentationEvaluator
from output.formatter import OutputFormatter


# Page configuration
st.set_page_config(
    page_title="AI Documentation Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid var(--primary-color);
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .metric-card h3 {
        color: #1f2937;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--primary-color);
        margin: 0;
    }
    
    .metric-description {
        color: #6b7280;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .badge-excellent {
        background-color: #d1fae5;
        color: #065f46;
    }
    
    .badge-good {
        background-color: #dbeafe;
        color: #1e40af;
    }
    
    .badge-warning {
        background-color: #fef3c7;
        color: #92400e;
    }
    
    .badge-danger {
        background-color: #fee2e2;
        color: #991b1b;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background-color: #f9fafb;
        border-radius: 8px 8px 0 0;
        border: 1px solid #e5e7eb;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 0.75rem;
        font-weight: 600;
        transition: all 0.3s;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 102, 246, 0.4);
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Progress indicators */
    .stProgress > div > div {
        background-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'code_input' not in st.session_state:
        st.session_state.code_input = ""
    if 'ai_docs' not in st.session_state:
        st.session_state.ai_docs = ""
    if 'human_docs' not in st.session_state:
        st.session_state.human_docs = ""
    if 'eval_result' not in st.session_state:
        st.session_state.eval_result = None
    if 'code_structure' not in st.session_state:
        st.session_state.code_structure = None


def load_sample_code():
    """Load sample code from file."""
    try:
        with open('data/sample_code.py', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"# Error loading sample code: {e}"


def load_sample_human_docs():
    """Load sample human documentation."""
    try:
        with open('data/sample_human_docs.json', 'r', encoding='utf-8') as f:
            docs = json.load(f)
            # Convert to markdown format
            markdown = "# Human-Written Documentation\n\n"
            for func_name, func_doc in docs.items():
                markdown += f"## Function: {func_name}\n\n"
                markdown += f"**Description:** {func_doc['description']}\n\n"
                if 'parameters' in func_doc:
                    markdown += "**Parameters:**\n"
                    for param, desc in func_doc['parameters'].items():
                        markdown += f"- `{param}`: {desc}\n"
                    markdown += "\n"
                if 'returns' in func_doc:
                    markdown += f"**Returns:** {func_doc['returns']}\n\n"
                if 'examples' in func_doc:
                    markdown += "**Examples:**\n```python\n"
                    markdown += '\n'.join(func_doc['examples'])
                    markdown += "\n```\n\n"
                markdown += "---\n\n"
            return markdown
    except Exception as e:
        return f"Error loading human docs: {e}"


def main():
    """Main application function."""
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Documentation Generator</h1>
        <p>Generative AI-Driven Automated Documentation with Interactive UI</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">Software Development & Architecture Project | Layered Architecture Demo</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        use_api = st.checkbox("Use OpenAI API", value=False, 
                             help="Enable to use real AI (requires API key)")
        
        if use_api:
            api_key = st.text_input("OpenAI API Key", type="password")
        else:
            st.info("💡 Using intelligent mock generator (no API required)")
            api_key = None
        
        doc_style = st.selectbox(
            "Documentation Style",
            ["google", "numpy"],
            help="Choose docstring format"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Architecture Layers")
        st.markdown("""
        1. ✅ **UI Layer** (Streamlit)
        2. ✅ **Preprocessing** (AST Parser)
        3. ✅ **AI Inference** (LLM)
        4. ✅ **Doc Generator**
        5. ✅ **Evaluation Engine**
        6. ✅ **Output Formatter**
        """)
        
        st.markdown("---")
        st.markdown("### 📚 Quick Start")
        st.markdown("""
        1. Load sample code
        2. Generate docs
        3. Load human docs
        4. Evaluate quality
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Input Python Code")
        code_input = st.text_area(
            "Paste your Python code here",
            height=400,
            value=st.session_state.code_input,
            placeholder="def example_function(param1, param2):\n    # Your code here\n    pass"
        )
        st.session_state.code_input = code_input
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("📂 Load Sample Code", use_container_width=True):
                st.session_state.code_input = load_sample_code()
                st.rerun()
        
        with col_btn2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.code_input = ""
                st.rerun()
    
    with col2:
        st.markdown("### 🎯 Actions")
        
        if st.button("🚀 Generate Documentation", type="primary", use_container_width=True):
            if not code_input.strip():
                st.error("⚠️ Please enter some Python code first!")
            else:
                with st.spinner("🔄 Analyzing code and generating documentation..."):
                    try:
                        # Layer 2: Parse code
                        parser = CodeParser()
                        code_structure = parser.get_structure(code_input)
                        
                        if not code_structure.is_valid:
                            st.error(f"❌ Syntax Error: {code_structure.error_message}")
                        else:
                            st.session_state.code_structure = code_structure
                            
                            # Layer 3: AI Inference
                            llm = LLMInterface(use_api=use_api, api_key=api_key)
                            
                            # Layer 4: Generate documentation
                            doc_gen = DocumentationGenerator(style=doc_style)
                            
                            all_docs = {}
                            for func in code_structure.functions:
                                ai_output = llm.generate_documentation(func)
                                docstring = doc_gen.generate_function_docs(func, ai_output)
                                all_docs[func.name] = docstring
                            
                            # Format final output
                            st.session_state.ai_docs = doc_gen.format_output(all_docs)
                            
                            st.success("✅ Documentation generated successfully!")
                            st.balloons()
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_load, col_eval = st.columns(2)
        with col_load:
            if st.button("📖 Load Sample Human Docs", use_container_width=True):
                st.session_state.human_docs = load_sample_human_docs()
                st.success("✅ Human documentation loaded!")
                st.rerun()
        
        with col_eval:
            if st.button("📊 Evaluate Documentation", use_container_width=True):
                if not st.session_state.ai_docs or not st.session_state.human_docs:
                    st.error("⚠️ Please generate AI docs and load human docs first!")
                else:
                    with st.spinner("📈 Evaluating documentation quality..."):
                        try:
                            # Layer 5: Evaluation
                            evaluator = DocumentationEvaluator()
                            eval_result = evaluator.evaluate(
                                st.session_state.ai_docs,
                                st.session_state.human_docs,
                                st.session_state.code_structure
                            )
                            st.session_state.eval_result = eval_result
                            
                            st.success("✅ Evaluation complete!")
                            st.rerun()
                        
                        except Exception as e:
                            st.error(f"❌ Evaluation error: {str(e)}")
    
    # Results section with tabs
    st.markdown("---")
    st.markdown("## 📄 Results")
    
    tabs = st.tabs([
        "📝 Original Code",
        "🤖 AI-Generated Documentation",
        "👤 Human Documentation",
        "📊 Evaluation Results"
    ])
    
    with tabs[0]:
        st.markdown("### Original Python Code")
        if st.session_state.code_input:
            st.code(st.session_state.code_input, language="python", line_numbers=True)
            
            if st.session_state.code_structure:
                st.markdown("#### Code Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Lines", st.session_state.code_structure.total_lines)
                with col2:
                    st.metric("Functions", len(st.session_state.code_structure.functions))
                with col3:
                    st.metric("Classes", len(st.session_state.code_structure.classes))
        else:
            st.info("👆 Enter code in the input area above")
    
    with tabs[1]:
        st.markdown("### AI-Generated Documentation")
        if st.session_state.ai_docs:
            st.markdown(st.session_state.ai_docs)
            
            # Download button
            st.download_button(
                label="⬇️ Download Documentation",
                data=st.session_state.ai_docs,
                file_name="ai_generated_docs.md",
                mime="text/markdown"
            )
        else:
            st.info("👆 Click 'Generate Documentation' to create AI docs")
    
    with tabs[2]:
        st.markdown("### Human-Written Documentation (Reference)")
        if st.session_state.human_docs:
            st.markdown(st.session_state.human_docs)
        else:
            st.info("👆 Click 'Load Sample Human Docs' to load reference documentation")
    
    with tabs[3]:
        st.markdown("### Evaluation Results")
        if st.session_state.eval_result:
            eval_result = st.session_state.eval_result
            
            # Overall score with big display
            st.markdown("#### Overall Quality Score")
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                score_color = "green" if eval_result.overall_score >= 70 else "orange" if eval_result.overall_score >= 50 else "red"
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #{score_color}33 0%, #{score_color}11 100%); 
                     padding: 2rem; border-radius: 10px; text-align: center; border: 2px solid #{score_color}88;">
                    <h1 style="margin: 0; color: {score_color}; font-size: 3.5rem;">
                        {eval_result.overall_score:.1f}
                    </h1>
                    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1.2rem;">out of 100</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Individual metrics
            st.markdown("#### Detailed Metrics")
            
            # Layer 6: Format output
            formatter = OutputFormatter()
            metric_cards = formatter.format_metric_cards(eval_result)
            
            cols = st.columns(2)
            for idx, card in enumerate(metric_cards[:4]):  # First 4 metrics in grid
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>{card['icon']} {card['title']}</h3>
                        <p class="metric-value">{card['value']}</p>
                        <p class="metric-description">{card['description']}</p>
                        <span class="status-badge badge-{'excellent' if '✅' in card['interpretation'] else 'good' if '✓' in card['interpretation'] else 'warning'}">
                            {card['interpretation']}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Detailed report
            with st.expander("📋 View Detailed Report"):
                report = formatter.generate_report(eval_result, st.session_state.code_structure)
                st.markdown(report)
            
            # Metric explanations
            with st.expander("ℹ️ Metric Explanations"):
                st.markdown("""
                #### How Metrics are Calculated
                
                **1. Keyword Overlap (Jaccard Similarity)**
                - Extracts meaningful keywords from both AI and human documentation
                - Calculates: `intersection / union` of keyword sets
                - Score: 0-100% (higher = more semantic similarity)
                
                **2. Coverage Score**
                - Counts documented vs. total code elements (functions, classes)
                - Calculation: `(documented / total) × 100`
                - Score: 0-100% (higher = more complete)
                
                **3. Length Ratio**
                - Compares word counts: `AI_words / Human_words`
                - Ideal range: 0.8 - 1.2 (balanced verbosity)
                
                **4. Consistency Score**
                - Checks formatting uniformity (Args, Returns, Examples sections)
                - Verifies consistent parameter naming and structure
                - Score: 0-100% (higher = more consistent style)
                
                **Overall Score**
                - Weighted average: 35% keyword + 30% coverage + 15% length + 20% consistency
                """)
        
        else:
            st.info("👆 Click 'Evaluate Documentation' to see quality metrics")
            st.markdown("""
            <div class="info-box">
                <h4>📊 What you'll see after evaluation:</h4>
                <ul>
                    <li>Overall quality score (0-100)</li>
                    <li>Keyword overlap analysis</li>
                    <li>Documentation coverage metrics</li>
                    <li>Length and verbosity comparison</li>
                    <li>Style consistency assessment</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p style="margin: 0;">
            <strong>AI-Driven Documentation Generator</strong> | 
            Software Development & Architecture Project
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Demonstrating Layered Architecture, AI Integration, and Professional UI Design
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
