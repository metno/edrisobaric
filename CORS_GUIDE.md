# CORS Implementation Guide

## ✅ CORS is Working!

The CORS middleware has been successfully added to the EDR-isobaric API.

## Important: How to Verify CORS Headers

**CORS headers only appear when the request includes an `Origin` header.** This is standard browser behavior.

### ❌ Won't show CORS headers:
```bash
curl http://127.0.0.1:5000/collections
```

### ✅ Will show CORS headers:
```bash
curl http://127.0.0.1:5000/collections -H "Origin: https://example.com"
```

## Testing CORS

### Test 1: Simple GET request with Origin
```bash
curl -i http://127.0.0.1:5000/collections \
  -H "Origin: https://example.com"
```

Expected headers:
```
access-control-allow-origin: *
access-control-allow-credentials: true
```

### Test 2: OPTIONS preflight request
```bash
curl -i -X OPTIONS http://127.0.0.1:5000/collections \
  -H "Origin: https://example.com" \
  -H "Access-Control-Request-Method: GET"
```

Expected headers:
```
access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
access-control-max-age: 600
access-control-allow-credentials: true
access-control-allow-origin: https://example.com
```

## Browser Testing

When testing from a browser (e.g., JavaScript fetch):

```javascript
// This will automatically include the Origin header
fetch('http://127.0.0.1:5000/collections')
  .then(response => response.json())
  .then(data => console.log(data));
```

You can verify CORS headers in browser DevTools:
1. Open DevTools (F12)
2. Go to Network tab
3. Make the request
4. Click on the request
5. Check Response Headers - you'll see `access-control-allow-origin: *`

## Configuration

The CORS middleware is configured in `edriso/app.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins
    allow_credentials=True,     # Allow cookies/auth headers
    allow_methods=["*"],        # Allow all HTTP methods
    allow_headers=["*"],        # Allow all headers
)
```

### Security Note

`allow_origins=["*"]` means the API accepts requests from ANY origin. 

For production, consider restricting to specific domains:
```python
allow_origins=[
    "https://yourdomain.com",
    "https://app.yourdomain.com",
]
```

## Troubleshooting

### "I don't see CORS headers"

1. **Are you sending an Origin header?** 
   - Browsers automatically send this
   - Command-line tools (curl, httpie) don't unless you specify it

2. **Check from browser DevTools**
   - The headers will be visible in the Network tab
   - Or use a browser extension like "ModHeader" to test

3. **Verify middleware is loaded**
   ```bash
   # Check app.py contains the middleware setup
   grep -A 5 "CORSMiddleware" edriso/app.py
   ```

### Common Issues

- **405 Method Not Allowed**: This is normal if testing with HEAD requests on GET-only endpoints
- **No Origin header**: CORS only applies when Origin is present
- **Browser still blocking**: Clear browser cache and try again

## References

- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
