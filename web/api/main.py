from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add parent directory to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.engines.discovery_engine import DiscoveryEngine
from src.engines.troubleshooting_engine import TroubleshootingEngine
from src.engines.backup_manager import BackupManager
from src.engines.reporting_engine import ReportingEngine
from src.utils.config_manager import ConfigManager
from src.utils.credential_manager import CredentialManager

app = FastAPI(title="SNATT API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
config_manager = ConfigManager()
config = config_manager.load_config()
credential_manager = CredentialManager()

# Request/Response Models
class ScanRequest(BaseModel):
    ip_range: str

class ConnectRequest(BaseModel):
    device_ids: List[str]

class DiagnosticsRequest(BaseModel):
    workflow: str

class BackupRequest(BaseModel):
    backup_type: str

class ReportRequest(BaseModel):
    report_type: str
    format: str

class CredentialRequest(BaseModel):
    name: str
    username: str
    password: str
    enable_password: Optional[str] = None

# In-memory storage (for demo - use database in production)
devices_db = []
diagnostics_results = []
backup_history = []

@app.get("/")
async def root():
    return {"message": "SNATT API", "version": "1.0.0"}

# Discovery endpoints
@app.post("/api/discovery/scan")
async def scan_network(request: ScanRequest):
    try:
        discovery_engine = DiscoveryEngine(config)
        devices = discovery_engine.scan_network(request.ip_range)
        
        # Store devices
        global devices_db
        devices_db = [
            {
                "id": str(i),
                "ip_address": device.ip_address,
                "hostname": device.hostname,
                "vendor": device.vendor,
                "status": device.status.value if hasattr(device.status, 'value') else str(device.status)
            }
            for i, device in enumerate(devices)
        ]
        
        return {"devices": devices_db}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/discovery/connect")
async def connect_devices(request: ConnectRequest):
    try:
        # Simulate connection
        connected_count = len(request.device_ids)
        
        # Update device status
        for device in devices_db:
            if device["id"] in request.device_ids:
                device["status"] = "connected"
        
        return {"connected": connected_count, "message": f"Connected to {connected_count} devices"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Diagnostics endpoints
@app.post("/api/diagnostics/run")
async def run_diagnostics(request: DiagnosticsRequest):
    try:
        # Get connected devices
        connected_devices = [d for d in devices_db if d.get("status") == "connected"]
        
        if not connected_devices:
            return {"results": [], "message": "No connected devices"}
        
        # Simulate diagnostic results
        results = []
        for device in connected_devices:
            results.append({
                "device_name": device.get("hostname", "Unknown"),
                "device_ip": device["ip_address"],
                "severity": "info",
                "message": f"{request.workflow} completed successfully",
                "details": "All checks passed"
            })
        
        global diagnostics_results
        diagnostics_results = results
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Backup endpoints
@app.post("/api/backup/create")
async def create_backup(request: BackupRequest):
    try:
        connected_devices = [d for d in devices_db if d.get("status") == "connected"]
        
        if not connected_devices:
            raise HTTPException(status_code=400, detail="No connected devices to backup")
        
        # Simulate backup
        from datetime import datetime
        for device in connected_devices:
            backup_history.append({
                "device_name": device.get("hostname", device["ip_address"]),
                "type": request.backup_type,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            })
        
        return {"message": f"Backup completed for {len(connected_devices)} devices"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/backup/history")
async def get_backup_history():
    return {"backups": backup_history}

# Reports endpoints
@app.post("/api/reports/generate")
async def generate_report(request: ReportRequest):
    try:
        # In a real implementation, generate actual report file
        return {
            "message": "Report generated",
            "report_type": request.report_type,
            "format": request.format
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Settings endpoints
@app.post("/api/settings/credentials")
async def add_credential(request: CredentialRequest):
    try:
        credential_manager.add_credential(
            name=request.name,
            username=request.username,
            password=request.password,
            enable_password=request.enable_password
        )
        return {"message": "Credential added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/settings/credentials")
async def get_credentials():
    try:
        creds = credential_manager.list_credentials()
        return {"credentials": [{"name": name, "username": username} for name, username in creds]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
