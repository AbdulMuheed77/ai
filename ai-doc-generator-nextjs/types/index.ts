export interface FunctionInfo {
  name: string;
  params: string[];
  returnAnnotation: string | null;
  docstring: string | null;
  lineStart: number;
  lineEnd: number;
  body: string;
  isAsync: boolean;
  isExported: boolean;
}

export interface ClassInfo {
  name: string;
  methods: FunctionInfo[];
  docstring: string | null;
  lineStart: number;
  lineEnd: number;
  isExported: boolean;
}

export interface CodeStructure {
  functions: FunctionInfo[];
  classes: ClassInfo[];
  moduleDocstring: string | null;
  totalLines: number;
  isValid: boolean;
  errorMessage: string | null;
}

export interface DocumentationOutput {
  functionName: string;
  description: string;
  paramDescriptions: Record<string, string>;
  returnDescription: string;
  examples: string[];
  inlineComments: string[];
}

export interface EvaluationResult {
  keywordOverlapScore: number;
  coverageScore: number;
  lengthRatio: number;
  consistencyScore: number;
  overallScore: number;
  detailedAnalysis: {
    keywordOverlap: {
      aiKeywords: string[];
      humanKeywords: string[];
      intersection: string[];
    };
    coverage: {
      totalElements: number;
      documentedElements: number;
      missingDocs: string[];
    };
    length: {
      aiWordCount: number;
      humanWordCount: number;
    };
    consistency: {
      issues: string[];
    };
  };
}

export interface AIConfig {
  useApi: boolean;
  apiKey?: string;
  model?: string;
}
