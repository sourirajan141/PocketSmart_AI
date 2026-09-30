from fastapi import APIRouter, HTTPException, Depends, Header
from ..models.schemas import RegisterRequest, LoginRequest
from ..core.db import get_conn
from ..core.security import hash_password, verify_password, create_access_token, decode_access_token

router=APIRouter(tags=["auth"])

def current_user(authorization: str|None=Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "): raise HTTPException(401,"Authentication required")
    try: uid=decode_access_token(authorization.split(" ",1)[1])
    except Exception: raise HTTPException(401,"Invalid or expired token")
    conn=get_conn(); u=conn.execute("SELECT id,name,email FROM users WHERE id=?",(uid,)).fetchone(); conn.close()
    if not u: raise HTTPException(401,"User not found")
    return dict(u)

@router.post("/register")
def register(body:RegisterRequest):
    conn=get_conn()
    try:
        cur=conn.execute("INSERT INTO users(name,email,password_hash) VALUES(?,?,?)",(body.name,body.email.lower(),hash_password(body.password))); conn.commit(); uid=cur.lastrowid
    except Exception: conn.close(); raise HTTPException(400,"Email is already registered")
    conn.close(); return {"message":"Registration successful","access_token":create_access_token(uid),"user":{"id":uid,"name":body.name,"email":body.email.lower()}}

@router.post("/login")
def login(body:LoginRequest):
    conn=get_conn(); u=conn.execute("SELECT * FROM users WHERE email=?",(body.email.lower(),)).fetchone(); conn.close()
    if not u or not verify_password(body.password,u["password_hash"]): raise HTTPException(401,"Invalid email or password")
    return {"message":"Login successful","access_token":create_access_token(u["id"]),"user":{"id":u["id"],"name":u["name"],"email":u["email"]}}

@router.post("/logout")
def logout(): return {"message":"Logged out. Remove the token from the browser."}

@router.get("/session-info")
def session_info(user=Depends(current_user)): return {"logged_in":True,"user":user}

@router.get("/session-data")
def session_data(user=Depends(current_user)):
    conn=get_conn(); count=conn.execute("SELECT COUNT(*) c FROM recommendations WHERE user_id=?",(user["id"],)).fetchone()["c"]; conn.close()
    return {"user":user,"recommendation_count":count}
