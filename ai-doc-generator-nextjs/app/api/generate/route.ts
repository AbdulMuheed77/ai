import { NextRequest, NextResponse } from 'next/server';
import { LLMInterface } from '@/lib/ai/llmInterface';
import { DocumentationGenerator } from '@/lib/generators/docGenerator';
import { CodeStructure, FunctionInfo } from '@/types';

export async function POST(request: NextRequest) {
    try {
        const { codeStructure, useApi, apiKey } = await request.json() as {
            codeStructure: CodeStructure,
            useApi: boolean,
            apiKey?: string
        };

        // Server-side environment variable fallback
        const finalApiKey = apiKey || process.env.OPENAI_API_KEY;

        if (useApi && !finalApiKey) {
            return NextResponse.json(
                { success: false, error: 'OpenAI API Key is required for API mode' },
                { status: 400 }
            );
        }

        const llm = new LLMInterface({ useApi, apiKey: finalApiKey });
        const generator = new DocumentationGenerator();

        // Generate documentation for each function
        // In a real app, might want to limit parallelism or use a queue
        const docsMap: Record<string, string> = {};

        await Promise.all(
            codeStructure.functions.map(async (func: FunctionInfo) => {
                const aiOutput = await llm.generateDocumentation(func);
                const docstring = generator.generateFunctionDocs(func, aiOutput);
                docsMap[func.name] = docstring;
            })
        );

        // Create the full formatted output
        let fullDocs = '';

        // Functions
        if (codeStructure.functions.length > 0) {
            fullDocs += '## Functions\n\n';
            codeStructure.functions.forEach(func => {
                if (docsMap[func.name]) {
                    fullDocs += `### ${func.name}\n\n\`\`\`javascript\n${docsMap[func.name]}\n\`\`\`\n\n`;
                }
            });
        }

        return NextResponse.json({ success: true, documentation: fullDocs, docsMap });
    } catch (error: any) {
        console.error('Generation Error:', error);
        return NextResponse.json(
            { success: false, error: error.message || 'Documentation generation failed' },
            { status: 500 }
        );
    }
}
