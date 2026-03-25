# app/routes/users.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=["Users"]
)

@router.post("/details")
async def save_user_details(request: Request):
    """
    MVP/demo mode: Receives user travel details and returns them.
    """
    try:
        data = await request.json()
        print("DEBUG: Received user details:", data)

        # Return received data
        return JSONResponse({
            "success": True,
            "message": "User travel info received (MVP/demo)",
            "user": data
        })

    except Exception as e:
        print(f"Error in save_user_details: {e}")
        return JSONResponse({
            "success": False,
            "message": "Failed to process user info",
            "error": str(e)
        }, status_code=500)