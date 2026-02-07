import { NextRequest, NextResponse } from 'next/server';
import { DocumentationEvaluator } from '@/lib/evaluation/evaluator';
import { CodeStructure } from '@/types';

export async function POST(request: NextRequest) {
    try {
        const { aiDocs, humanDocs, codeStructure } = await request.json() as {
            aiDocs: string,
            humanDocs: string,
            codeStructure: CodeStructure
        };

        if (!aiDocs) {
            return NextResponse.json(
                { success: false, error: 'AI Documentation is required' },
                { status: 400 }
            );
        }

        // If no human docs provided, we can maybe mock them or just evaluate consistentcy/coverage
        // For this demo, we'll assume humanDocs might be empty and handle gracefully in evaluator or here
        const effectiveHumanDocs = humanDocs || '';

        const evaluator = new DocumentationEvaluator();
        const evaluation = evaluator.evaluate(aiDocs, effectiveHumanDocs, codeStructure);

        return NextResponse.json({ success: true, evaluation });
    } catch (error: any) {
        return NextResponse.json(
            { success: false, error: error.message },
            { status: 500 }
        );
    }
}
