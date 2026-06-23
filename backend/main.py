import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import replicate
from dotenv import load_dotenv

# 1. Load your secret API token from the .env file
load_dotenv()

app = FastAPI()

# 2. Enable CORS so your frontend can communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_video(request: VideoRequest):
    print(f"Received prompt from frontend: {request.prompt}")
    
    # Check if the API token loaded properly
    if not os.getenv("REPLICATE_API_TOKEN"):
        print("Error: REPLICATE_API_TOKEN is missing from your .env file!")
        raise HTTPException(status_code=500, detail="API Token missing on backend.")
    
    try:
        print("Sending prompt to Replicate AI cloud... (This takes a few seconds)")
        
        # 3. Call the correct text-to-video model version on Replicate
        output = replicate.run(
            "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
            input={
                "prompt": request.prompt,
                "num_frames": 16,
                "fps": 8
            }
        )
        
        # The AI returns a list containing the web URL of your new video file
        video_url = output[0]
        print(f"Success! Generated Video URL: {video_url}")
        
        return {"video_url": video_url}
        
    except Exception as e:
        print(f"AI Generation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))