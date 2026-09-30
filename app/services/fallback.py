PLATFORM_LINKS = {
    "Amazon": "https://www.amazon.in/",
    "Flipkart": "https://www.flipkart.com/",
    "IKEA": "https://www.ikea.com/in/en/",
    "Swiggy": "https://www.swiggy.com/",
    "Zomato": "https://www.zomato.com/",
    "OYO": "https://www.oyorooms.com/",
}

def home_fallback(req):
    b=req.budget; alloc={"Furniture":round(b*.40,2),"Lighting":round(b*.20,2),"Decor":round(b*.20,2),"Utility":round(b*.20,2)}
    items=[
      {"category":"Furniture","item":f"{req.style} compact furniture set","platform":"IKEA","estimated_price":alloc["Furniture"]*.8,"reason":"Prioritizes essential pieces within the furniture allocation."},
      {"category":"Lighting","item":"LED ceiling/light set","platform":"Amazon","estimated_price":alloc["Lighting"]*.65,"reason":"Energy-efficient lighting option for common rooms."},
      {"category":"Decor","item":"Wall art and soft-furnishing bundle","platform":"Flipkart","estimated_price":alloc["Decor"]*.55,"reason":"Adds style without consuming the core furniture budget."},
      {"category":"Utility","item":"Ceiling fan / storage essentials","platform":"Amazon","estimated_price":alloc["Utility"]*.7,"reason":"Keeps practical needs inside the plan."}]
    return _response("home",b,alloc,items,"Fallback home plan generated locally.")

def party_fallback(req):
    b=req.budget; alloc={"Catering":round(b*.50,2),"Decoration":round(b*.20,2),"Entertainment":round(b*.15,2),"Venue":round(b*.15,2)}
    per=max(b/req.guests,1)
    items=[
      {"category":"Catering","item":f"Food package for {req.guests} guests","platform":"Zomato","estimated_price":alloc["Catering"],"reason":f"Targets an average total budget of about ₹{per:.0f} per guest."},
      {"category":"Decoration","item":f"{req.event_type} decoration kit","platform":"Amazon","estimated_price":alloc["Decoration"]*.75,"reason":"Simple decor keeps the event allocation controlled."},
      {"category":"Entertainment","item":"Speaker/music setup","platform":"Amazon","estimated_price":alloc["Entertainment"]*.7,"reason":"Uses a modest entertainment allocation."},
      {"category":"Venue","item":f"{req.venue} venue option","platform":"OYO","estimated_price":alloc["Venue"]*.8,"reason":"Provides a venue/accommodation discovery route."}]
    return _response("party",b,alloc,items,"Fallback party plan generated locally.")

def jewelry_fallback(req):
    b=req.budget; alloc={"Necklace":round(b*.40,2),"Earrings":round(b*.25,2),"Bracelet":round(b*.20,2),"Reserve":round(b*.15,2)}
    color=f" in {req.outfit_color}" if req.outfit_color else ""
    items=[
      {"category":"Necklace","item":f"{req.style} statement necklace{color}","platform":"Amazon","estimated_price":alloc["Necklace"]*.7,"reason":f"Suitable for a {req.occasion.lower()} while protecting the overall budget."},
      {"category":"Earrings","item":f"{req.style} matching earrings{color}","platform":"Flipkart","estimated_price":alloc["Earrings"]*.75,"reason":"Designed as a coordinated accessory pair."},
      {"category":"Bracelet","item":"Minimal matching bracelet","platform":"Amazon","estimated_price":alloc["Bracelet"]*.65,"reason":"Adds a complementary piece without exhausting the budget."}]
    return _response("jewelry",b,alloc,items,"Fallback jewelry plan generated locally. Image-aware AI can be enabled with Gemini.")

def _response(planner,budget,allocation,recommendations,note):
    for x in recommendations: x["link"]=PLATFORM_LINKS.get(x["platform"],"#")
    return {"planner":planner,"budget":budget,"summary":f"Budget-aware {planner} recommendations prepared within ₹{budget:,.0f}.","allocation":allocation,"recommendations":recommendations,"ai_used":False,"note":note}
