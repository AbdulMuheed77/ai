import OpenAI from 'openai';
import { FunctionInfo, DocumentationOutput, AIConfig } from '@/types';

export class LLMInterface {
    private client: OpenAI | null = null;
    private useApi: boolean;
    private model: string;

    constructor(config: AIConfig) {
        this.useApi = config.useApi;
        this.model = config.model || 'gpt-3.5-turbo';

        if (this.useApi && config.apiKey) {
            this.client = new OpenAI({
                apiKey: config.apiKey,
                dangerouslyAllowBrowser: true // Note: In production, call via API routes only
            });
        }
    }

    public async generateDocumentation(func: FunctionInfo): Promise<DocumentationOutput> {
        if (this.useApi && this.client) {
            return this.generateWithApi(func);
        } else {
            return this.generateWithMock(func);
        }
    }

    private async generateWithApi(func: FunctionInfo): Promise<DocumentationOutput> {
        try {
            const prompt = this.createPrompt(func);

            const response = await this.client!.chat.completions.create({
                model: this.model,
                messages: [
                    { role: 'system', content: 'You are an expert technical writer generating JSDoc documentation.' },
                    { role: 'user', content: prompt }
                ],
                temperature: 0.3,
            });

            const content = response.choices[0].message.content || '';
            return this.parseApiResponse(content, func);
        } catch (error) {
            console.error('API Generation Error:', error);
            return this.generateWithMock(func); // Fallback to mock
        }
    }

    private generateWithMock(func: FunctionInfo): DocumentationOutput {
        // Intelligent mock generation based on function name and structure
        const verb = this.inferVerb(func.name);
        const description = `${verb} the ${this.formatName(func.name)} functionality.`;

        // Generate param descriptions
        const paramDescriptions: Record<string, string> = {};
        func.params.forEach(param => {
            paramDescriptions[param] = `The ${param} input parameter.`;
        });

        return {
            functionName: func.name,
            description: `${description}\n\nThis function handles the logic for ${func.name.toLowerCase()} processing with robust error handling.`,
            paramDescriptions,
            returnDescription: func.returnAnnotation ? `Returns a value of type ${func.returnAnnotation}.` : 'The result of the operation.',
            examples: [
                `// Example usage of ${func.name}`,
                `const result = ${func.name}(${func.params.map(p => '...').join(', ')});`,
                `console.log(result);`
            ],
            inlineComments: [
                `// Calculate ${func.name}`,
                `// Validate input parameters`
            ]
        };
    }

    private createPrompt(func: FunctionInfo): string {
        return `Generate detailed JSDoc documentation for the following JavaScript/TypeScript function:

Function Name: ${func.name}
Parameters: ${func.params.join(', ')}
Code:
\`\`\`javascript
${func.body}
\`\`\`

Return the output as a JSON object with the following fields:
- description: A clear summary of the function
- paramDescriptions: Object mapping parameter names to descriptions
- returnDescription: Description of the return value
- examples: Array of usage example strings
- inlineComments: Array of suggested inline comments
`;
    }

    private parseApiResponse(content: string, func: FunctionInfo): DocumentationOutput {
        try {
            // Try to extract JSON from code blocks if present
            const jsonMatch = content.match(/```json\n([\s\S]*?)\n```/) ||
                content.match(/```\n([\s\S]*?)\n```/) ||
                [null, content];

            const jsonStr = jsonMatch[1] || content;
            const parsed = JSON.parse(jsonStr);

            return {
                functionName: func.name,
                description: parsed.description || 'No description generated.',
                paramDescriptions: parsed.paramDescriptions || {},
                returnDescription: parsed.returnDescription || 'No return description.',
                examples: parsed.examples || [],
                inlineComments: parsed.inlineComments || []
            };
        } catch (e) {
            console.error('Failed to parse AI response', e);
            return this.generateWithMock(func);
        }
    }

    // Helpers for mock mode
    private inferVerb(name: string): string {
        if (name.startsWith('get')) return 'Retrieves';
        if (name.startsWith('set')) return 'Sets';
        if (name.startsWith('is')) return 'Checks if';
        if (name.startsWith('calc')) return 'Calculates';
        if (name.startsWith('handle')) return 'Handles';
        return 'Performs';
    }

    private formatName(name: string): string {
        return name.replace(/([A-Z])/g, ' $1').toLowerCase();
    }
}
