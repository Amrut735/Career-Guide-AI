import os

from celery import Celery
from flask import Flask

from services.career_service import analyze_profile, build_cache_key
from utils.extensions import cache
from utils.validation import AnalyzeRequest


redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
celery = Celery("career_ai", broker=redis_url, backend=redis_url)

cache_app = Flask("career_ai_cache")
cache_app.config["CACHE_TYPE"] = "RedisCache"
cache_app.config["CACHE_REDIS_URL"] = redis_url
cache_app.config["CACHE_DEFAULT_TIMEOUT"] = 3600
cache.init_app(cache_app)


@celery.task(name="generate_guidance_task")
def generate_guidance_task(payload_dict):
    payload = AnalyzeRequest.model_validate(payload_dict)
    cache_key = build_cache_key(payload)
    cached = cache.get(cache_key)
    if cached:
        return {"cached": True, **cached}

    guidance_text, json_output, user_profile, timestamp = analyze_profile(payload)
    result = {
        "guidance_text": guidance_text,
        "json_output": json_output,
        "user_profile": user_profile,
        "timestamp": timestamp,
    }
    cache.set(cache_key, result, timeout=3600)
    return {"cached": False, **result}
