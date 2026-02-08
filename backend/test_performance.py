#!/usr/bin/env python3
"""
Premium Streaming Performance Test Script
Tests cache performance and response times
"""
import httpx
import time
import asyncio

BASE_URL = "http://localhost:8000"

async def test_search():
    """Test search endpoint"""
    print("\n🔍 Testing Search Endpoint...")
    async with httpx.AsyncClient() as client:
        start = time.time()
        # Note: Search requires auth, so we'll test stream directly with a known video ID
        print("⚠️  Search endpoint requires authentication, skipping...")
        print("   Using known video ID for testing: JGwWNGJdvx8 (Ed Sheeran - Shape of You)")
        return "JGwWNGJdvx8"

async def test_stream(video_id: str, test_name: str):
    """Test stream endpoint and measure response time"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        start = time.time()
        # Use test endpoint (no auth required)
        response = await client.get(f"{BASE_URL}/test/stream/{video_id}")
        elapsed = (time.time() - start) * 1000
        
        if response.status_code == 200:
            data = response.json()
            cached = data.get('cached', False)
            fetch_time = data.get('fetch_time_ms', 0)
            cache_icon = "⚡" if cached else "🔄"
            
            print(f"{cache_icon} {test_name}: {elapsed:.0f}ms (fetch: {fetch_time}ms, cached: {cached})")
            return data
        else:
            print(f"❌ {test_name} failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None

async def main():
    print("=" * 60)
    print("🎵 PREMIUM STREAMING PERFORMANCE TEST")
    print("=" * 60)
    
    # Test health endpoint
    print("\n❤️  Testing Health Endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"✅ Backend is healthy: {response.json()}")
        else:
            print(f"❌ Health check failed")
            return
    
    # Get test video ID
    video_id = await test_search()
    if not video_id:
        print("❌ Cannot continue without video ID")
        return
    
    print(f"\n🎯 Testing with video ID: {video_id}")
    print("\n📊 Stream Performance Test (3 requests):")
    print("-" * 60)
    
    # First request (cache miss)
    await test_stream(video_id, "Request 1 (MISS)")
    
    # Wait a moment
    await asyncio.sleep(0.5)
    
    # Second request (cache hit)
    await test_stream(video_id, "Request 2 (HIT) ")
    
    # Wait a moment
    await asyncio.sleep(0.5)
    
    # Third request (cache hit)
    await test_stream(video_id, "Request 3 (HIT) ")
    
    print("\n" + "=" * 60)
    print("✅ Performance test complete!")
    print("\n📈 Expected Results:")
    print("   - First request: 2-5 seconds (yt-dlp fetch)")
    print("   - Cached requests: < 100ms (Redis/memory)")
    print("\n💡 Note: Search endpoint requires Firebase authentication.")
    print("   To test search, use the frontend or provide a valid token.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
