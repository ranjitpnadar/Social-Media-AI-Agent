# services/llm_client.py
from together import Together
from dotenv import load_dotenv
import time
load_dotenv()

_client = None

def get_together_client() -> Together:
    """Returns a singleton Together client."""
    global _client
    if _client is None:
        _client = Together()  # Reads TOGETHER_API_KEY from env automatically
    return _client

def chat_completion(
    messages: list[dict],
    model: str = "google/gemma-3n-E4B-it",
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> str:
    """
    Generic chat completion wrapper around Together API.
    Returns the assistant message content as a string.
    """
    client = get_together_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content

def image_generation(
    prompt: str,
    model: str = "black-forest-labs/FLUX.2-dev",
    width: int = 1024,
    height: int = 1024,
    steps: int = 4,
    n: int = 1,
) -> list[str]:
    """
    Generates images using Together's /v1/images/generations endpoint.
    Returns a list of image URLs.
    """
    client = get_together_client()
    response = client.images.generate(
        prompt=prompt,
        model=model,
        width=width,
        height=height,
        steps=steps,
        n=n,
    )
    urls = [img.url for img in response.data]
    return urls

def video_generation(
    prompt: str,
    model: str = "minimax/video-01-director",
    width: int = 1366,
    height: int = 768,
    seconds: str = "5", 
    fps: int = 24,
    steps: int = 20,
    guidance_scale: float = 7.0,
    output_format: str = "MP4",
    output_quality: int = 20,
    negative_prompt: str = "blurry, low quality, distorted",
    max_wait:int = 300
) -> str | None:
    """
    Generates video using Together's videos endpoint.
    Polls until complete and returns the video URL.
    """
    client = get_together_client()

    try:
        payload = dict(
            prompt=prompt,
            model=model,
            width=width,
            height=height,
            seconds=seconds,
            fps=fps,
            steps=steps,
            guidance_scale=guidance_scale,
            output_format=output_format,
            output_quality=output_quality,
        )
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        # ✅ frame_images completely omitted — only pass when you have real keyframe data

        print(f"🎬 Submitting video job | model={model} | {width}x{height} | {seconds}s")

        job = client.videos.create(**payload)
        print(f"✅ Video job submitted: {job}")
        # Poll for completion
        elapsed = 0
        while elapsed < max_wait:
            status = client.videos.retrieve(job.id)
            print(f"⏳ [{elapsed}s] Status: {status.status}")

            if status.status == "completed":
                url = status.outputs.video_url   # ✅ correct field per docs
                print(f"✅ Video ready: {url}")
                return url

            elif status.status == "failed":
                error = getattr(status, "error", None)
                print(f"❌ Job failed: {error}")
                return None

            time.sleep(poll_interval)
            elapsed += poll_interval

        print(f"❌ Timed out after {max_wait}s")
        return None
    except Exception as e:
        print(f"❌ Error submitting video job: {str(e)}")


    # Poll until complete
    # elapsed = 0
    # while elapsed < max_wait:
    #     video_response = client.videos.retrieve(job_id)
    #     status = video_response.status

    #     print(f"⏳ Status: {status} ({elapsed}s elapsed)")

    #     if status == "completed":
    #         url = video_response.download_url
    #         print(f"✅ Video ready: {url}")
    #         return url

    #     elif status == "failed":
    #         print(f"❌ Video job failed: {video_response}")
    #         return None

    #     time.sleep(poll_interval)
    #     elapsed += poll_interval

    print(f"❌ Video generation timed out after {max_wait}s")
    return None