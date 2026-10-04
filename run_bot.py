import asyncio
import os
import sys

# Ensure project root and backend are on sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
backend_dir = os.path.join(root_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from bot.bot import main

if __name__ == "__main__":
    asyncio.run(main())
