# How to Add ADMIN_API_KEY to Render

## Quick Steps to Add Environment Variable on Render:

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Log in to your account

2. **Select Your Service**
   - Click on your service: `doc-esign`

3. **Navigate to Environment**
   - Click on the "Environment" tab in the left sidebar

4. **Add the New Environment Variable**
   - Click "Add Environment Variable"
   - **Key**: `ADMIN_API_KEY`
   - **Value**: `demo-admin-key-2024`
   - Click "Save Changes"

5. **Deploy Changes**
   - Render will automatically redeploy your service with the new environment variable
   - Wait for the deploy to complete (usually takes 2-3 minutes)

## Testing the Admin Endpoints

Once deployed, you can test the admin endpoints:

### Clear All Data
```bash
curl -X DELETE "https://doc-esign.onrender.com/api/admin/clear-all-data" \
  -H "X-Admin-Key: demo-admin-key-2024" \
  -H "Content-Type: application/json"
```

### Delete Specific Signature
```bash
curl -X DELETE "https://doc-esign.onrender.com/api/admin/signature/{tracking_id}" \
  -H "X-Admin-Key: demo-admin-key-2024" \
  -H "Content-Type: application/json"
```

### Delete All Signatures for a Document Type
```bash
curl -X DELETE "https://doc-esign.onrender.com/api/admin/signatures/by-document/company_policy" \
  -H "X-Admin-Key: demo-admin-key-2024" \
  -H "Content-Type: application/json"
```

## Important Notes
- The service will automatically restart when you add the environment variable
- Make sure to use the exact same key value in your API requests
- This key is required for all admin endpoints for security
- The automatic midnight IST cleanup will also work once this is configured

## VSCode REST Client
If you're using the VSCode REST Client extension, the api.rest file is already updated with the correct admin key for all admin endpoints.