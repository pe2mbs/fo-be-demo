import ew.mail
import ew.auth

def registerApi( app, cors ):
    ew.mail.registerApi( app, cors )
    ew.auth.registerApi( app, cors )
    return

def registerExtensions( app, db ):
    return

def registerShellContext( app, db ):
    return

def registerCommands( app ):

    return

