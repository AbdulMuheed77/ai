import { parse } from '@babel/parser';
import traverse from '@babel/traverse';
import * as t from '@babel/types';
import { CodeStructure, FunctionInfo, ClassInfo } from '@/types';

export class CodeParser {
    private code: string = '';
    private functions: FunctionInfo[] = [];
    private classes: ClassInfo[] = [];

    constructor() { }

    public parse(code: string): CodeStructure {
        this.code = code;
        this.functions = [];
        this.classes = [];

        try {
            const ast = parse(code, {
                sourceType: 'module',
                plugins: ['typescript', 'jsx', 'classProperties', 'decorators-legacy'],
            });

            // Extract module-level docstring (comments at the top)
            const moduleDocstring = this.extractModuleDocstring(ast);

            // Travel the AST
            traverse(ast, {
                FunctionDeclaration: (path) => {
                    // Only top-level functions (not inside classes, handled separately)
                    if (!path.parentPath.isClassBody()) {
                        this.functions.push(this.parseFunction(path.node));
                    }
                },
                ClassDeclaration: (path) => {
                    this.classes.push(this.parseClass(path.node));
                },
                // Handle arrow functions assigned to variables
                VariableDeclarator: (path) => {
                    if (
                        t.isArrowFunctionExpression(path.node.init) ||
                        t.isFunctionExpression(path.node.init)
                    ) {
                        // Only if it's a top-level variable
                        if (path.parentPath.parentPath?.isProgram()) {
                            const name = t.isIdentifier(path.node.id) ? path.node.id.name : 'anonymous';
                            const funcNode = path.node.init as t.ArrowFunctionExpression | t.FunctionExpression;
                            this.functions.push(this.parseFunction(funcNode, name));
                        }
                    }
                }
            });

            return {
                functions: this.functions,
                classes: this.classes,
                moduleDocstring,
                totalLines: code.split('\n').length,
                isValid: true,
                errorMessage: null,
            };

        } catch (error: any) {
            return {
                functions: [],
                classes: [],
                moduleDocstring: null,
                totalLines: code.split('\n').length,
                isValid: false,
                errorMessage: error.message || 'Unknown parsing error',
            };
        }
    }

    private parseFunction(
        node: t.FunctionDeclaration | t.FunctionExpression | t.ArrowFunctionExpression | t.ClassMethod,
        inferredName?: string
    ): FunctionInfo {
        const loc = node.loc!;
        const startLine = loc.start.line;
        const endLine = loc.end.line;

        // Extract name
        let name = inferredName || 'anonymous';
        if (t.isFunctionDeclaration(node) && node.id) {
            name = node.id.name;
        } else if (t.isClassMethod(node) && t.isIdentifier(node.key)) {
            name = node.key.name;
        }

        // Extract parameters
        const params = node.params.map(param => {
            if (t.isIdentifier(param)) return param.name;
            if (t.isAssignmentPattern(param) && t.isIdentifier(param.left)) return param.left.name;
            return 'param';
        });

        // Extract return annotation
        let returnAnnotation: string | null = null;
        if (node.returnType && t.isTSTypeAnnotation(node.returnType)) {
            // Extract the raw text of the type annotation from the source code
            if (node.returnType.loc) {
                const typeStart = node.returnType.loc.start;
                const typeEnd = node.returnType.loc.end;

                // Get lines from code
                const allLines = this.code.split('\n');

                // Handle single line vs multi-line type annotations
                if (typeStart.line === typeEnd.line) {
                    const line = allLines[typeStart.line - 1];
                    returnAnnotation = line.slice(typeStart.column, typeEnd.column);
                } else {
                    // Multi-line type annotation
                    const startLine = allLines[typeStart.line - 1].slice(typeStart.column);
                    const middleLines = allLines.slice(typeStart.line, typeEnd.line - 1);
                    const endLine = allLines[typeEnd.line - 1].slice(0, typeEnd.column);
                    returnAnnotation = [startLine, ...middleLines, endLine].join('\n');
                }

                // Remove the leading colon and whitespace if captured (usually AST node is just the type, but good to clean)
                returnAnnotation = returnAnnotation.replace(/^:\s*/, '').trim();
            } else {
                returnAnnotation = 'any'; // Fallback
            }
        }

        // Extract docstring (leading comments)
        const docstring = this.extractDocstring(node);

        // Extract body
        const lines = this.code.split('\n');
        const body = lines.slice(startLine - 1, endLine).join('\n');

        return {
            name,
            params,
            returnAnnotation,
            docstring,
            lineStart: startLine,
            lineEnd: endLine,
            body,
            isAsync: node.async,
            isExported: node.type === 'FunctionDeclaration' ? (node as any).export === true : false,
        };
    }

    private parseClass(node: t.ClassDeclaration): ClassInfo {
        const loc = node.loc!;
        const name = node.id ? node.id.name : 'AnonymousClass';
        const methods: FunctionInfo[] = [];

        if (node.body && node.body.body) {
            node.body.body.forEach(item => {
                if (t.isClassMethod(item)) {
                    // Skip constructor for documentation purposes? usually no, but keeping simple
                    if (item.kind === 'method') {
                        methods.push(this.parseFunction(item));
                    }
                }
            });
        }

        const docstring = this.extractDocstring(node);

        return {
            name,
            methods,
            docstring,
            lineStart: loc.start.line,
            lineEnd: loc.end.line,
            isExported: false, // Simplification
        };
    }

    private extractDocstring(node: t.Node): string | null {
        if (node.leadingComments && node.leadingComments.length > 0) {
            const lastComment = node.leadingComments[node.leadingComments.length - 1];
            if (lastComment.type === 'CommentBlock') {
                // Basic cleanup of JSDoc style
                return lastComment.value
                    .replace(/^\*/gm, '') // Remove leading asterisks
                    .replace(/\n\s+/g, '\n') // Remove excessive indentation
                    .trim();
            }
        }
        return null;
    }

    private extractModuleDocstring(ast: t.File): string | null {
        if (ast.comments && ast.comments.length > 0) {
            const firstComment = ast.comments[0];
            // Heuristic: if comment is at the very top (line 1), it might be module doc
            if (firstComment.loc && firstComment.loc.start.line === 1 && firstComment.type === 'CommentBlock') {
                return firstComment.value.trim();
            }
        }
        return null;
    }
}
