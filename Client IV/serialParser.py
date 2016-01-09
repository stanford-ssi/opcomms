# Proposal: Rename module to this to prevent naming conflicts

# placeholder functions for testing
last_msg = None
def sendMessage(msg): global last_msg; last_msg = msg + b"a"
def checkMessage(): return last_msg