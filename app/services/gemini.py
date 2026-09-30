import json
from .fallback import home_fallback, party_fallback, jewelry_fallback
from ..core.config import settings

try:
    import google.generativeai as genai
except Exception:
    genai = None

SYSTEM = '''You are PocketSmart AI, a budget-aware recommendation assistant. Return ONLY valid JSON with keys: summary, allocation (object of category to number), recommendations (array). Each recommendation must have category,item,platform,estimated_price,reason. Respect the user's total budget. Platform names may include Amazon, Flipkart, IKEA, Swiggy, Zomato, OYO. Do not claim live inventory or exact live prices; label prices as estimates.''' 

def _call(prompt, image_bytes=None, mime_type=None):
    if not settings.gemini_api_key or genai is None: return None
    genai.configure(api_key=settings.gemini_api_key)
    model=genai.GenerativeModel(settings.gemini_model, system_instruction=SYSTEM)
    parts=[prompt]
    if image_bytes and mime_type:
        parts.append({"mime_type":mime_type,"data":image_bytes})
    result=model.generate_content(parts)
    raw=result.text.strip().replace("```json","").replace("```","")
    return json.loads(raw)

def generate(planner, req, image_bytes=None, mime_type=None):
    try:
        prompt=f"Planner: {planner}\nUser input: {req.model_dump_json()}\nCreate practical recommendations for an Indian user."
        data=_call(prompt,image_bytes,mime_type)
        if data:
            data.update({"planner":planner,"budget":req.budget,"ai_used":True,"note":"Generated with Gemini. Prices and availability are estimates; verify before purchase."})
            return data
    except Exception:
        pass
    return {"home":home_fallback,"party":party_fallback,"jewelry":jewelry_fallback}[planner](req)
