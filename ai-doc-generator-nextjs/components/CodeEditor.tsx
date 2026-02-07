'use client';

import React from 'react';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import js from 'react-syntax-highlighter/dist/esm/languages/hljs/javascript';
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';

SyntaxHighlighter.registerLanguage('javascript', js);

interface CodeEditorProps {
    code: string;
    onChange: (value: string) => void;
    placeholder?: string;
}

export default function CodeEditor({ code, onChange, placeholder }: CodeEditorProps) {
    return (
        <div className="relative h-[500px] w-full border border-gray-700 rounded-lg overflow-hidden flex flex-col">
            <div className="bg-gray-800 text-gray-400 px-4 py-2 text-xs font-mono uppercase tracking-wider border-b border-gray-700">
                JavaScript Input
            </div>
            <div className="relative flex-1">
                <textarea
                    value={code}
                    onChange={(e) => onChange(e.target.value)}
                    placeholder={placeholder}
                    className="absolute inset-0 w-full h-full p-4 font-mono text-sm bg-transparent text-transparent caret-white resize-none focus:outline-none z-10"
                    spellCheck={false}
                    style={{
                        // Make text transparent so we see the syntax highlighter behind it
                        // but keep caret visible. This is a simple trick for editable syntax highlighting.
                        color: 'transparent',
                        backgroundColor: 'transparent'
                    }}
                />
                <div className="absolute inset-0 w-full h-full pointer-events-none z-0">
                    <SyntaxHighlighter
                        language="javascript"
                        style={atomOneDark}
                        customStyle={{ margin: 0, padding: '1rem', height: '100%', fontSize: '0.875rem' }}
                        showLineNumbers={true}
                        wrapLines={true}
                    >
                        {code || ' '}
                    </SyntaxHighlighter>
                </div>
            </div>
        </div>
    );
}
