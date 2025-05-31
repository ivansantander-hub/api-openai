# 🔐 Authentication Setup Guide

## Railway Environment Variables

To enable authentication for your OpenAI API Client, you need to set up environment variables in Railway.

### Required Environment Variables

1. **ACCESS_KEY** - The secret key that users must enter to access the service
2. **OPENAI_API_KEY** - Your OpenAI API key (already configured)

### Setting up ACCESS_KEY in Railway

1. **Go to your Railway dashboard** and select your project
2. **Click on your service** (usually called "api-openai")
3. **Go to the Variables tab**
4. **Add a new variable:**
   - **Variable Name:** `ACCESS_KEY`
   - **Value:** Enter a secure key (e.g., `my-super-secret-key-2024`)

### Example Configuration

```
ACCESS_KEY=your-secure-access-key-here
OPENAI_API_KEY=sk-your-openai-key-here
```

### Security Recommendations

- **Use a strong, unique key** - Mix letters, numbers, and symbols
- **Keep it secret** - Don't share the key publicly
- **Change it periodically** - Update the key regularly for security
- **Use different keys** - Different keys for different environments (dev/prod)

### Example Strong Keys

```
ACCESS_KEY=OpenAI-2024-SecureKey!89
ACCESS_KEY=AI-Service-Ultra-Safe#2024
ACCESS_KEY=MyApp-Secret-Pass_2024$99
```

### How It Works

1. **User visits the website** → Login modal appears
2. **User enters the access key** → Frontend sends key to `/auth` endpoint
3. **Backend validates the key** → Compares with `ACCESS_KEY` environment variable
4. **If valid** → User gets access to all OpenAI features
5. **If invalid** → Access denied, must try again

### Testing

After setting up the `ACCESS_KEY` variable:

1. **Deploy your application** to Railway
2. **Visit your application URL**
3. **Enter the access key** you configured
4. **Access should be granted** if the key matches

### Troubleshooting

If authentication isn't working:

1. **Check that ACCESS_KEY is set** in Railway variables
2. **Verify the key value** matches exactly (case-sensitive)
3. **Check application logs** in Railway for error messages
4. **Try redeploying** the service after adding the variable

### Additional Security Features

The authentication system includes:

- **Token persistence** - Key is remembered in browser until logout
- **Automatic logout** - Invalid tokens are cleared automatically
- **Secure transmission** - Key is sent via HTTPS
- **Session management** - Each user session is independent

---

**⚠️ Important:** Make sure to set the `ACCESS_KEY` environment variable in Railway before users try to access your application! 