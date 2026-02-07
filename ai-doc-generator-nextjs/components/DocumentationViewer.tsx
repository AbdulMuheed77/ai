import React from 'react';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import js from 'react-syntax-highlighter/dist/esm/languages/hljs/javascript';
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { Copy, Check } from 'lucide-react';

SyntaxHighlighter.registerLanguage('javascript', js);

interface DocumentationViewerProps {
    documentation: string;
}

export default function DocumentationViewer({ documentation }: DocumentationViewerProps) {
    const [copied, setCopied] = React.useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(documentation);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="bg-gray-900 rounded-lg overflow-hidden border border-gray-700">
            <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
                <span className="text-xs font-mono text-gray-400 uppercase">JSDoc Output</span>
                <button
                    onClick={handleCopy}
                    className="flex items-center gap-2 text-xs text-gray-400 hover:text-white transition-colors"
                >
                    {copied ? <Check size={14} className="text-green-400" /> : <Copy size={14} />}
                    {copied ? 'Copied!' : 'Copy'}
                </button>
            </div>
            <div className="p-0">
                <SyntaxHighlighter
                    language="javascript"
                    style={atomOneDark}
                    customStyle={{ margin: 0, padding: '1.5rem', fontSize: '0.875rem' }}
                    showLineNumbers={true}
                    wrapLines={true}
                >
                    {documentation || '// Generated documentation will appear here...'}
                </SyntaxHighlighter>
            </div>
        </div>
    );
}
