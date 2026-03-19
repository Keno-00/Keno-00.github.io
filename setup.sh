#!/bin/bash
# Quick setup script for kenojose.site

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== kenojose.site Quick Setup ===${NC}\n"

# Check structure
echo "Checking directory structure..."
if [ -f "index.html" ] && [ -f "blog.html" ] && [ -f "css/style.css" ]; then
    echo -e "${GREEN}✓ All files present${NC}"
else
    echo "✗ Missing files. Run setup first."
    exit 1
fi

# Check asset directory
if [ ! -d "assets" ]; then
    mkdir -p assets
    echo -e "${GREEN}✓ Created assets directory${NC}"
else
    echo -e "${GREEN}✓ Assets directory exists${NC}"
fi

# Check avatar
if [ ! -f "assets/avatar.png" ]; then
    echo -e "${BLUE}Note: Add your avatar to assets/avatar.png${NC}"
else
    echo -e "${GREEN}✓ Avatar found${NC}"
fi

# Offer to start server
echo ""
echo "Ready to test locally?"
read -p "Start HTTP server on port 8000? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Starting server...${NC}"
    echo "Visit http://localhost:8000"
    python3 -m http.server 8000
fi
