import { FunctionInfo, DocumentationOutput } from '@/types';

export class DocumentationGenerator {
    public generateFunctionDocs(func: FunctionInfo, aiOutput: DocumentationOutput): string {
        const lines: string[] = [];

        lines.push('/**');

        // Description
        lines.push(` * ${aiOutput.description}`);
        lines.push(' *');

        // Parameters
        func.params.forEach(param => {
            const desc = aiOutput.paramDescriptions[param] || 'Parameter description';
            lines.push(` * @param {any} ${param} - ${desc}`);
        });

        // Returns
        if (aiOutput.returnDescription) {
            lines.push(` * @returns {any} ${aiOutput.returnDescription}`);
        }

        // Examples
        if (aiOutput.examples && aiOutput.examples.length > 0) {
            lines.push(' *');
            aiOutput.examples.forEach(ex => {
                lines.push(` * @example`);
                // Handle multiline examples
                ex.split('\n').forEach(line => {
                    lines.push(` * ${line}`);
                });
            });
        }

        lines.push(' */');

        return lines.join('\n');
    }

    public generateMarkdownReport(results: any): string {
        // Helper to generate markdown downloads
        return `# AI Generated Documentation\n\n${results}`;
    }
}
