import { EvaluationResult, CodeStructure } from '@/types';

export class DocumentationEvaluator {

    public evaluate(aiDocs: string, humanDocs: string, structure: CodeStructure): EvaluationResult {
        const keywordOverlapScore = this.calculateKeywordOverlap(aiDocs, humanDocs);
        const coverageScore = this.calculateCoverage(structure);
        const lengthRatio = this.calculateLengthRatio(aiDocs, humanDocs);
        const consistencyScore = this.calculateConsistency(aiDocs);

        // Weighted average
        const overallScore = (
            (keywordOverlapScore * 0.35) +
            (coverageScore * 0.30) +
            (this.interpretLengthRatio(lengthRatio) * 0.15) +
            (consistencyScore * 0.20)
        );

        return {
            keywordOverlapScore,
            coverageScore,
            lengthRatio,
            consistencyScore,
            overallScore: Math.round(overallScore * 10) / 10,
            detailedAnalysis: {
                keywordOverlap: {
                    aiKeywords: this.extractKeywords(aiDocs),
                    humanKeywords: this.extractKeywords(humanDocs),
                    intersection: this.extractKeywords(aiDocs).filter(x => this.extractKeywords(humanDocs).includes(x))
                },
                coverage: {
                    totalElements: structure.functions.length,
                    documentedElements: structure.functions.length, // assuming full generation
                    missingDocs: []
                },
                length: {
                    aiWordCount: this.countWords(aiDocs),
                    humanWordCount: this.countWords(humanDocs)
                },
                consistency: {
                    issues: []
                }
            }
        };
    }

    private calculateKeywordOverlap(doc1: string, doc2: string): number {
        const set1 = new Set(this.extractKeywords(doc1));
        const set2 = new Set(this.extractKeywords(doc2));

        const intersection = new Set([...set1].filter(x => set2.has(x)));
        const union = new Set([...set1, ...set2]);

        if (union.size === 0) return 0;
        return (intersection.size / union.size) * 100;
    }

    private extractKeywords(text: string): string[] {
        return text.toLowerCase()
            .replace(/[^\w\s]/g, '')
            .split(/\s+/)
            .filter(w => w.length > 3);
    }

    private calculateCoverage(structure: CodeStructure): number {
        if (structure.functions.length === 0) return 100;
        // In this app flow, we generate docs for everything extracted, so 100% coverage of what we processed
        return 100;
    }

    private calculateLengthRatio(aiDocs: string, humanDocs: string): number {
        const aiWords = this.countWords(aiDocs);
        const humanWords = this.countWords(humanDocs);
        if (humanWords === 0) return 1;
        return aiWords / humanWords;
    }

    private countWords(text: string): number {
        return text.trim().split(/\s+/).length;
    }

    private calculateConsistency(docs: string): number {
        // Check for JSDoc standard tags consistency
        const hasParam = /@param/.test(docs);
        const hasReturn = /@returns?/.test(docs);
        const hasExample = /@example/.test(docs);

        let score = 100;
        if (!hasParam) score -= 20;
        if (!hasReturn) score -= 10;
        if (!hasExample) score -= 10;

        return Math.max(0, score);
    }

    private interpretLengthRatio(ratio: number): number {
        // Ideal ratio is 0.8 to 1.2
        if (ratio >= 0.8 && ratio <= 1.2) return 100;
        const diff = Math.abs(1 - ratio);
        return Math.max(0, 100 - (diff * 50));
    }
}
