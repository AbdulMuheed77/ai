import requests
import json
import sys

BASE_URL = "http://localhost:3000"

def test_api():
    print("Testing API Endpoints...")
    
    # 1. Test Parse
    code = """
    function calculateTotal(items, taxRate) {
        let total = 0;
        for (let i = 0; i < items.length; i++) {
            total += items[i].price * items[i].quantity;
        }
        return total * (1 + taxRate);
    }
    """
    
    print("\n[1] Testing /api/parse...")
    try:
        parse_res = requests.post(f"{BASE_URL}/api/parse", json={"code": code})
        parse_data = parse_res.json()
        
        if parse_data.get("success"):
            print("✅ Parse Successful")
            structure = parse_data.get("structure")
            # Verify my fixes
            func = structure["functions"][0]
            print(f"   Function Name: {func['name']}")
            print(f"   Return Annotation: {func.get('returnAnnotation')}") 
            # Note: returnAnnotation might be null or 'any' if not typescript, passing JS above.
            # Let's try TS code to test my fix
        else:
            print(f"❌ Parse Failed: {parse_data.get('error')}")
            return
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    # 1b. Test Parse with Types
    ts_code = """
    function getMessage(id: string): string {
        return "Message " + id;
    }
    """
    print("\n[1b] Testing /api/parse with TypeScript...")
    try:
        parse_res = requests.post(f"{BASE_URL}/api/parse", json={"code": ts_code})
        parse_data = parse_res.json()
        if parse_data.get("success"):
            func = parse_data["structure"]["functions"][0]
            print(f"   Return Annotation: '{func.get('returnAnnotation')}'")
            if func.get('returnAnnotation') == 'string':
                 print("✅ Type Extraction Verified")
            else:
                 print("⚠️ Type Extraction Result Unexpected")
    except Exception as e:
        print(f"❌ Error: {e}")


    # 2. Test Generate (Mock Mode)
    print("\n[2] Testing /api/generate (Mock)...")
    try:
        # Use structure from first parse
        gen_res = requests.post(f"{BASE_URL}/api/generate", json={
            "codeStructure": parse_data["structure"], # Using the TS one
            "useApi": False
        })
        gen_data = gen_res.json()
        
        if gen_data.get("success"):
             print("✅ Generation Successful")
             print(f"   Docs Length: {len(gen_data.get('documentation', ''))}")
             ai_docs = gen_data.get("documentation")
        else:
             print(f"❌ Generation Failed: {gen_data.get('error')}")
             return
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # 3. Test Evaluate
    print("\n[3] Testing /api/evaluate...")
    try:
        eval_res = requests.post(f"{BASE_URL}/api/evaluate", json={
            "aiDocs": ai_docs,
            "humanDocs": ai_docs, # Self-eval
            "codeStructure": parse_data["structure"]
        })
        eval_data = eval_res.json()
        
        if eval_data.get("success"):
            print("✅ Evaluation Successful")
            evaluation = eval_data.get("evaluation")
            print(f"   Overall Score: {evaluation.get('overallScore')}")
            detailed = evaluation.get("detailedAnalysis", {})
            kw_overlap = detailed.get("keywordOverlap", {})
            print(f"   Keywords Found: {len(kw_overlap.get('aiKeywords', []))}")
            if len(kw_overlap.get('aiKeywords', [])) > 0:
                 print("✅ Detailed Analysis Verified (Keywords populated)")
            else:
                 print("⚠️ Detailed Analysis Empty")
        else:
            print(f"❌ Evaluation Failed: {eval_data.get('error')}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
