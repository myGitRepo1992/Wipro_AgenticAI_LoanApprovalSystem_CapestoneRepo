from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from datetime import datetime

app = FastAPI(title="NotificationSystem MCP Server")


class NotificationRequest(BaseModel):
    applicant_id: str
    applicant_name: str
    email: str
    phone: str
    case_id: str
    decision: str
    action: str


class NotificationLog(BaseModel):
    case_id: str
    timestamp: str
    status: str


notification_log = {}


@app.post("/send_notification")
def send_notification(request: NotificationRequest):
    """MCP endpoint for sending notifications."""
    try:
        notification_data = {
            "case_id": request.case_id,
            "applicant_id": request.applicant_id,
            "applicant_name": request.applicant_name,
            "email": request.email,
            "phone": request.phone,
            "decision": request.decision,
            "action": request.action,
            "timestamp": datetime.now().isoformat(),
            "status": "sent"
        }

        notification_log[request.case_id] = notification_data

        return {
            "status": "success",
            "message": f"Notification sent for case {request.case_id}",
            "notification": notification_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/notifications/{case_id}")
def get_notification(case_id: str):
    """Retrieves notification status."""
    if case_id in notification_log:
        return {"status": "success", "notification": notification_log[case_id]}
    return {"status": "not_found"}


@app.get("/notification_history")
def get_history(limit: int = 10):
    """Retrieves recent notification history."""
    recent = list(notification_log.values())[-limit:]
    return {"status": "success", "count": len(recent), "notifications": recent}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "NotificationSystem"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8004)
