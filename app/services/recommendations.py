import json
from ..core.db import get_conn
from .gemini import generate

def save_history(user_id, planner, request_obj, response):
    conn=get_conn(); conn.execute("INSERT INTO recommendations(user_id,planner,request_json,response_json) VALUES(?,?,?,?)",(user_id,planner,json.dumps(request_obj),json.dumps(response))); conn.commit(); conn.close()

def history(user_id):
    conn=get_conn(); rows=conn.execute("SELECT id,planner,request_json,response_json,created_at FROM recommendations WHERE user_id=? ORDER BY id DESC LIMIT 30",(user_id,)).fetchall(); conn.close()
    return [dict(r) for r in rows]

def make(user_id, planner, req, image_bytes=None, mime_type=None):
    data=generate(planner,req,image_bytes,mime_type); save_history(user_id,planner,req.model_dump(),data); return data
