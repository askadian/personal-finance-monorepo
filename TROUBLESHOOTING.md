# Troubleshooting Guide

This guide helps you resolve common issues when setting up and running the Personal Finance Monorepo locally.

## Table of Contents

- [npm Installation Issues](#npm-installation-issues)
  - [EACCES Permission Error](#eacces-permission-error)
  - [npm Cache Issues](#npm-cache-issues)
- [Running the Application](#running-the-application)
  - [react-scripts: command not found](#react-scripts-command-not-found)
- [Node.js Version Issues](#nodejs-version-issues)
- [General Tips](#general-tips)

## npm Installation Issues

### EACCES Permission Error

If you encounter an error like:

```
npm error code EACCES
npm error syscall mkdir
npm error path /Users/username/.npm/_cacache/index-v5/xx/xx
npm error errno -13
npm error
npm error Your cache folder contains root-owned files, due to a bug in
npm error previous versions of npm which has since been addressed.
```

**Solution 1: Fix npm cache permissions (Recommended)**

Run the following command to fix the permissions on your npm cache folder:

```bash
sudo chown -R $(whoami) ~/.npm
```

Or on macOS, if you know your user ID and group ID:
```bash
sudo chown -R 501:20 ~/.npm
```

Then try installing again:
```bash
cd frontend
npm install
```

**Solution 2: Clear npm cache**

If the permission fix doesn't work, try clearing the npm cache:

```bash
npm cache clean --force
cd frontend
npm install
```

**Solution 3: Use a different npm cache location**

You can temporarily use a different cache location:

```bash
cd frontend
npm install --cache /tmp/npm-cache
```

**Solution 4: Use npm ci instead**

If you have a `package-lock.json` file, use `npm ci` which provides a cleaner install:

```bash
cd frontend
npm ci
```

### npm Cache Issues

If you continue to have cache-related issues:

1. **Clear the cache completely:**
   ```bash
   npm cache clean --force
   ```

2. **Verify cache integrity:**
   ```bash
   npm cache verify
   ```

3. **Install with a fresh cache:**
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

### react-scripts: command not found

If you see this error:

```
sh: react-scripts: command not found
```

**Cause:** The dependencies were not installed successfully (usually due to the EACCES error above).

**Solution:**

1. First, fix any installation errors (see [EACCES Permission Error](#eacces-permission-error))
2. Install dependencies successfully:
   ```bash
   cd frontend
   npm install
   ```
3. Verify that `node_modules` directory exists:
   ```bash
   ls -la frontend/node_modules
   ```
4. Try running the application again:
   ```bash
   npm start
   ```

## Node.js Version Issues

The frontend application requires **Node.js v14 or higher**.

**Check your Node.js version:**

```bash
node --version
```

**If you need to upgrade Node.js:**

- **Using nvm (Node Version Manager) - Recommended:**
  ```bash
  # Install nvm if you haven't already
  # Visit: https://github.com/nvm-sh/nvm
  
  # Install the latest LTS version
  nvm install --lts
  
  # Use the LTS version
  nvm use --lts
  ```

- **Direct download:**
  Visit [nodejs.org](https://nodejs.org/) and download the latest LTS version.

## General Tips

### Fresh Start

If you're experiencing persistent issues, try a complete fresh start:

```bash
# Navigate to frontend directory
cd frontend

# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
npm install

# Start the application
npm start
```

### Check for Global npm Issues

Sometimes global npm configuration can cause issues:

```bash
# Check npm configuration
npm config list

# Reset to defaults if needed
npm config delete cache
npm config delete prefix
```

### Use Yarn as an Alternative

If npm continues to cause issues, you can try using Yarn:

```bash
# Install Yarn globally
npm install -g yarn

# Navigate to frontend directory
cd frontend

# Install dependencies
yarn install

# Start the application
yarn start
```

### Verify Package Integrity

Ensure your `package.json` and `package-lock.json` are not corrupted:

```bash
cd frontend
npm install --package-lock-only
```

## Still Having Issues?

If you've tried all the above solutions and still can't run the application:

1. Check the [Issues](https://github.com/askadian/personal-finance-monorepo/issues) page to see if others have reported similar problems
2. Create a new issue with:
   - Your operating system and version
   - Node.js version (`node --version`)
   - npm version (`npm --version`)
   - Complete error message
   - Steps you've already tried

## Successful Installation

Once installation is successful, you should see:

```
added 1298 packages, and audited 1299 packages in XXs

267 packages are looking for funding
  run `npm fund` for details
```

And when you run `npm start`, you should see:

```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
```

The application will automatically open in your default browser, or you can manually navigate to [http://localhost:3000](http://localhost:3000).
