---
name: ws-tester
description: Test WebSocket client/server communication. Use for real-time communication verification.
tools: Read, Glob, Grep, Bash
model: sonnet
---

WebSocket tester for cvp/ws/ modules.

## Structure
- `cvp/ws/client/` - Client implementation
- `cvp/ws/server/` - Server implementation
- `tester/ws/` - WebSocket tests

## Test Areas
- Connection (establish, reconnect, disconnect)
- Messages (text, binary, ordering)
- Errors (failures, timeouts, abnormal close)

## Async Pattern
```python
def test_connect(self):
    async def _test():
        # async test logic
        pass
    asyncio.run(_test())
```
