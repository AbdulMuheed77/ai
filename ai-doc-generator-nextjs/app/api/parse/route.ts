import { NextRequest, NextResponse } from 'next/server';
import { CodeParser } from '@/lib/parsers/jsParser';

export async function POST(request: NextRequest) {
    try {
        const { code } = await request.json();

        if (!code) {
            return NextResponse.json(
                { success: false, error: 'No code provided' },
                { status: 400 }
            );
        }

        const parser = new CodeParser();
        const structure = parser.parse(code);

        return NextResponse.json({ success: true, structure });
    } catch (error: any) {
        return NextResponse.json(
            { success: false, error: error.message },
            { status: 500 }
        );
    }
}
